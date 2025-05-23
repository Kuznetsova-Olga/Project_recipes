import requests
from bs4 import BeautifulSoup
HOST = "https://menunedeli.ru/"
URL = 'https://menunedeli.ru/podborki-receptov/bystrye-recepty/'
HEADERS = {'accept' : '*/*', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'}
def get_html(url, params=''):
  r = requests.get(url, headers=HEADERS, params=params)
  return r
def get_content(html):
  soup = BeautifulSoup(html, 'html.parser')
  items = soup.find_all('article', class_='post-card-in-lst row no-gutters')
  recipes = []
  for item in items:
    recipes.append({
        'Название': item.find('h5', class_='hdr').get_text(),
        'Ссылка на рецепт': HOST + item.find('h5', class_='hdr').find('a').get('href'),
        'Ингредиенты': item.find('ul', class_='ingredients-lst').get_text()
    })
  return recipes
html = get_html(URL)
recipes_site = get_content(html.text)
print(recipes_site)
