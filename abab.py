import requests
from bs4 import BeautifulSoup
import csv

# 종목 코드 입력 받기
stock_code = input("종목 코드를 입력하세요: ")

# 종목명 입력 받기
stock_name = input("종목명을 입력하세요: ")

# 크롤링할 주소 설정 (네이버 증권 일별시세 페이지)
url = f"http://finance.naver.com/item/sise_day.nhn?code={stock_code}"    
# https://finance.naver.com/item/sise_day.naver?code=005930&page=1,2,3,4,5 

# User-agent 헤더 설정 (브라우저처럼 보이도록 함)
headers = {'User-agent': 'Mozilla/5.0'}

# 페이지 수 설정 25= 1년치 
pagescount = 25


stock_data = [] # 일별시세 데이터를 저장하는 리스트 

for page in range(1, pagescount + 1):
    
    page_url = f"{url}&page={page}" # 페이지 URL 조합

    
    response = requests.get(page_url, headers=headers) # 페이지 내용을 가져옴 User-agent 

    # 페이지 파싱
    html = BeautifulSoup(response.text, "lxml")

    # 시세 데이터 테이블 찾기
    table = html.find("table", {"class": "type2"})

    if table:
        # 테이블에서 데이터 추출
        rows = table.find_all("tr")[1:]  # 첫번쨰 행은 헤더니까 1부터 시작
        #rows=열  

        for row in rows:                             
            columns = row.find_all("td")
            
            # 종가 데이터가 있는지 확인
            if len(columns) > 1:
                date = columns[0].text.strip()  # 날짜
                closing_price = columns[1].text.strip()  # 종가
                

                # 추출한 데이터를 리스트에 추가
                stock_data.append((date, closing_price))

# CSV 파일로 저장
csv_file_name = f"{stock_name}_stock_data.csv"

with open(csv_file_name, "w", newline="", encoding="utf-8") as csvfile:
    csv_writer = csv.writer(csvfile)
    # CSV 파일에 헤더를 추가 (종목명, 날짜, 종가)
    csv_writer.writerow(["종목코드","종목명", "날짜", "종가"])
    # 시세 데이터를 CSV 파일에 쓰기
    for date, closing_price in stock_data:
        csv_writer.writerow([stock_code,stock_name, date, closing_price])

print(f"{csv_file_name} 파일로 데이터를 저장했습니다.")
