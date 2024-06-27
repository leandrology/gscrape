import requests
from bs4 import BeautifulSoup
import concurrent.futures
import time
import csv
from urllib.parse import quote_plus

def check_ranking(keyword, website):
    encoded_keyword = quote_plus(keyword)
    url = f"https://www.google.com/search?q={encoded_keyword}&num=100"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    time.sleep(1)
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        search_results = soup.find_all('div', class_='yuRUbf')
        
        for index, result in enumerate(search_results, start=1):
            link = result.find('a')['href']
            if website in link:
                return keyword, index
        
        return keyword, "Not found in top 100 results"
    except Exception as e:
        return keyword, f"Error: {str(e)}"

def batch_check_rankings(keywords, website):
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_keyword = {executor.submit(check_ranking, keyword, website): keyword for keyword in keywords}
        for future in concurrent.futures.as_completed(future_to_keyword):
            keyword = future_to_keyword[future]
            try:
                results.append(future.result())
            except Exception as exc:
                print(f'{keyword} generated an exception: {exc}')
    return results

def save_to_csv(results, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Keyword', 'Ranking'])
        for result in results:
            writer.writerow(result)

# Example usage
website = "greenproenergy.ie"
keywords = [
    "seai grants Ireland",
"energy Ireland",
"ber rating Ireland",
"air tightness test Ireland",
"home energy assessment Ireland",
"energy grants Ireland",
"ber cert Ireland",
"air tightness testing Ireland",
"home energy audit Ireland",
"energy efficiency Ireland",
"energy consultants Ireland",
"ber certificate Ireland",
"air tightness test results Ireland",
"energy efficient homes Ireland",
"domestic ventilation systems Ireland",
"air tightness test near me Ireland",
"home energy consultant Ireland",
"energy saving grants Ireland",
"energy engineering Ireland",
"home energy consultants Ireland",
"ber energy rating Ireland",
"energy consultant Ireland",
"ventilation testing equipment Ireland",
"energy consulting Ireland",
"home energy efficiency audit Ireland",
"grants for energy efficiency Ireland",
"energy sustainability Ireland",
"seai better energy homes grant Ireland",
"seai better energy grants Ireland",
"seai contractors Ireland",
"seai energy grants Ireland",
"seai technical advisor Ireland",
"seai registered contractors Ireland",
"seai contractors list Ireland",
"seai approved contractors list Ireland",
"seai registered insulation contractors Ireland",
"seai contractor registration Ireland",
"seai contractor contact Ireland",
"seai registered pv installers Ireland",
"registered seai contractors Ireland",
"seai grants registered contractors Ireland",
"home energy assessment in Ireland",
"energy efficiency solutions Ireland",
"ber rating services Ireland",
"energy grants for homes Ireland",
"energy consultants in Ireland",
"ventilation testing services Ireland",
"sustainable energy solutions Ireland",
"ber certificate assistance Ireland",
"energy saving consultation Ireland",
"renewable energy services Ireland",
"seai grants for Ireland residents",
"air tightness test near me in Ireland",
"ber energy rating assessment Ireland",
"energy transition Ireland",
"seai energy homes grant Ireland",
"seai Ireland",
"sustainable energy Ireland",
"home energy grants Ireland",
"nationwide energy consultants Ireland",
"engineering consultants Ireland",
"ber assessors Ireland",
"ber Ireland",
"find a ber assessor Ireland",
"air tightness test building regulations Ireland",
"air leak test house Ireland",
"home energy assessment cost Ireland",
"home energy audit business Ireland",
"energy consultancy Ireland",
"commercial energy efficiency Ireland",
"sustainable energy consulting Ireland",
"ventilation testing Ireland",
"energy management services Ireland",
"part l compliance Ireland",
"part l compliance report Ireland",
"heating and domestic hot water systems for dwellings – achieving compliance with part l Ireland",
"display energy certificates requirements Ireland",
"display energy certificates Ireland",
"display energy certificates register Ireland",
"house energy ratings Ireland",
]

results = batch_check_rankings(keywords, website)
save_to_csv(results, 'keyword_rankings.csv')

print("Rankings have been saved to keyword_rankings.csv")
for keyword, ranking in results:
    print(f"Ranking for '{keyword}': {ranking}")