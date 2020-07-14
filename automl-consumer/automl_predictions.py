import csv
import json
import os
import signal
from datetime import datetime, timezone
from pathlib import Path
from pprint import pformat
from time import sleep, monotonic
from typing import Optional, List

import requests

from loguru import logger as log

# noinspection PyUnresolvedReferences
# this script is run from within a docker container
# the following will be present at build time
from auto_mpg import Car

DATAROBOT_API_TOKEN = os.getenv("DATAROBOT_API_TOKEN")
DATAROBOT_ENDPOINT = os.getenv("DATAROBOT_ENDPOINT")
DATAROBOT_DEPLOYMENT_ID = os.getenv("DATAROBOT_DEPLOYMENT_ID")
KEEP_ALIVE = int(os.getenv("KEEP_ALIVE", 300))
now = datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

log.add(Path("/var").joinpath("log", "mlops", f"automl_predictions-{now}.log"))


def get_car_prediction(cars: List[Car]) -> Optional[List]:
    prediction_headers = {
        "Authorization": f"Bearer {DATAROBOT_API_TOKEN}",
        "Content-Type": "application/json; charset=UTF-8",
    }
    url = f"{DATAROBOT_ENDPOINT}/deployments/{DATAROBOT_DEPLOYMENT_ID}/predictions/"
    response = None
    try:
        payload = [dict(car) for car in cars]
        response = requests.post(
            url, headers=prediction_headers, data=json.dumps(payload),
        )
        assert response.status_code == 200
    except AssertionError:
        log.error(f"Something went wrong. Status: {response.status_code}")
        return None
    else:
        _predictions = response.json()
        data = _predictions["data"]
        return [
            [car["passthroughValues"]["car_id"], round(car["prediction"], 2)]
            for car in data
        ]


class Shutdown:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True


if __name__ == "__main__":
    shutdown = Shutdown()
    predictions = []
    start = monotonic()
    while not shutdown.kill_now:
        if monotonic() - start > KEEP_ALIVE:
            log.info("Elapse time exceeds KEEP_ALIVE time. Shutting down...")
            break
        some_cars = [Car() for _ in range(100)]
        log.info("Making predictions.")
        summary = get_car_prediction(some_cars)
        predictions.extend(summary)
        sleep(5)
    summary_file = Path("/var").joinpath("log", "mlops", f"summary-{now}.csv")
    with summary_file.open("w") as f:
        writer = csv.writer(f)
        writer.writerow(["car_id", "mpg"])
        writer.writerows(predictions)
