import requests
from bs4 import BeautifulSoup
# On chage la page en HTML
category_url = "https://books.toscrape.com/catalogue/category/books/add-a-comment_18/"
url = category_url + "index.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
liste_livres = soup.select(".image_container > a")
liste_livres_url = []
for livre in liste_livres:
    livre_clean = livre.get("href")
    livre_url = livre_clean.replace("../../..", "https://books.toscrape.com/catalogue")
    liste_livres_url.append(livre_url)

#On vérifie s'i y a un bouton "next"
next_page = soup.find("li", class_="next")
#On créé une boucle pour les pages suivante
while next_page != None:
    next_page_url = category_url + next_page.find("a").get("href")
    page = requests.get(next_page_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    liste_livres = soup.select(".image_container > a")
    for livre in liste_livres:
        livre_clean = livre.get("href")
        livre_url = livre_clean.replace("../../..", "https://books.toscrape.com/catalogue")
        liste_livres_url.append(livre_url)
    next_page = soup.find("li", class_="next")
print(liste_livres_url)
print(len(liste_livres_url))