import requests
from bs4 import BeautifulSoup
import gspread
from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
user_agent = UserAgent()

headers = {'User-Agent': user_agent.desktop}

def request():
  url = "https://www.kitco.com/price/precious-metals"
  response = requests.get(url, headers=headers)
  content = response.content

  soup = BeautifulSoup(content, "html.parser")
  return soup

def parse(soup):

  element = soup.find_all("ul")
  element = element[3]

  data_list = []
  for li in element.find_all("li"):  
    content_div = li.find("div", class_="BidAskGrid_gridifier__l1T1o")  
    metal_name = content_div.find("span", class_="BidAskGrid_bold__vjdF5").text.strip()
    is_rhodium = metal_name == "Rhodium"  
    if is_rhodium:
        metal_name = content_div.find("span", class_="pl-[10px] !border-0").text.strip()  
    
    data_points = []
    for span in content_div.find_all("span"):
        data_points.append(span.text.strip())
    
    change_elements = content_div.find_all("div", class_="BidAskGrid_change__ALV4Z")  
    change_values = []
    for change_element in change_elements:
        change_values.append(change_element.text.strip())
    
    data_to_append = data_points + change_values
    if is_rhodium:
        data_to_append = data_to_append[1:]
    data_list.append(data_to_append) 

  print(data_list)

  return data_list

def output(data_list):

  gc = gspread.service_account(filename="creds.json") 
  sh = gc.open('prices').worksheet("Scraped") 

  sh.update(data_list)

# Main program
if __name__ == "__main__":
    soup = request()
    data_list = parse(soup)
    output(data_list)

    print("Metal prices sent to Google Sheets successfully!")