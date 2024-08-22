import os
import xml.etree.ElementTree as ElementTree
from dataclasses import dataclass
from typing import Any

import httpx
import orjson
from loguru import logger
from recipe_scrapers import scrape_html


@dataclass
class Recipe:
    name: str
    ingredients: list[str]
    instructions: list[str]
    source_url: str
    nutrition: Any | None = None


# parse serious eats sitemap
sitemap_path = "data/serious_eats_sitemap_1.xml"
if not os.path.exists(sitemap_path):
    sitemap_url = "https://www.seriouseats.com/sitemap_1.xml"
    response = httpx.get(sitemap_url)

    os.makedirs("data", exist_ok=True)
    with open(sitemap_path, "wb") as f:
        f.write(response.content)

tree = ElementTree.parse(sitemap_path)
root = tree.getroot()
assert root.tag == r"{http://www.sitemaps.org/schemas/sitemap/0.9}urlset"

recipe_urls = []
namespace = root.tag[0:-6]
for element in root.iter(f"{namespace}loc"):
    recipe_url = element.text
    recipe_urls.append(recipe_url)


# load in visited cache
html_path = "data/recipes"
os.makedirs(html_path, exist_ok=True)
visited_recipes_log = f"{html_path}/visited.log"
visited_recipes = set()
if os.path.exists(visited_recipes_log):
    with open(visited_recipes_log) as f:
        for line in f:
            line = line.strip()
            if line:
                visited_recipes.add(line)


# write to append only log
with open(visited_recipes_log, "a") as log_f:
    with open(f"{html_path}/raw_data.jsonl", "a") as f:
        for url in recipe_urls[:100]:
            _, name = os.path.split(url)
            if name in visited_recipes:
                continue

            html = httpx.get(url)
            scraper = scrape_html(html.content, org_url=url)
            try:
                data = scraper.to_json()
            except NotImplementedError:
                logger.warning(f"to_json failed. Skip scraping: {url}")
                log_f.write(name + "\n")
                visited_recipes.add(name)
                continue

            if (
                "title" not in data
                or "ingredients" not in data
                or "instructions" not in data
            ):
                # it's not a recipe, so skip
                logger.warning(f"Not a recipe. Skip scraping: {url}")
                log_f.write(name + "\n")
                visited_recipes.add(name)
                continue

            f.write(orjson.dumps(data).decode() + "\n")
            log_f.write(name + "\n")
            visited_recipes.add(name)
