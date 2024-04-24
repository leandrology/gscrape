import requests
from bs4 import BeautifulSoup
import gspread
from fake_useragent import UserAgent
import time
import schedule

# Set headers with a random user agent
headers = {'User-Agent': UserAgent().desktop}


# # Parse HTML content with Beautiful Soup
# soup = BeautifulSoup(content, "html.parser")
# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# driver = webdriver.Chrome(options=options)
# user_agent = UserAgent()

# headers = {'User-Agent': user_agent.desktop}
def run():
    url = "https://www.kitco.com/price/precious-metals"
    response = requests.get(url, headers=headers)
    content = response.content

    soup = BeautifulSoup(content, "html.parser")


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



    gc = gspread.service_account(filename="creds.json") 
    sh = gc.open('prices').worksheet("Scraped") 

    sh.update(data_list)
    print("Metal prices sent to Google Sheets successfully!")

    pass

schedule.every(20).seconds.do(run)

while True:
    schedule.run_pending()
    time.sleep(1)

# # Main program
# if __name__ == "__main__":
#     run()
#     # soup = request()
#     # data_list = parse(soup)
#     # output(data_list)

#     print("Metal prices sent to Google Sheets successfully!")
    
# python -m pip install -r requirements.txt