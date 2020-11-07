from http.server import HTTPServer, SimpleHTTPRequestHandler
from pprint import pprint

from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas as pd

wine_excel = pd.read_excel('wine2.xlsx', sheet_name='Лист1')

dict_wine = wine_excel.to_dict(orient='record')

white_wine = []
red_wine = []
beverages = []
sored_wines = {}

for wine in dict_wine:
    cat_vino = wine['Категория']
    if cat_vino == 'Белые вина':
        white_wine.append(wine)
        sored_wines[cat_vino] = white_wine
    elif cat_vino == 'Красные вина':
        red_wine.append(wine)
        sored_wines[cat_vino] = red_wine
    elif cat_vino == 'Напитки':
        beverages.append(wine)
        sored_wines[cat_vino] = beverages

pprint(sored_wines)

years_now = datetime.datetime.now()
years_start = 1920

EARS_JOB = years_now.year - years_start

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

rendered_page = template.render(
    age=EARS_JOB,
    wines=dict_wine,

)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)
server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()