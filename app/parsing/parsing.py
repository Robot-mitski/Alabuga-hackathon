from flask import Blueprint
import requests
from bs4 import BeautifulSoup

module = Blueprint("parsing", __name__)

def parse_text(url: str):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, "html.parser")
    txt = ""
    for i in soup.find_all("p", class_="topic-body__content-text"):
        txt += f" {i.text}"
    txt.lstrip()
    return txt

def parse_urls_txts(req):
    resp = requests.get(f"https://m.lenta.ru/search?query={req}#size=10%7Csort=2%7Cdomain=1%7Cmodified,format=yyyy-MM-dd")
    soup = BeautifulSoup(resp.content, "html.parser")
    search = soup.find_all(class_="card-search")[:10]
    txts = []
    for i in search:
        txts.append(parse_text("https://m.lenta.ru/"+i["href"]))
    return txts

    