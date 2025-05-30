# парсинг с сайта
import requests
from bs4 import BeautifulSoup

HOST = "https://menunedeli.ru/"
URL = 'https://menunedeli.ru/podborki-receptov/bystrye-recepty/'

HEADERS = {'accept': '*/*', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


# в функции содержится предобработка ингредиентов
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('article', class_='post-card-in-lst row no-gutters')
    recipes = []
    for item in items:
        recipes.append({
            'Название': item.find('h5', class_='hdr').get_text(),
            'Ингредиенты': item.find('ul', class_='ingredients-lst').get_text()
        })
    for el in recipes:
        new_lst = el["Ингредиенты"].strip().split('\n')
        del el["Ингредиенты"]
        result = [i.split('–')[0].strip() for i in new_lst]
        result_ = set(result)
        el['Ингредиенты'] = result_
    return recipes


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
    

user_input = input("Введите имеющиеся у вас ингредиенты (через запятую): ").strip()
user_ingredients = set()
for item in user_input.split(','):
    user_ingredients.add(item.strip().capitalize())


recipes_all_ingredients, possible_recipes_with_missing, missing_for_other = find_possible_recipes(user_ingredients, recipes_site)


if recipes_all_ingredients:
    print("\nВам не нужны дополнительные ингредиенты. Вы cможете приготовить следующее блюдо:")
    for recipe in recipes_all_ingredients:
        print(f"- {recipe['Название']}")
        extra_ingredients = set(user_ingredients) - recipe["Ингредиенты"]
        if extra_ingredients:
            print(f"- Лишние ингредиенты из вашего списка: {', '.join(extra_ingredients)}")
elif possible_recipes_with_missing:
    print("\nВам нужны дополнительные ингредиенты. Добавив их, вы можете приготовить следующие блюда:")
    for recipe in possible_recipes_with_missing:
        print(f"{recipe['Название']}")
        info = missing_for_other.get(recipe['Название'])
        extra_ingredients = set(user_ingredients) - recipe["Ингредиенты"]
        if extra_ingredients:
            print(f"- Лишние ингредиенты из вашего списка: {', '.join(extra_ingredients)}")
        if info:
            print(f"- Недостающие ингредиенты: {', '.join(info['Недостающее'])}")
else:
    print("К сожалению, по вашим ингредиентам не найдено подходящих рецептов.")



