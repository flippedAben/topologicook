import os

import orjson
from loguru import logger

from topologicook.recipe import Recipe

# load in visited cache
source_data_path = "data/raw_metadata/data.jsonl"
dest_path = "data/recipes"
os.makedirs(dest_path, exist_ok=True)
visited_log = f"{dest_path}/visited.log"
visited_names = set()
if os.path.exists(visited_log):
    with open(visited_log) as f:
        for line in f:
            line = line.strip()
            if line:
                visited_names.add(line)

    logger.info("Loaded visited.log")

with open(f"{dest_path}/data.jsonl", "a") as dest_f:
    with open(visited_log, "a") as dest_log_f:
        with open(source_data_path, "r") as source_f:
            for line in source_f:
                data = orjson.loads(line)
                assert "json-ld" in data
                assert "microdata" in data
                assert "source_url" in data

                _, name = os.path.split(data["source_url"])
                if name in visited_names:
                    continue

                json_ld_recipes = []
                for item in data["json-ld"]:
                    assert "@type" in item
                    if "Recipe" in item["@type"]:
                        json_ld_recipes.append(item)

                if len(json_ld_recipes) == 0:
                    logger.info(f"Not a recipe: {name}")
                else:
                    # Take the first recipe and disregard the others. We only support recipe web sites
                    # with one recipe per page.
                    if len(json_ld_recipes) > 1:
                        logger.warning(
                            f"More than 1 JSON LD item in {data["source_url"]}"
                        )

                    recipe = Recipe.from_json_ld(json_ld_recipes[0])
                    dest_f.write(orjson.dumps(recipe).decode() + "\n")

                dest_log_f.write(name + "\n")
                visited_names.add(name)
                logger.info(f"Wrote {name}")

                # TODO implement above for microdata
