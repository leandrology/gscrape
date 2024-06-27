import requests
from bs4 import BeautifulSoup

def check_ranking(keyword, website):
    url = f"https://www.google.ie/search?q={keyword}&num=100"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    search_results = soup.find_all('div', class_='yuRUbf')
    
    for index, result in enumerate(search_results, start=1):
        link = result.find('a')['href']
        if website in link:
            return index
    
    return "Not found in top 100 results"

# Example usage
keyword = "Dietician Ireland"
keyword2 = "Nutritionist Ireland"
website = "insideoutnutrition.ie"
ranking = check_ranking(keyword, website)
ranking2 = check_ranking(keyword2, website)
print(f"{website} ranking for the word '{keyword}': {ranking}")
print(f"{website} ranking for the word '{keyword2}': {ranking2}")