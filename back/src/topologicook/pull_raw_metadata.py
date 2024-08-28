import os
import xml.etree.ElementTree as ElementTree

import extruct
import httpx
import orjson
from loguru import logger

sitemap_path = "data/serious_eats_sitemap_1.xml"
if not os.path.exists(sitemap_path):
    sitemap_url = "https://www.seriouseats.com/sitemap_1.xml"
    response = httpx.get(sitemap_url)

    os.makedirs("data", exist_ok=True)
    with open(sitemap_path, "wb") as f:
        f.write(response.content)

    logger.info("Pulled sitemap")


tree = ElementTree.parse(sitemap_path)
root = tree.getroot()
assert root.tag == r"{http://www.sitemaps.org/schemas/sitemap/0.9}urlset"
namespace = root.tag[0 : -len("urlset")]
recipe_urls = []
for element in root.iter(f"{namespace}loc"):
    recipe_url = element.text
    recipe_urls.append(recipe_url)

logger.info("Parsed sitemap")


# load in visited cache
html_path = "data/raw_metadata"
os.makedirs(html_path, exist_ok=True)
visited_log = f"{html_path}/visited.log"
visited_names = set()
if os.path.exists(visited_log):
    with open(visited_log) as f:
        for line in f:
            line = line.strip()
            if line:
                visited_names.add(line)

logger.info("Loaded visited.log")


# write to append only log
with open(visited_log, "a") as log_f:
    with open(f"{html_path}/data.jsonl", "a") as f:
        for url in recipe_urls[:100]:
            _, name = os.path.split(url)
            if name in visited_names:
                continue

            html = httpx.get(url)
            data = extruct.extract(html.content, syntaxes=["json-ld", "microdata"])
            assert len(data) == 2
            assert "json-ld" in data
            assert "microdata" in data
            data["source_url"] = url

            f.write(orjson.dumps(data).decode() + "\n")
            log_f.write(name + "\n")
            visited_names.add(name)
            logger.info(f"Wrote {url}")
