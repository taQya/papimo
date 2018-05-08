#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from datetime import datetime
import lxml.html
import requests
import time

BASE_URL = "https://papimo.jp"
SLEEP_TIME = 1 # 連アタしないように上手いこと調整して

# 1:今日のデータ 2:昨日のデータ
# 12時を越えたら昨日のデータ扱いになる
DAY_CODE = 1

# カラム数が少ない機種
SARABAN_NAME = "押忍!サラリーマン番長"
SARABAN = [5,10]

# papimoのデータ取ります
class Papimo:

    def get_response(self, url):
        """
        レスポンス情報の取得
        """
        session = requests.Session()
        response = session.get(BASE_URL + url)
        time.sleep(SLEEP_TIME)
        return response

    def get_machine_link(self, url):
        """
        機種データを取得
        """

        print "----------- 機種データを取得しています"
        index_links = []
        i = 1

        # 機種情報をページURLをあるだけ取得する
        while True:
            print url + "?page=" + str(i)
            response = self.get_response(url + "?page=" + str(i))
            if response.status_code <> 200:
                break;

            soup = BeautifulSoup(response.text, "lxml")
            for link in soup.find("ul", class_="item").find_all("a"):
                index_links.append(link.get("href"))

            i+=1
        print "----------- 機種データの取得が終了しました 設置機種:" + str(len(index_links)) + "機種"
        return index_links

    def get_number_links(self, url):
        """
        全台番号取得
        """
        index_links = self.get_machine_link(url)
        number_links = []
        # print "全機種数:" + str(len(index_links))

        amount = len(index_links)

        for index_link in index_links:
            response = self.get_response(index_link)
            soup = BeautifulSoup(response.text, "lxml")
            for machine in soup.find("ul", class_="sort").find_all("a"):
                number_links.append(machine.get("href"))
                print machine.get("href")

        return number_links

    def get_machine_info(self, url):
        """
        台情報を取得する
        param:
            url: URL (str)
        return
            data :
                - 機種名
                - 台番号
                - day
                - BB回数
                - RB回数
                - ART回数
                - ＢＢ確率
                - 合成確率
                - 総スタート
                - ARTゲーム数
                - 最終スタート
                - 最大出メダル
                - リンク
        """

        response = self.get_response(url)
        soup = BeautifulSoup(response.text, "lxml")

        # 台情報の取得
        rack_info = soup.find("div", class_="nav-panel")

        # 本日のデータ
        tr = rack_info.find_all("tr")
        data = []
        name = soup.find("p", class_="name").text
        no = soup.find("p", class_="unit_no").text
        data.append(name)
        data.append(no)
        yyyymmdd = datetime.now().strftime("%Y/%m/%d")
        for td in tr[DAY_CODE].find_all("td"):
            t = td.text
            # 特殊データ対応
            if name.encode('utf-8') == SARABAN_NAME and len(data) + 1 in SARABAN:
                data.append('-')
            # 日付変換
            if t in u'本日' :
                t = str(yyyymmdd)
            data.append(t)

        # このデータのリンク
        data.append(BASE_URL + url)

        return data
