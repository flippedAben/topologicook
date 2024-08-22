import json
import os
from dataclasses import dataclass
from datetime import datetime
from zipfile import ZipFile

import httpx
from loguru import logger

from topologicook.env import ENV


def pull_foundational_food_data():
    zip_path = "data/foundational_foods.zip"
    if not os.path.exists(zip_path):
        # As of Aug 2024, USDA site uses HTTP/1.1, so no need for httpx there.
        # However, recipe websites may use HTTP2, so use it.
        response_zip = httpx.get(ENV.FOUNDATIONAL_FOODS_JSON_URL)

        os.makedirs("data", exist_ok=True)
        with open(zip_path, "wb") as f:
            f.write(response_zip.content)

        logger.info(f"created {zip_path}")

    data_name = "foundationDownload.json"
    json_path = f"data/{data_name}"
    if not os.path.exists(json_path):
        with ZipFile(zip_path) as zip:
            # The ZIP file should only contain a single JSON file.
            assert zip.namelist() == [data_name]
            zip.extract(data_name, "data")

        logger.info(f"created {json_path}")


def load_foundationa_food_data():
    with open("data/foundationDownload.json", "r") as f:
        data = json.load(f)

    assert len(data) == 1
    assert "FoundationFoods" in data
    foods = data["FoundationFoods"]

    assert isinstance(foods, list)

    @dataclass
    class Nutrient:
        fdc_id: int
        name: str
        amount: float
        unit: str

    @dataclass
    class Food:
        fdc_id: int
        name: str
        category: str
        # Based on 100g of the food
        nutrients: list[Nutrient]
        publication_date: datetime

    parsed_foods: list[Food] = []
    for food in foods:
        name = food["description"]
        if "foodPortions" not in food:
            logger.warning(f"missing food portion data: {name}")

        if "nutrientConversionFactors" not in food:
            logger.warning(f"missing nutrient conversion data: {name}")

        parsed_nutrients = []
        for nutrient in food["foodNutrients"]:
            if "amount" not in nutrient:
                logger.warning(f"missing {nutrient["nutrient"]["name"]}: {name}")
                continue

            parsed_nutrients.append(
                Nutrient(
                    nutrient["id"],
                    nutrient["nutrient"]["name"],
                    nutrient["nutrient"]["unitName"],
                    nutrient["amount"],
                )
            )

        parsed_foods.append(
            Food(
                food["fdcId"],
                name,
                food["foodCategory"]["description"],
                parsed_nutrients,
                datetime.strptime(food["publicationDate"], "%m/%d/%Y"),
            )
        )

    nutrient_count = {}
    nutrient_names = {}
    for food in parsed_foods:
        for n in food.nutrients:
            nutrient_count[n.fdc_id] = nutrient_count.get(n.fdc_id, 0) + 1
            if n.name in nutrient_names:
                nutrient_names[n.name].append(n.fdc_id)
            else:
                nutrient_names[n.name] = [n.fdc_id]

    print(nutrient_names)


def pull_fndds_data():
    _, filename = os.path.split(ENV.FNDDS_CSV_URL)

    zip_path = f"data/{filename}"
    if not os.path.exists(zip_path):
        response_zip = httpx.get(ENV.FNDDS_CSV_URL)

        os.makedirs("data", exist_ok=True)
        with open(zip_path, "wb") as f:
            f.write(response_zip.content)

        logger.info(f"created {zip_path}")

    with ZipFile(zip_path) as zip:
        zip.extractall("data")


def load_fndds_data():
    _, filename = os.path.split(ENV.FNDDS_CSV_URL)
    dirname, _ = os.path.splitext(filename)


pull_fndds_data()
