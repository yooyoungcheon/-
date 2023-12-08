import requests
from bs4 import BeautifulSoup

def get_code(URL):
    code_list = []
    url = f'{URL}'
    response = requests.get(url)
    # 페이지 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # a_tags = soup.find_all('a', class_='tltle')  # class가 'tltle'인 <a> 태그들을 선택
    tr_elements = soup.find(id='contentarea').find_all('tr')
    for tr in tr_elements:
        td_elements = tr.find_all('a',class_='tltle')
        for a_tag in td_elements:
            href = a_tag.get('href')
            code_list.append(href)
    
    return code_list

def get_stock_data(code_list):
    stock_list = []
    for code in code_list:

        # 종목 페이지 URL 생성
        url = f'https://finance.naver.com{code}'
    
        # HTTP GET 요청
        response = requests.get(url)
    
        # 페이지 파싱
        soup = BeautifulSoup(response.text, 'html.parser')
    
        # 종목이름 추출
        stock_data=[]
        company_name = soup.find('div', {'class': 'wrap_company'}).find('a').text
        stock_data.append(company_name)

        # 주식 데이터 표에서 날짜 크롤링
        tmp_1 = soup.find('div', {'class': 'content_wrap'}).find('table',{'class' :'tb_type1 tb_num tb_type1_ifrs'})
        tmp_2 = tmp_1.find('thead').find_all('tr')

        date = tmp_2[1]
        been = [column.get_text(strip=True) for column in date if column.get_text(strip=True)] # 빈 문자열 제거
        for i in been:
            if i:
                stock_data.append(i)

        # 주식 이름과 표의 날짜를 한 줄로 합친 후 리스트에 저장
        if stock_data:
            stock_list.append(stock_data)   
    
        # 표에서 각 데이터 크롤링
        tmp_3 = soup.find('div', {'class': 'content_wrap'}).find('table',{'class' :'tb_type1 tb_num tb_type1_ifrs'})
        tmp_4 = tmp_3.find('tbody').find_all('tr')


        # 원하는 정보를 찾아 해당 인덱스로 데이터 가져올수있음
        # 0:매출액 1:영업이익 2:당기순이익 3:영업이익률 4:순이익률 5:ROE 6:부채비율 7:당좌비율
        # 8: 유보율 9:EPS 10:PER 11:BPS 12:PBR 13:주당배당금 14:시가배당률 15:배당성향 
        temp_2=[]
        data = tmp_4[0] # 매출액
        qwe = [column.get_text(strip=True) for column in data if column.get_text(strip=True)] # 빈 문자열 제거
        for i in qwe:
            if i:
                temp_2.append(i)

        if temp_2:
            stock_list.append(temp_2)   
        
    return stock_list

stock_code = get_code('https://finance.naver.com/sise/sise_market_sum.naver')
stock_list = get_stock_data(stock_code)

for stock in stock_list:
    print(stock)
