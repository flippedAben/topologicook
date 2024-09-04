from dataclasses import dataclass
from typing import Any, Self

from dacite import from_dict


@dataclass
class ImageObject:
    url: str


@dataclass
class Person:
    name: str
    url: str


@dataclass
class Organization:
    name: str
    url: str
    brand: str


@dataclass
class NutritionInformation:
    calories: str
    carbohydrateContent: str
    cholesterolContent: str
    fatContent: str
    fiberContent: str
    proteinContent: str
    saturatedFatContent: str
    sodiumContent: str
    sugarContent: str
    unsaturatedFatContent: str


@dataclass
class HowToStep:
    text: str
    image: list[ImageObject] | None = None


@dataclass
class TimeRange:
    minValue: str
    maxValue: str


@dataclass
class Recipe:
    headline: str
    datePublished: str
    dateModified: str
    author: list[Person]
    description: str
    image: ImageObject
    publisher: Organization
    name: str
    recipeCategory: list[str]
    recipeCuisine: list[str]
    recipeIngredient: list[str]
    recipeInstructions: list[HowToStep]
    totalTime: str | TimeRange
    cookTime: str | None = None
    prepTime: str | None = None
    nutrition: NutritionInformation | None = None

    @classmethod
    def from_json_ld(cls, data: dict[str, Any]) -> Self:
        remove_at_sign_keys(data)
        return from_dict(data_class=Recipe, data=data)


def remove_at_sign_keys(data: Any):
    if isinstance(data, dict):
        keys = list(data.keys())
        for key in keys:
            if key.startswith("@"):
                data.pop(key)
            else:
                remove_at_sign_keys(data[key])
    elif isinstance(data, list):
        for item in data:
            remove_at_sign_keys(item)
