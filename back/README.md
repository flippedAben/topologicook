# topologicook

## Alternatives

- [mealie](https://github.com/mealie-recipes/mealie)
- [tandoor](https://github.com/TandoorRecipes/recipes)

## Setup

- `uv`. Python package management.

## Pull from USDA

USDA provides a _Foundational Foods_ database, which is the one kept up to date. From their [documentation](https://fdc.nal.usda.gov/Foundation_Foods_Documentation.html):

> Foundation Foods does not provide data on all nutrients. This is because of the uniqueness of the data:
>
> - Some nutrients are not found in certain foods (e.g., cholesterol in plant foods, protein in oils).
> - Some nutrients in a food have not yet been analyzed. Data analyses are continually conducted and as data on nutrients are obtained, values will be added to food profiles.

Recommended nutrient intakes and limits: https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx

## Parse recipes from various sources

https://github.com/hhursev/recipe-scrapers/

## Normalize recipe data

TODO

## Map ingredients to foods (FDC IDs)

Given some ingredient name in a recipe (i.e. sliced apples), I want to map it to an item in the USDA database.
I experiement with different methods, see which ones work the best (TODO how do i measure).

- Accuracy. How to measure this?
- Speed

Some ideas:

- Text similiarty
  - Models I can use here, enumerated by [HuggingFace](https://huggingface.co/spaces/mteb/leaderboard).
  - Article with ideas to consider: https://www.newscatcherapi.com/blog/ultimate-guide-to-text-similarity-with-python
  - Fuzzy search: https://dev.to/miguelsmuller/comparing-text-similarity-measurement-methods-sentence-transformers-vs-fuzzy-og3
- LLM with prompting

## Calculate nutrition of the recipe

TODO
