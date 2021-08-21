import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from pandas.io.json import json_normalize
import re

def scraper(url):
    df_houses = pd.DataFrame(columns = ["title", "price", "location"])
    pages_limit = False
    for i in range(1, 500):
        print(str(i))
        if pages_limit == False:
            response = requests.get(url + str(i))
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            all_houses = soup.find_all("div", {"class": "ann-box-details"})
            if len(all_houses) != 0:
                print(len(all_houses))
                for house in all_houses:
                    title = re.findall(r'(?<=title\=\")(.*?)(?=\")', str(house))
                    price = re.findall(r'(?<=class\=\"ann\-price\"\>)(.*?)(?=<)', str(house))
                    location = re.findall(r'(?<=pin\"\>\<\/span>)(.*?)(?=<\/span)', str(house))
                    df_houses = df_houses.append({"title": title, "price": price, "location": location}, ignore_index=True)
            else:
                pages_limit = True
        else:
            return df_houses
    return df_houses

houses_on_sale = scraper("https://www.encuentra24.com/el-salvador-es/bienes-raices-venta-de-propiedades-casas.")
apartments_on_sale = scraper("https://www.encuentra24.com/el-salvador-es/bienes-raices-venta-de-propiedades-apartamentos.")
apartments_on_lease = scraper("https://www.encuentra24.com/el-salvador-es/bienes-raices-alquiler-apartamentos.")
houses_on_lease = scraper("https://www.encuentra24.com/el-salvador-es/bienes-raices-alquiler-casas.")

