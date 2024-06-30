#1
# import joblib
# loaded_model = joblib.load('model/model.pkl') # сохраненная модель
 
# new_data = [[5.1, 3.5, 10, 1.0, 0.77, 3.555]]  # Пример новых данных
# prediction = loaded_model.predict(new_data)
# print(prediction)

# 2
# import requests
# from bs4 import BeautifulSoup

# url = "https://lenta.ru/news/2024/06/29/windows10/"
# resp = requests.get(url)
# soup = BeautifulSoup(resp.content, "html.parser")
# links = soup.find("div", class_="topic-body__content")
# companies = []
# for ln in links.find_all("a"):
#     link = str(ln["href"])
#     if "tags/organizations" in str(ln["href"]):
#         companies.append(ln.text)
# print(companies)

# 3
# import requests
# from bs4 import BeautifulSoup



# 4
# import requests
# from bs4 import BeautifulSoup
# import pandas as pd

# url = "https://lenta.ru/news/2024/06/28/krupneyshie/"
# resp = requests.get(url)
# soup = BeautifulSoup(resp.content, "html.parser")
# links = soup.find("div", class_="topic-body__content")
# companies = []
# for ln in links.find_all("a"):
#     link = str(ln["href"])
#     if "tags/organizations" in str(ln["href"]):
#         companies.append(ln.text)
# txt = ""
# for i in soup.find_all("p", class_="topic-body__content-text"):
#     txt += f" {i.text}"
# txt = txt[1:]

# df['new'] = df['old'].apply(def)
# def add_companies():


# urls = pd.read_csv("urls.csv")





# table = pd.DataFrame(columns=["url", "company", "from", "to"])
# for row in urls:
#     table.

import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_isGood(url: str):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, "html.parser")

    text_lns = resp.text.splitlines()
    for ln in text_lns:
        if "isGood" in ln:
            return(bool(ln.split(": ")[-1][:-1]))

df = pd.read_csv("urls.csv")

df["good"] = df["url"].apply(get_isGood)
df.to_csv("sex.csv", index=False)

def get_organizator(url: str):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, "html.parser")
    links = soup.find("div", class_="topic-body__content")
    companies = []
    for ln in links.find_all("a"):
        link = str(ln["href"])
        if "tags/organizations" in str(ln["href"]):
            companies.append(link.split("/")[-2])
    return companies
