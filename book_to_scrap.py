#On importe les différents packages nécessaires
import csv
import requests
from bs4 import BeautifulSoup

#On charge la page de l'article en HTML
url_livre = "https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html"
page_livre = requests.get(url_livre)
soup_livre = BeautifulSoup(page_livre.content, "html.parser")

#On place la future entête du CSV dans une liste
entete = ["product_page_url", "universal_product_code (UPC)", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]

#On créé un fichier CSV en "write" et on y insère l'entête
"""with open("livres.csv", "w") as fichier_csv:
    writer = csv.writer(fichier_csv, delimiter=",")
    writer.writerow(entete)"""

#On récupère les informations demandées dans des variables
    #récupération de l'url de la page
product_page_url = url
    #récupération du titre du livre (seul élément en <h1>
title = soup_livre.h1.string
    #Pour récupérer les éléments en bas de page qui sont sous forme de
    #tableau, on créé deux listes avec les <th> et les <td> et on fait un dictionnaire
tableau = soup_livre.find("table", class_="table-striped")
nom = tableau.find_all("th")
valeur = tableau.find_all("td")
liste_noms = []
for name in nom:
   liste_noms.append(name.string)
liste_valeurs = []
for values in valeur:
    liste_valeurs.append(values.string)
dictionnaire_tableau = dict(zip(liste_noms, liste_valeurs))
    #depuis les dictionnaire, on peut récupérer depuis le dictionnaire
universal_product_code = dictionnaire_tableau["UPC"]
price_including_tax = dictionnaire_tableau["Price (incl. tax)"]
price_excluding_tax = dictionnaire_tableau["Price (excl. tax)"]
number_available = dictionnaire_tableau["Availability"]
    #pour la description, on récupère le texte enfant de la classe product_page
    #on trasnforme la liste obtenue en variable simple et on récupère le txt
product_description = soup_livre.select(".product_page > p")
product_description = product_description[0].text
    #Pour récupérer la catégorie qui se trouve dans le breadcrumbs qu'on va
    #transformer en liste et dont on va récupérer l'avant dernière valeur
    #on ne récupère que le texte
category = soup_livre.select(".breadcrumb > li")
category = category[-2].find("a").string
    #pour l'url de l'image, on va dans la classe "active" pour récupérer
    #l'attribut "src" et il faut remplacer "../.." par la racine du site
image_url = soup_livre.select(".active > img")
image_url = image_url[0]
image_url = image_url.get("src")
image_url = image_url.replace("../..", "https://books.toscrape.com")
    #Pour récupérer le nombre d'étoiles, on peut voir qu'il est clairement
    #mis dans la classe, qu'il faut donc récupérer
review_rating = soup_livre.find("p", {"class": "star-rating"}).get("class")
review_rating = review_rating[1]
if review_rating == "One":
    review_rating="1 star"
elif review_rating == "Two":
    review_rating="2 stars"
elif review_rating == "Three":
    review_rating="3 stars"
elif review_rating == "Four":
    review_rating="4 stars"
elif review_rating == "Five":
    review_rating="5 stars"

#On regarde si tout se passe bien
print(product_page_url)
print(title)
print(product_description)
print(universal_product_code)
print(price_including_tax)
print(price_excluding_tax)
print(number_available)
print(image_url)
print(category)
print(review_rating)