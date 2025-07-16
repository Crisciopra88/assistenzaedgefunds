import requests
from bs4 import BeautifulSoup

def scrape_ftmo_faq():
    url = "https://ftmo.com/it/faq/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    faq_data = []
    items = soup.select(".elementor-accordion .elementor-tab-title")

    for item in items:
        question = item.get_text(strip=True)
        answer_element = item.find_next_sibling("div")
        if answer_element:
            answer = answer_element.get_text(separator="\n", strip=True)
        else:
            answer = "Nessuna risposta trovata."
        faq_data.append(f"Domanda: {question}\nRisposta: {answer}\n"_
