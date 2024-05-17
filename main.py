import requests
from bs4 import BeautifulSoup
import gspread
from fake_useragent import UserAgent
import time
import schedule

# Set headers with a random user agent
ua = UserAgent(platforms=["desktop"])
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


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
    # print ("This is the response: ", response)
    content = response.content
    # print ("This is the content: ", content)
    soup = BeautifulSoup(content, "html.parser")
    # print ("This is the soup: ", soup)


    element = soup.find_all("ul")
    element = element[4]
    # print (element)
    items = soup.find("ul", class_="BidAskGrid_listify__1liIU")
    data_list = []
    row = 1
    for li in items.find_all("li"):
      div = li.find("div", class_="BidAskGrid_gridifier__l1T1o")
      metal = div.find("span", class_="BidAskGrid_bold__vjdF5").text.strip()
    #   date = div.find_all("span")[1].text.strip()
    #   time = div.find_all("span")[2].text.strip()
    #   bid = div.find_all("span")[3].text.strip()
    #   ask = div.find_all("span")[4].text.strip()
    #   change_value = div.find("div", class_="BidAskGrid_changeUp__snqc8").text.strip()
    #   low = div.find_all("span")[5].text.strip()
    #   high = div.find_all("span")[6].text.strip()
     
      is_rhodium = metal == "Rhodium"  
      if is_rhodium:
          metal = div.find("span", class_="pl-[10px] !border-0").text.strip()  
      
      data_points = []
      for span in div.find_all("span"):
          data_points.append(span.text.strip())
      
      change_elements = div.find_all("div", class_="BidAskGrid_change__ALV4Z")  
      change_values = []
      for change_element in change_elements:
          change_values.append(change_element.text.strip())
      
      data_to_append = data_points + change_values
      if is_rhodium:
          data_to_append = data_to_append[1:]
      data_list.append(data_to_append) 
     
      # is_rhodium = metal == "Rhodium"  
      # if is_rhodium:
      #     metal = div.find("span", class_="pl-[10px] !border-0").text.strip()
      # if is_rhodium:
      #    data_to_append = data_to_append[1:]
      #    data_list.append(data_to_append)
      # data_list.append([metal, date, time, bid, ask, change_value, low, high])
      # data_list.append({
      #     "Metal": metal,
      #     "Date": date,
      #     "Time": time,
      #     "Bid": bid,
      #     "Ask": ask,
      #     "Change": change_value,
      #     "Low": low,
      #     "High": high
      # })

    print(data_list)
  
    # for li in element.find_all("li"):  
    #   content_div = li.find("ul", class_="BidAskGrid_listify__1liIU") 
    #   metal_name = content_div.find("span", class_="BidAskGrid_bold__vjdF5").text.strip()
    #   is_rhodium = metal_name == "Rhodium"  
    #   if is_rhodium:
    #       metal_name = content_div.find("span", class_="pl-[10px] !border-0").text.strip()  
      
    #   data_points = []
    #   for span in content_div.find_all("span"):
    #       data_points.append(span.text.strip())
      
    #   change_elements = content_div.find_all("div", class_="BidAskGrid_change__ALV4Z")  
    #   change_values = []
    #   for change_element in change_elements:
    #       change_values.append(change_element.text.strip())
      
    #   data_to_append = data_points + change_values
    #   if is_rhodium:
    #       data_to_append = data_to_append[1:]
      # data_list.append(data_to_append) 

    # print(data_list)



    gc = gspread.service_account(filename="creds.json")
    sh = gc.open('NEW KITCO_LIVE PRICES').worksheet("Scraped") 

    sh.update(data_list)
    # row += 1
    print("Metal prices sent to Google Sheets successfully!")

    pass

schedule.every(20).seconds.do(run)

while True:
    schedule.run_pending()
    time.sleep(1)

# # Main program
if __name__ == "__main__":
    run()
#     # soup = request()
#     # data_list = parse(soup)
#     # output(data_list)

#     print("Metal prices sent to Google Sheets successfully!")
    
# python -m pip install -r requirements.txt