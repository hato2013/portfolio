from selenium import webdriver
from time import sleep
import numpy as np
import csv
import os
import pandas as pd
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
tag = "none"
products = []
earnings = []
fees = []
deliverys = []
profits = []
dates = []
ids = []
blank = []
#tagによって場合分けして特定のリストに加える
def case_tag(text):
    global tag
    global products
    global earnings
    global fees
    global deliverys
    global profits
    global dates
    global ids
    if tag == "fee":
        text = text.replace("¥", "").replace(",","")
        fees.append(int(text))
    if tag == "delivery":
        text = text.replace("¥", "").replace(",","")
        deliverys.append(int(text))
    if tag == "profit":
        text = text.replace("¥", "").replace(",","")
        profits.append(int(text))
    if tag == "date":
        dates.append(text)
    if tag == "id":
        ids.append(text)
    if tag == "product":
        split_list = text.splitlines()
        products.append(split_list[0])
        text = split_list[1].replace("¥", "").replace(",","")
        earnings.append(int(text))
    tag = "none"
#場合分けでtagをつける
def make_tag(text):
    global tag
    if text == "商品":
        tag = "product"
    if text == "販売手数料":
        tag = "fee"
    if text == "配送料":
        tag = "delivery"
    if text == "販売利益":
        tag = "profit"
    if text == "購入日時":
        tag = "date"
    if text == "商品ID":
        tag = "id"
#listの足し算
def python_list_add(in1, in2):
    wrk = np.array(in1, dtype=object) + np.array(in2, dtype=object)
    return wrk.tolist()
#cromeを開く
driver = webdriver.Chrome(r'C:\Users\okefu\merukari_work\chromedriver')
driver.maximize_window()
#メルカリを開く
driver.get('https://www.mercari.com/jp/mypage/')
os.system('PAUSE')
#売上履歴のページまで行く
element = driver.find_element_by_link_text("売上・振込申請")
element.click()
element = driver.find_element_by_link_text("売上履歴")
element.click()
#それぞれの商品のページから商品情報を回収する
elem_a = driver.find_elements_by_xpath('/html/body/div[1]/main/div[1]/section/ul/li/a')
for i in range(len(elem_a)):
    elem_a = driver.find_elements_by_xpath('/html/body/div[1]/main/div[1]/section/ul/li/a')
    elem_a[i].click()
    for info in driver.find_elements_by_class_name('transact-info-table-cell'):
        print(info.text)
        #tagで判断
        case_tag(info.text)
        #tagをつける
        make_tag(info.text)
    #配送料がなかった場合0を入れる
    if len(deliverys) != len(products):
        deliverys.append(0)
    blank.append("")
    driver.back()
#feesとdeliverysをたしたlist,mfを作る
mf = python_list_add(fees, deliverys)
#作ったlistを使ってdataframeを作る
df = pd.DataFrame({'日付': dates,
                   'メルカリ商品ID': ids,
                   'タイトル': products,
                   '売上': earnings,
                   '手数料': fees,
                   '送料（メルカリ便）': deliverys,
                   'MF転記手数料総額': mf,
                   '送料（出品者負担）': blank,
                   '入金': profits})
#dfのtypeをobject型にする
df = df.astype(({"売上": object}))
df = df.astype(({"手数料": object}))
df = df.astype(({"送料（メルカリ便）": object}))
df = df.astype(({"MF転記手数料総額": object}))
df = df.astype(({"入金": object}))

#2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

#認証情報設定
#ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
#ここに自分の取得したjsonファイルを入力する(change_point)
credentials = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\okefu\Downloads\shining-relic-307314-ef4ad4a33ab7.json', scope)

#OAuth2の資格情報を使用してGoogle APIにログインします。
gc = gspread.authorize(credentials)

#共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。(change_point)
SPREADSHEET_KEY = '1hT6pS7Yp8p346KyX2yFxcXzgL5PqjWH9qBY_8P02SAw'

#共有設定したスプレッドシートのワークシート1を開く
worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1
# 数字からアルファベットを返す関数
# 例：26→Z、27→AA、10000→NTP
def toAlpha(num):
    if num<=26:
        return chr(64+num)
    elif num%26==0:
        return toAlpha(num//26-1)+chr(90)
    else:
        return toAlpha(num//26)+chr(64+num%26)

col_lastnum = len(df.columns) # DataFrameの列数
row_lastnum = len(df.index)   # DataFrameの行数
#cell_listを作りそれぞれ代入する
cell_list = worksheet.range('A1:'+toAlpha(col_lastnum)+str(row_lastnum+1))
for cell in cell_list:
    if cell.row == 1:
        val = df.columns[cell.col-1]
    else:
        val = df.iloc[cell.row-2][cell.col-1]
    cell.value = val
worksheet.update_cells(cell_list)
