import json
import os
from datetime import datetime
from pathlib import Path
from pprint import pformat
from time import sleep
from typing import Dict, Optional, List

import requests

# noinspection PyUnresolvedReferences
from auto_mpg import Car
from loguru import logger as log

DATAROBOT_API_TOKEN = os.getenv("DATAROBOT_API_TOKEN")
DATAROBOT_KEY = os.getenv("DATAROBOT_KEY")
DATAROBOT_ENDPOINT = os.getenv("DATAROBOT_ENDPOINT")
DATAROBOT_DEPLOYMENT_ID = os.getenv("DATAROBOT_DEPLOYMENT_ID")
now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

log.add(Path().cwd().joinpath("logs", f"automl_predictions-{now}.log"))


def get_car_prediction(cars: List[Car]) -> Optional[Dict]:
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
        prediction = response.json()
        log.info(f"Predictions:\n{pformat(prediction)}")
        return prediction


if __name__ == "__main__":
    try:
        while True:
            some_cars = [Car() for _ in range(10)]
            log.info("Making predictions.")
            predictions = get_car_prediction(some_cars)
            sleep(1)
    except KeyboardInterrupt:
        pass
