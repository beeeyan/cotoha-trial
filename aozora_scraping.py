# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup

def get_aocora_sentence(aozora_url):
    res = requests.get(aozora_url)
    # BeautifulSoupの初期化
    soup = BeautifulSoup(res.content, 'lxml')
    # 青空文庫のメインテキストの取得
    main_text = soup.find("div", class_="main_text")
    # ルビの排除
    for script in main_text(["rp","rt","h4"]):
        script.decompose()
    sentences = [line.strip() for line in main_text.text.splitlines()]
    sentences = [line for line in sentences if line != '']
    return sentences
