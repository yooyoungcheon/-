import requests
from bs4 import BeautifulSoup

def get_stock_data(stock_code):
    url = f"https://finance.naver.com/item/sise_day.nhn?code={stock_code}"
    
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        data_list = []
        table = soup.find("table", class_="type2")
        rows = table.find_all("tr")
        
        for row in rows[1:]:  # Skip the header row
            columns = row.find_all("td")
            
            date = columns[0].text
            volume = columns[1].text
            start_price = columns[3].text
            high_price = columns[4].text
            low_price = columns[5].text
            
            data_list.append({
                "Date": date,
                "Volume": volume,
                "Start Price": start_price,
                "High Price": high_price,
                "Low Price": low_price
            })
        
        return data_list
    else:
        print("Failed to fetch the page.")
        return None

if __name__ == "__main__":
    stock_code = "code=066570"  # 종목코드
    stock_data = get_stock_data(stock_code)
    
    if stock_data:
        for data in stock_data:
            print(f"Date: {data['Date']}, Volume: {data['Volume']}, Start Price: {data['Start Price']}, High Price: {data['High Price']}, Low Price: {data['Low Price']}")
