def find_possible_recipes(user_ingredients, recipes_site):
    recipes_all_ingredients = []
    possible_recipes_with_missing = []
    missing_for_other = {}
    for recipe in recipes_site:
        needed = recipe["Ингредиенты"]
        available = set(user_ingredients)
        possible_recipe = needed.intersection(available)
        if possible_recipe == needed:
            recipes_all_ingredients.append(recipe)
        elif len(possible_recipe) >= 3:
            possible_recipes_with_missing.append(recipe)
            missing_ingredients = needed - available
            missing_for_other[recipe["Название"]] = {"Недостающее": missing_ingredients}
    return recipes_all_ingredients, possible_recipes_with_missing, missing_for_other


# получение списка со всеми рецептами (один словарь - один рецепт)
html = get_html(URL)
recipes_site = get_content(html.text)
for i in recipes_site:
    print(i["Ингредиенты"])


