import requests
from bs4 import BeautifulSoup

URL = "https://ftmo.com/it/faq/"
OUTPUT_FILE = "ftmo_faq.txt"

def scrape_ftmo_faq():
    print("🔍 Sto raccogliendo le domande e risposte da FTMO...")
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    faqs = soup.select('.elementor-accordion-item')  # Dipende dalla struttura del sito
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for faq in faqs:
            question = faq.select_one('.elementor-tab-title').get_text(strip=True)
            answer = faq.select_one('.elementor-tab-content').get_text(strip=True)
            f.write(f"Q: {question}\nA: {answer}\n\n")

    print(f"✅ Fatto! File salvato in: {OUTPUT_FILE}")

if __name__ == "__main__":
    scrape_ftmo_faq()
