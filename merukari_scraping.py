from selenium import webdriver
from time import sleep
import numpy as np
driver = webdriver.Chrome(r'C:\Users\okefu\merukari_scraping\chromedriver')
driver.maximize_window()
judge = input("keywordをいくつ入力しますか")
keywords = []
num = 0
while num < int(judge):
    keyword = input("keywordを入力してください")
    keywords.append(keyword)
    num += 1
keywords = "+".join(keywords)
get_price = input("求める値段を入力してください")
get_price = int(get_price)
url = "https://www.mercari.com/jp/search/?keyword=" + keywords
driver.get(url)
i = 0
prices = []
sold_prices = []
links = []
while True:
    i = i + 1
    sleep(1)
    posts = driver.find_elements_by_class_name("items-box")
    for post in posts:
        if (len(post.find_elements_by_class_name("item-sold-out-badge")) > 0):
            price = post.find_element_by_class_name("items-box-price").text
            price = price.replace('¥', '').replace(',', '')
            price = int(price)
            sold_prices.append(price)
            continue
        link = post.find_element_by_css_selector("a")
        link = link.get_attribute("href")
        links.append(link)
        price = post.find_element_by_class_name("items-box-price").text
        price = price.replace('¥', '').replace(',', '')
        price = int(price)
        prices.append(price)
    next_link = driver.find_elements_by_xpath("//ul[@class='pager']//li[@class='pager-next visible-pc']//a")
    driver.get(next_link[0].get_attribute("href"))
    if i > 4:
        break
dic = {key: val for key, val in zip(links, prices)}
q75, q25 = np.percentile(sold_prices, [75 ,25])
q25 = int(q25)
print(q25)
dic = {k: v for k, v in dic.items() if q25 <= v <= get_price}
dic_sorted = sorted(dic.items(), key=lambda x:x[1], reverse=True)
print(dic_sorted)
# keys = [k for k, v in dic.items() if q25 <= v <= get_price]
# print(keys)
