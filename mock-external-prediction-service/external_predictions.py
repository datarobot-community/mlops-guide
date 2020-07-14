import csv
import os
import signal
from datetime import datetime, timezone
from pathlib import Path
from time import sleep, monotonic
from typing import Optional, List

import joblib

from loguru import logger as log

# noinspection PyUnresolvedReferences
# this script is run from within a docker container
# the following will be present at build time
from auto_mpg import Car
from datarobot.mlops.mlops import MLOps
from datarobot.mlops.common.enums import OutputType

MLOPS_DEPLOYMENT_ID = os.getenv("MLOPS_DEPLOYMENT_ID")
MLOPS_MODEL_ID = os.getenv("MLOPS_MODEL_ID")
OUTPUT_TYPE = OutputType.OUTPUT_DIR
SPOOL_DIR = "/tmp/ta"
SPOOL_MAX_FILE_SIZE = 104_857_600
SPOOL_MAX_FILES = 5
KEEP_ALIVE = int(os.getenv("KEEP_ALIVE", 60))
now = datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

log.add(
    Path("/var").joinpath("log", "mlops", f"external_predictions-{now}.log")
)

model = joblib.load("gbr.joblib")


def report_to_service_health(n_predictions: int, elapse_time: float):
    """Use DataRobot mlops client to report service health"""
    mlops = (
        MLOps()
        .set_deployment_id(MLOPS_DEPLOYMENT_ID)
        .set_model_id(MLOPS_MODEL_ID)
        .set_output_type(OUTPUT_TYPE)
        .set_spool_dir(SPOOL_DIR)
        .set_spool_file_max_size(SPOOL_MAX_FILE_SIZE)
        .set_spool_max_files(SPOOL_MAX_FILES)
        .init()
    )
    mlops.report_deployment_stats(
        num_predictions=n_predictions, execution_time_ms=elapse_time * 1_000
    )
    mlops.shutdown()


def mpg_predictions(cars: List[Car]) -> Optional[List]:
    global model
    x_values = [
        [car.horsepower, car.acceleration, car.model_year, car.origin]
        for car in cars
    ]
    try:
        start_time = monotonic()
        _predictions = model.predict(x_values)
        elapse_time = monotonic() - start_time
    except Exception as _e:
        log.error(_e)
        return None
    else:
        report_to_service_health(len(_predictions), elapse_time)
        car_id_w_prediction = list(zip([car.car_id for car in cars], x_values))
        log.info(f"Predictions: {car_id_w_prediction}")
        return car_id_w_prediction


class Shutdown:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True


if __name__ == "__main__":
    # Model input: horsepower, acceleration, model year, origin
    shutdown = Shutdown()
    predictions = []
    start = monotonic()
    while not shutdown.kill_now:
        if monotonic() - start > KEEP_ALIVE:
            log.info("Elapse time exceeds KEEP_ALIVE time. Shutting down...")
            break
        some_cars = [Car() for _ in range(100)]
        log.info("Making predictions.")
        summary = mpg_predictions(some_cars)
        predictions.extend(summary)
        sleep(5)
    summary_file = Path("/var").joinpath(
        "log", "mlops", f"external-summary-{now}.csv"
    )
    with summary_file.open("w") as f:
        writer = csv.writer(f)
        writer.writerow(["car_id", "mpg"])
        writer.writerows(predictions)
