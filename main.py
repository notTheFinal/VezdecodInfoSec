from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

# Опции для браузера
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
options = webdriver.ChromeOptions()
# options.headless = True
options.add_argument(f'user-agent={user_agent}')
options.add_argument("--window-size=1920,1080")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome('chromedriver', options=options)

# name = "Александр"
# surname = "Чумилин"
# town = "Иркутск"
nick1 = "turboshurrik"
nick2 = "MCShurrik"
# page = 3
page = 2
YSearchResponse = ""

# driver.get(f'https://www.google.com/search?q="{surname}+{name}"+-Анатольевич+-Смолин+-ИП+-news') - 20 point
driver.get(f'https://www.google.com/search?q="{nick1}"')
time.sleep(3)
firstSearchResponse = driver.page_source

# driver.get(f'https://www.google.com/search?q="{name}+{surname}"+-Анатольевич+-Смолин+-ИП+-news') - 20 point
driver.get(f'https://www.google.com/search?q="{nick2}"')
time.sleep(3)
secondSearchResponse = driver.page_source

# driver.get(f'https://www.google.com/search?q="{surname}+{town}"+-Анатольевич+-Смолин+-ИП+-news') - 20 point
# time.sleep(3)
# thirdSearchResponse = driver.page_source

for i in range(page):
    driver.get(f'https://yandex.ru/search/?text="{nick1}"&lr=63&clid=2380813&p={i}&cee=1')
    time.sleep(3)
    YSearchResponse += driver.page_source

for i in range(page):
    driver.get(f'https://yandex.ru/search/?text="{nick2}"&lr=63&clid=2380813&p={i}&cee=1')
    time.sleep(3)
    YSearchResponse += driver.page_source


driver.quit()

links = []

firstSearchSoup = BeautifulSoup(firstSearchResponse, 'html.parser')
secondSearchSoup = BeautifulSoup(secondSearchResponse, 'html.parser')
# thirdSearchSoup = BeautifulSoup(thirdSearchResponse, 'html.parser') - 20 point
YSearchSoup = BeautifulSoup(YSearchResponse, 'html.parser')

firstSearch = firstSearchSoup.find( id="search" )
for link in firstSearch.find_all('a'):
    links.append(link.get('href'))

secondSearch = secondSearchSoup.find(id="search")
for link in secondSearch.find_all('a'):
    links.append(link.get('href'))

# thirdSearch = thirdSearchSoup.find(id="search") - 20 point
# for link in thirdSearch.find_all('a'):
#     links.append(link.get('href'))

YSearch = YSearchSoup.find_all("div", {"class": "main serp i-bem"})
for link in YSearch[0].find_all('a'):
    links.append(link.get('href'))

links = set(links)
for link in links:
    if link and "." in link and not "webcache" in link and not "ru/images" in link:
        print(link)


# После первой проверки в гугле прокликиваем все ссылки, находим лишние фамилии и отчества. Добавляем в запрос "-Анатольевич", а также "-Смолин"

# найденные профили
# https://leader-id.ru/users/1420357
# https://www.istu.edu/ob_irnitu/person/chumilin_aleksandr_vladimirovich
# https://bigrank.net/ispolniteli/71322/
# http://sismp3.narod.ru/about.htm
# https://vk.com/id188805813 (этот профиль не напрямую, а через https://list-vk.com/188805813/#photos)
# https://www.fl.ru/users/turboshurrik/portfolio/#/

# Найденые профили после второй проверки по никнеймам
# https://www.istu.edu/ob_irnitu/person/chumilin_aleksandr_vladimirovich
# http://sismp3.narod.ru/about.htm
# https://freelancehunt.com/freelancer/turboshurrik.html
# https://www.fl.ru/users/turboshurrik/portfolio/#/
# vk.com/id188805813
# https://rostravel.ru/user/188805813/
# https://www.weblancer.net/users/turboshurrik/
# https://www.pinterest.ru/turboshurrik/
# https://ctftime.org/user/95502
# http://turboshurrik.blogspot.com

