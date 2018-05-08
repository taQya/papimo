#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
from datetime import datetime
import os
import time
import Papimo
from config import SHOP_NAME, SHOP_CODE, S5_CODE, S20_CODE
# ロガー設定
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)

VIEW_PATH = "/h/" + SHOP_CODE + "/hit/view/"
MACHINE_PATH = "/hit/index_machine/"
OUTPUT_DIR = os.getcwd() + "/output/"
URL_S5 = "/h/" + SHOP_CODE + MACHINE_PATH + "1-5-" + S5_CODE
URL_S20 = "/h/" + SHOP_CODE + MACHINE_PATH + "1-20-" + S20_CODE

header_column =[
                "機種名",
                "台番号",
                "日付",
                "BB回数",
                "RB回数",
                "ART回数",
                "ＢＢ確率",
                "合成確率",
                "総スタート",
                "ARTゲーム数",
                "最終スタート",
                "最大出メダル",
                "リンク"
                ]

def output(data_list):
    # ヘッダ
    header = ""
    for h in header_column:
        header += '\"' + h + '\"' + '\t'
    header += '\n'

    # ファイル名
    yyyymmdd = datetime.now().strftime("%Y%m%d")
    output = OUTPUT_DIR + yyyymmdd + "_data_" + SHOP_NAME + ".csv2"
    logger.info(output + " に出力します。")

    # 出力
    with open(output, "w") as f:
        f.write(header)
        for data in data_list:
            for d in data:
                f.write('\"' + d.encode("utf-8") + '\"')
                f.write('\t')
            f.write('\n')


def main():
    start = time.time()
    logger.info("台データを取得しています")

    # papimo
    pa = Papimo.Papimo()

    # 全台番号を取得
    #s20 = pa.get_number_links(URL_S5)
    s20 = pa.get_number_links(URL_S20)

    sorce_list = _sort(s20)

    #print "5スロ台数:" + str(len(s5))
    print "20スロ台数:" + str(len(s20))

    data_list = []

    for s in sorce_list:
        data = pa.get_machine_info(s)
        data_list.append(data)

    output(data_list)

    # 終了処理
    elapsed_time = time.time() - start
    logger.info("処理時間: {} [sec]".format(round(elapsed_time, 1)))
    logger.info("終了しました")

def _sort(list):
    numbers = []
    for s in list:
        numbers.append(s.replace(VIEW_PATH, ""))

    numbers.sort(key = int)

    sorted_list =[]
    for n in numbers:
        sorted_list.append(VIEW_PATH + str(n))

    return sorted_list

#single view
TEST_SINGLE = '/h/00031715/hit/view/600'
def debug():
    pa = Papimo.Papimo()
    res = pa.get_machine_info(TEST_SINGLE)
    data_list = [res]
    output(data_list)

if __name__ == '__main__':
    main()
