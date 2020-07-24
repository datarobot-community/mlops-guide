import uuid
from random import randint, seed, uniform
from typing import Optional


class Car:
    """Generates an `average` car based on the minimum and maximum values
    found in the original Auto MPG dataset."""

    MIN_ACCELERATION = 8.15
    MAX_ACCELERATION = 24.80
    MIN_CYLINDERS = 3
    MAX_CYLINDERS = 12
    MIN_DISPLACEMENT = 68
    MAX_DISPLACEMENT = 455
    MIN_HORSEPOWER = 46
    MAX_HORSEPOWER = 230
    MIN_MODEL_YEAR = 70
    MAX_MODEL_YEAR = 82
    MIN_ORIGIN = 1
    MAX_ORIGIN = 3
    MIN_WEIGHT = 1613
    MAX_WEIGHT = 4997

    def __init__(self, random_seed: Optional[int] = None):
        if random_seed is not None:
            seed(a=random_seed)
        self._acceleration: Optional[float] = round(
            uniform(self.MIN_ACCELERATION, self.MAX_ACCELERATION), 2
        )
        self._cylinders: Optional[int] = randint(
            self.MIN_CYLINDERS, self.MAX_CYLINDERS
        )
        self._displacement: Optional[float] = randint(
            self.MIN_DISPLACEMENT, self.MAX_DISPLACEMENT
        )
        self._horsepower: Optional[float] = round(
            uniform(self.MIN_HORSEPOWER, self.MAX_HORSEPOWER), 2
        )
        self._model_year: Optional[int] = randint(
            self.MIN_MODEL_YEAR, self.MAX_MODEL_YEAR
        )
        self._origin: Optional[int] = randint(self.MIN_ORIGIN, self.MAX_ORIGIN)
        self._weight: Optional[float] = round(
            uniform(self.MIN_WEIGHT, self.MAX_WEIGHT), 2
        )

    def __repr__(self):
        return (
            f"<Car("
            f"acceleration={self.acceleration}, cylinders={self.cylinders}, "
            f"displacement={self.displacement}, horsepower={self.horsepower}, "
            f"model_year={self.model_year}, origin={self.origin}, "
            f"weight={self.weight})"
        )

    def __iter__(self):
        fields = {
            "car_id": self.car_id,
            "acceleration": self.acceleration,
            "cylinders": self.cylinders,
            "displacement": self.displacement,
            "horsepower": self.horsepower,
            "model year": self.model_year,
            "origin": self.origin,
            "weight": self.weight,
        }
        for prop, val in fields.items():
            yield prop, val

    @property
    def car_id(self):
        return uuid.uuid4().hex[:8]

    @property
    def acceleration(self):
        return self._acceleration

    @property
    def cylinders(self):
        return self._cylinders

    @property
    def displacement(self):
        return self._displacement

    @property
    def horsepower(self):
        return self._horsepower

    @property
    def model_year(self):
        return self._model_year

    @property
    def origin(self):
        return self._origin

    @property
    def weight(self):
        return self._weight
