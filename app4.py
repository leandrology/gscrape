from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import random
import csv

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)

    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    return driver

def get_google_ranking(driver, keyword, target_url, num_results=50):
    url = f"https://www.google.ie/search?q={keyword}&num={num_results}"
    
    time.sleep(random.uniform(1, 3))
    driver.get(url)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.g")))
    time.sleep(random.uniform(2, 4))

    search_results = driver.find_elements(By.CSS_SELECTOR, "div.yuRUbf")

    for index, result in enumerate(search_results, start=1):
        link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
        if re.search(target_url, link, re.IGNORECASE):
            return index
        
        time.sleep(random.uniform(0.1, 0.3))

        if index % 10 == 0:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(1, 2))

    return None

def process_keywords(keywords, target_url, max_retries=3):
    driver = setup_driver()
    results = []

    for keyword in keywords:
        for attempt in range(max_retries):
            try:
                ranking = get_google_ranking(driver, keyword, target_url)
                results.append((keyword, ranking))
                print(f"Processed: {keyword} - Ranking: {ranking}")
                break
            except Exception as e:
                print(f"Attempt {attempt + 1} failed for '{keyword}': {str(e)}")
                if attempt < max_retries - 1:
                    wait_time = random.uniform(60, 180)
                    print(f"Waiting for {wait_time:.2f} seconds before retrying...")
                    time.sleep(wait_time)
                else:
                    print(f"Max retries reached for '{keyword}'. Moving to next keyword.")
                    results.append((keyword, None))

        # Add a longer delay between keywords
        time.sleep(random.uniform(5, 10))

    driver.quit()
    return results

def save_results_to_csv(results, filename="keyword_rankings.csv"):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Keyword', 'Ranking'])
        for keyword, ranking in results:
            writer.writerow([keyword, ranking if ranking else 'Not found'])

# Example usage
target_url = "greenproenergy.ie"
keywords = [
"ventilation testing services Ireland",
"ventilation testing Ireland",
]

results = process_keywords(keywords, target_url)
save_results_to_csv(results)

print("Results saved to keyword_rankings.csv")
for keyword, ranking in results:
    if ranking:
        print(f"The website {target_url} ranks #{ranking} for the keyword '{keyword}'")
    else:
        print(f"The website {target_url} was not found in the top 50 results for the keyword '{keyword}'")
