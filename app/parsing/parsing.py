from flask import Blueprint
import requests
from bs4 import BeautifulSoup

module = Blueprint("parsing", __name__)

def parse_text(url: str):
    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, "html.parser")
        txt = ""
        for i in soup.find_all("p", class_="topic-body__content-text"):
            txt += f" {i.text}"
        txt.lstrip()
        return txt
    except Exception as ex:
        print(ex)
        return ""

    