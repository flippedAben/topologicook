import os
from dataclasses import dataclass, fields

from dotenv import load_dotenv


@dataclass()
class Env:
    FOUNDATIONAL_FOODS_JSON_URL: str
    FNDDS_CSV_URL: str

    def __init__(self, **kwargs):
        names = set(field.name for field in fields(self))
        for key, value in kwargs.items():
            if key in names:
                setattr(self, key, value)


load_dotenv()
ENV = Env(**os.environ)
