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

# import requests
# from bs4 import BeautifulSoup
# import pandas as pd

# def get_isGood(url: str):
#     resp = requests.get(url)
#     soup = BeautifulSoup(resp.content, "html.parser")

#     text_lns = resp.text.splitlines()
#     for ln in text_lns:
#         if "isGood" in ln:
#             return(bool(ln.split(": ")[-1][:-1]))

# df = pd.read_csv("urls.csv")

# df["good"] = df["url"].apply(get_isGood)
# df.to_csv("sex.csv", index=False)

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

import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import time, sleep
from requests.adapters import HTTPAdapter, Retry

def get_companies_tags_pos(url):
    resp = requests.get(url)
    soup_ = BeautifulSoup(resp.content, "html.parser")
    tags_in_text = get_organizator_text(soup_)
    for i in tags_in_text:
        return get_tag_pos(soup_, i)

def get_isGood(soup):
    text_lns = str(soup).splitlines()
    for ln in text_lns:
        if "isGood" in ln:
            return(bool(ln.split(": ")[-1][:-1]))
        
def get_organizator(soup):
    links = soup.find("div", class_="topic-body__content")
    companies = []
    for ln in links.find_all("a"):
        link = str(ln["href"])
        if "tags/organizations" in str(ln["href"]):
            companies.append(link.split("/")[-2])
    return companies

def get_tag_pos(soup, tag):
    text = get_page_text(soup)
    from_ = text.find(tag)
    to = text.find(tag)+len(tag)-1
    return from_, to

def get_organizator_text(soup):
    links = soup.find("div", class_="topic-body__content")
    companies = []
    for ln in links.find_all("a"):
        link = ln["href"]
        if "tags/organizations" in link:
            companies.append(ln.text)
    return companies

def get_page_text(soup):
    txt = ""
    for i in soup.find_all("p", class_="topic-body__content-text"):
        txt += f" {i.text}"
    txt.lstrip()
    return txt

urls = pd.read_csv("urls.csv")
df = urls.head(5000)
df_out = pd.DataFrame(columns=["url", "tagfrom", "tagto", "organizator", "isgood"])

start = time()
for i, elem in df.itertuples(index=True):
    flag = False
    delay = 1
    while not flag:
        try:
            url = elem
            resp = requests.get(url)
            soup = BeautifulSoup(resp.content, "html.parser")
            orgs_text = get_organizator_text(soup)
            orgs = get_organizator(soup)
            isgood = get_isGood(soup)
            if not orgs: df_out.loc[df_out.shape[0]] = (url, None, None, None, isgood)
            for j in range(len(orgs)):
                pos = get_tag_pos(soup, orgs_text[j])
                df_out.loc[df_out.shape[0]] = (url, pos[0], pos[1], orgs[j], isgood)
            flag = True
            delay = 1
            print(url, "ok")
        except Exception as ex:
            print(ex)
            sleep(delay)
            if delay < 256:
                delay *= 2
            flag = False
end=time()
print(end-start)
df_out.to_csv("out.csv", index=False)

# df = pd.read_csv("urls.csv")

# df["good"] = df["url"].apply(get_isGood)
# df.to_csv("sex.csv", index=False)


# begin = time()
# df["tagpos"] = df["url"].apply(get_companies_tags_pos)
# df["organizator"] = df["url"].apply(get_organizator)
# end = time()
# df.to_csv("out.csv", index=False)
# print(end-begin)