import csv
import json
import os
import signal
from datetime import datetime
from pathlib import Path
from pprint import pformat
from time import sleep
from typing import Dict, Optional, List

import requests

# noinspection PyUnresolvedReferences
from auto_mpg import Car
from loguru import logger as log


# def handle_sigterm(*args):
#     raise KeyboardInterrupt()


DATAROBOT_API_TOKEN = os.getenv("DATAROBOT_API_TOKEN")
DATAROBOT_KEY = os.getenv("DATAROBOT_KEY")
DATAROBOT_ENDPOINT = os.getenv("DATAROBOT_ENDPOINT")
DATAROBOT_DEPLOYMENT_ID = os.getenv("DATAROBOT_DEPLOYMENT_ID")
now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

log.add(Path().cwd().joinpath("logs", f"automl_predictions-{now}.log"))


def get_car_prediction(cars: List[Car]) -> Optional[List]:
    prediction_headers = {
        "Authorization": f"Bearer {DATAROBOT_API_TOKEN}",
        "Content-Type": "application/json; charset=UTF-8",
        "datarobot-key": DATAROBOT_KEY,
    }
    url = (
        f"https://datarobot-predictions.orm.datarobot.com/predApi/v1.0/"
        f"deployments/{DATAROBOT_DEPLOYMENT_ID}/predictions"
    )

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
        predictions = response.json()
        log.info(f"Predictions:\n{pformat(predictions)}")
        data = predictions["data"]
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
    while not shutdown.kill_now:
        some_cars = [Car() for _ in range(10)]
        log.info("Making predictions.")
        summary = get_car_prediction(some_cars)
        predictions.extend(summary)
        sleep(1)
    summary_file = Path().cwd().joinpath("logs", f"summary-{now}.csv")
    with summary_file.open("w") as f:
        writer = csv.writer(f)
        writer.writerow(["car_id", "mpg"])
        writer.writerows(predictions)
