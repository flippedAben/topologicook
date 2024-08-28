from pprint import pprint

import orjson
from loguru import logger

from topologicook.recipe import Recipe

source_data_path = "data/raw_metadata/data.jsonl"
with open(source_data_path, "r") as f:
    for line in f:
        data = orjson.loads(line)
        assert "json-ld" in data
        assert "microdata" in data
        assert "source_url" in data

        json_ld_recipes = []
        for item in data["json-ld"]:
            assert "@type" in item
            if "Recipe" in item["@type"]:
                json_ld_recipes.append(item)

        if len(json_ld_recipes) == 0:
            logger.info(f"Not a recipe: {data["source_url"]}")
        else:
            # Take the first recipe and disregard the others. We only support recipe web sites
            # with one recipe per page.
            recipe = Recipe.from_json_ld(json_ld_recipes[0])
            pprint(recipe)

        # TODO implement above for microdata
