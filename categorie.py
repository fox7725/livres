import requests
from bs4 import BeautifulSoup

#On se connecte à la page d'accueil du site
url_categories = "https://books.toscrape.com/index.html"
page_categories = requests.get(url_categories)
soup_categories = BeautifulSoup(page_categories.content, "html.parser")

#On sélcetionne la liste des catégories
categories = soup_categories.select(".side_categories > ul > li > ul > li > a")

#On créé une boucle pour récupérer les liens des catégories
liens = []
for lien in categories:
    lien_complet = "https://books.toscrape.com/" + lien.get("href")
    liens.append(lien_complet)

#On créé une boucle pour récupérer les noms des catégories
noms = []
for nom_cat in categories:
    nom_cat_texte = nom_cat.text.strip()
    noms.append(nom_cat_texte)

#On créé un dictionnaire avec les noms et les liens
dictionnaire_categories = dict(zip(noms, liens))
#print(liens)
print(dictionnaire_categories)