import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from pandas.io.json import json_normalize
import re

df_houses = pd.DataFrame(columns = ["title", "price", "location"])
pages_limit = False
for i in range(1, 102):
    print(str(i))
    if pages_limit == False:
        response = requests.get(f'https://www.encuentra24.com/el-salvador-es/bienes-raices-venta-de-propiedades-casas.{i}')
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        if len(soup) != 0:
            pages_limit = False
            all_houses = soup.find_all("div", {"class": "ann-box-details"})
            for house in all_houses:
                title = re.findall(r'(?<=title\=\")(.*?)(?=\")', str(house))
                price = re.findall(r'(?<=class\=\"ann\-price\"\>)(.*?)(?=<)', str(house))
                location = re.findall(r'(?<=pin\"\>\<\/span>)(.*?)(?=<\/span)', str(house))
                df_houses = df_houses.append({"title": title, "price": price, "location": location}, ignore_index=True)
        else:
            pages_limit = True
    else:
        break
df_houses.to_csv("venta_casas.csv")
