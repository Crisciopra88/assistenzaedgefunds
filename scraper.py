import requests
from bs4 import BeautifulSoup

def fetch_ftmo_faq():
    url = "https://ftmo.com/it/faq/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    faqs = []
    for item in soup.select(".faq__item"):
        question = item.select_one(".faq__question")
        answer = item.select_one(".faq__answer")
        if question and answer:
            faqs.append(f"Q: {question.get_text(strip=True)}\nA: {answer.get_text(strip=True)}\n")

    with open("ftmo_faq.txt", "w", encoding="utf-8") as f:
        f.write("\n\n".join(faqs))

if __name__ == "__main__":
    fetch_ftmo_faq()
    print("✅ FAQ FTMO salvate in ftmo_faq.txt")
