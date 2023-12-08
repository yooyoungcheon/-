from bs4 import BeautifulSoup
import requests

def crawling(url_temp):
    data_list = []
    for i in range(4):
        url = url_temp.format(i+1)
        response = requests.get(url)

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        tr_elements = soup.find(id='contentarea').find_all('tr')

        for tr in tr_elements:
            td_elements = tr.find_all(class_='tltle')
            number = tr.find_all('td',class_='number')
            row_data = []
    
  
            for td in td_elements:
                row_data.append(td.get_text(strip=True))
    
            for num in number:
                row_data.append(num.get_text(strip=True))

            if row_data:
                data_list.append(row_data)
    return data_list

url = 'https://finance.naver.com/sise/sise_market_sum.naver?&page={}'
temp = crawling(url)
for row in temp:
     print(row)