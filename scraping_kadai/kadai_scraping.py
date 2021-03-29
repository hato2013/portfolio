from selenium import webdriver
import numpy as np
import pandas as pd
#chromedriverを読み込む
driver = webdriver.Chrome(r'C:\Users\okefu\merukari_scraping\chromedriver')
driver.maximize_window()
#サイトを読み込む
driver.get('https://ai-products.net/')
#forループのスクレイピング
for i in range(29):
    #pageを1~29の間で回す
    page = str(i+1)
    #[シート・収集したい項目[サービス・技術]のカテゴリを選択する
    try:
        element = driver.find_element_by_xpath('//*[@id="primary"]/div[2]/section[3]/div[2]/ul/li['+page+']/a')
    except NoSuchElementException:
        continue
    #カテゴリの名前を取得しておく
    category = element.text
    #そのカテゴリのページに移動する
    url = element.get_attribute('href')
    driver.get(url)
    #サービス名をlistに入れる
    service_names = []
    for service_name in driver.find_elements_by_class_name('service'):
        service_names.append(service_name.text)
    #説明をリストに入れる
    service_catches = []
    for service_catch in driver.find_elements_by_class_name('serviceCatch'):
        service_catches.append(service_catch.text)
    #利用料金をリストに入れる
    costs = []
    for cost in driver.find_elements_by_xpath('//dl[@class="cost"]/dd'):
        costs.append(cost.text)
    #初期費用をリストに入れる
    initial_costs = []
    for initial_cost in driver.find_elements_by_xpath('//dl[@class="initial-cost"]/dd'):
        initial_costs.append(initial_cost.text)
    #無料プランをリストに入れる
    free_plans = []
    for free_plan in driver.find_elements_by_xpath('//dl[@class="free-plan"]/dd'):
        free_plans.append(free_plan.text)
    #無料トライアルをリストに入れる
    free_trials = []
    for free_trial in driver.find_elements_by_xpath('//dl[@class="free-trial"]/dd'):
        free_trials.append(free_trial.text)
    #service_namesに入ったいらない要素を全部取り除く
    while True:
        try:
            service_names.remove('')
        except ValueError:
            break
    #dataframe化する
    df = pd.DataFrame({'サービス名': service_names,
                   '説明': service_catches,
                   '利用料金': costs,
                   '初期費用': initial_costs,
                   '無料プラン': free_plans,
                   '無料トライアル': free_trials})
    #dataframeをcsvに変換する
    df.to_csv(category+'.csv', encoding='utf_8_sig')
    #元のページに戻る
    driver.back()