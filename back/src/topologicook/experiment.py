from pprint import pprint

import extruct
import httpx


def see_if_extruct_gets_image_data_from_serious_eats():
    url = "https://www.seriouseats.com/peanut-butter-jelly-sandwich-cookie-recipe"
    response = httpx.get(url)
    data = extruct.extract(response.content, syntaxes=["json-ld", "microdata"])
    pprint(data)


see_if_extruct_gets_image_data_from_serious_eats()
