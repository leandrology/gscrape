from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def check_google_maps_ranking(keyword, business_name, location):
    url = f"https://www.google.ie/maps/search/{keyword}/{location}"
    
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
    
    # Initialize the WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(url)
        
        # Wait for the results to load
        wait = WebDriverWait(driver, 10)
        results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.Nv2PK")))
        
        for index, result in enumerate(results, start=1):
            name = result.find_element(By.CSS_SELECTOR, "div.qBF1Pd").text.strip()
            if business_name.lower() in name.lower():
                return index
        
        return "Not found in visible results"
    
    finally:
        driver.quit()

# Example usage
keyword = "ventilation testing services Ireland"
business_name = "Greenpro Energy Consultants" 
location = "Ireland"

ranking = check_google_maps_ranking(keyword, business_name, location)
print(f"Ranking for '{business_name}' when searching '{keyword}' in {location}: {ranking}")