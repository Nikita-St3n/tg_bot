import requests
from bs4 import BeautifulSoup

def get_anecdotes(page):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    }

    new_anekdots = {}

    # page = random.randint(0, 24)

    url = f"https://anekdotov.net/anekdot/index-page-{page}.html"
    req = requests.get(url, headers)

    soup = BeautifulSoup(req.text, "lxml")

    anekdots = soup.find_all("div", class_="anekdot")
    for anekdot in anekdots:
        anekdot_p = anekdot.find_all("p")
        anekdot_url = anekdot.find("a").get("href")

        anekdot_text = ""

        for p in anekdot_p:
            anekdot_text += p.text.strip() + '\n'
        
        anekdot_text += '\n' + "<b>Жизненные анекдоты</b>"

        new_anekdots[anekdot_url] = {
            "anekdot_text": anekdot_text
        }

    return new_anekdots