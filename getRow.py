import requests
from bs4 import BeautifulSoup

# 페이지 네비게이션을 이용해서 마지막 페이지 number을 가져오는 함수
def getMaxPage(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    last_page_tag = soup.find_all("td", {"class": "pgRR"})[0].find('a')

    link = last_page_tag["href"]

    return int(link[-2:]) #반환 값 마지막 페이지 number

#한페이지 안 table의 각 row를 list 형태로 반환
def getRowList(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    table = soup.find_all("div", {"class": "box_type_l"})[0].find("table")

    row_list = table.findAll("tr", {"onmouseover": True})

    return row_list

#모든 종목을 가져오는 함수
def getAllRow(url):
    max_page = getMaxPage(url)
    column_list = [] #모든 column을 저장할 리스트

    for page in range(1, max_page+1): #url에 페이지 번호를 순서대로 넣는 반복문
        url = f"https://finance.naver.com/sise/sise_market_sum.naver?&page={page}"
        column_list.extend(getRowList(url=url)) #getRowlist 함수에서 가져온 리스트를 column_list에 추가함

    return column_list