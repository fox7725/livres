import os
import csv
import fonctions
import requests
from bs4 import BeautifulSoup
import urllib.request
from fonctions import *

#on test l'existence des répertoires pour l'enregistrement du CSV et des images sinon les créer,
#grace à "exist_ok=True", l'erreur est ignorée si les répertoires existent
os.makedirs("csv", exist_ok=True)
os.makedirs("images", exist_ok=True)

#On défini les variables pour la fonction de création du CSV en "write"
#On appelle la fonction de manipulation du CSV pour créer le fichier et placer l'entête
entete = ["product_page_url", "universal_product_code (UPC)", "title", "price_including_tax", "price_excluding_tax", \
          "number_available", "product_description", "category", "review_rating", "image_url"]
dossier = "csv/livres.csv"
delimiteur = ","
fonctions.CSV_manip(dossier, "w", delimiteur, entete)

#On se connecte à la page d'accueil du site avec la fonction lectuSite
url_categories = "https://books.toscrape.com/index.html"
soup_categories = fonctions.lectureSite(url_categories)

print("Je mémorise l'ensemble des catégories à parcourir")

#On sélectionne la liste des catégories
categories = soup_categories.select(".side_categories > ul > li > ul > li > a")

#On récupère les liens et noms des catégories qu'on met dans un dictionnaire
suivi = fonctions.dictCategories(categories)
#On récupère les liens des catégories sous forme de liste (les clés dans le dictionnaire créé par la fonction
liens = list(suivi.keys())
#On récupère les noms des catégories sous forme de liste (les valeurs dans le dictionnaire créé par la fonction
noms = list(suivi.values())

print("J'ai compté "+str(len(categories))+" catégories, j'ai donc créé un dossier par catégorie pour y organiser les images.")

#On demande s'il s'agit d'une démo
demo = " "
while demo != "oui" and demo != "non" :
    print("Le traitement complet dure près de 20 minutes.")
    demo = input("Voulez vous juste faire un test rapide de quelques minutes ? ('oui' ou 'non') ")
    if demo != "oui" and demo != "non" :
        print("la réponse '"+str(demo)+"' n'est pas valable ! Merci de répondre par 'oui' ou par 'non'.")
    elif demo == "oui" :
        print("Parfait, je ne vais traiter que les deux premières catégories")
    elif demo == "non" :
        print("Je vais donc réaliser le travail en entier et parcourir les "+str(len(categories))+" catégories.")
        print("Prenez le temps de vous faire un café, et revenez me voir dans 20 minutes. :-)")

#Initialisation du compteur pour suivre l'avancement
compteur = len(categories)

#On créé une boucle pour récupérer les liens des livres de chaque page de chaque catégorie
for category_url in liens:

    #on vérifie s'il s'agit du mode démo
    if demo=="oui" and compteur==(len(categories)-2) :
        print("Comme nous sommes dans le mode démo, nous allons nous arrêter là.")
        break

    #maintenant que le mode démo est vérifié on continue le travail
    compteur -= 1
    print("J'attaque les livres de la catégorie '"+suivi[category_url]+"'. Il restera encore "+str(compteur)+" catégories à traiter.")

    #On se connecte à la première page de la catégorie pour y récupérer la liste des livres
    soup_page = fonctions.lectureSite(category_url)
    liste_livres = soup_page.select(".image_container > a")
    liste_livres_url = []
    for livre in liste_livres:
        livre_clean = livre.get("href")
        livre_url = livre_clean.replace("../../..", "https://books.toscrape.com/catalogue")
        liste_livres_url.append(livre_url)

    # On vérifie s'i y a un bouton "next"
    next_page = soup_page.find("li", class_="next")
    # On créé une boucle pour les pages suivante
    while next_page != None:
        #On transforme le lien pour qu'il soit utilisable
        next_page_url = category_url.rsplit("/", 1)[0] + "/" + next_page.find("a").get("href")
        #On se connecte à la page pour récupérer le liste des livres
        soup_page = fonctions.lectureSite(next_page_url)
        liste_livres = soup_page.select(".image_container > a")
        for livre in liste_livres:
            livre_clean = livre.get("href")
            livre_url = livre_clean.replace("../../..", "https://books.toscrape.com/catalogue")
            liste_livres_url.append(livre_url)
        next_page = soup_page.find("li", class_="next")

    #On créé une boucle pour récupérer les informations sur chaque page de livre
    product_page_url = []
    title = []
    product_description = []
    universal_product_code = []
    price_including_tax = []
    price_excluding_tax = []
    number_available = []
    image_url = []
    category = []
    review_rating = []
    for url_livre in liste_livres_url:
        #On se connecte à la page de chaque livre
        soup_livre = fonctions.lectureSite(url_livre)

        # On récupère les informations demandées dans des variables
        # récupération de l'url de la page
        product_page_url.append(url_livre)
        # récupération du titre du livre (seul élément en <h1>)
        title.append(soup_livre.h1.string)
        # Pour récupérer les éléments en bas de page qui sont sous forme de
        # tableau, on créé deux listes avec les <th> et les <td> et on fait un dictionnaire
        tableau = soup_livre.find("table", class_="table-striped")
        nom_tableau = tableau.find_all("th")
        valeur = tableau.find_all("td")
        liste_noms = []
        for name in nom_tableau:
            liste_noms.append(name.string)
        liste_valeurs = []
        for values in valeur:
            liste_valeurs.append(values.string)
        dictionnaire_tableau = dict(zip(liste_noms, liste_valeurs))
        # depuis les dictionnaire, on peut récupérer depuis le dictionnaire
        universal_product_code.append(dictionnaire_tableau["UPC"])
        price_including_tax.append(dictionnaire_tableau["Price (incl. tax)"])
        price_excluding_tax.append(dictionnaire_tableau["Price (excl. tax)"])
        number_available.append(dictionnaire_tableau["Availability"])
        # pour la description, on récupère le texte enfant de la classe product_page
        # on trasnforme la liste obtenue en variable simple et on récupère le txt
        product_description_l = soup_livre.select(".product_page > p")
        if product_description_l:
            #Certains descriptifs constiennent des caractères spéciaux, alors on encode en UTF-8
            #puis on décode pour traduire les caractère spéciaux
            product_description.append(product_description_l[0].text.encode("utf-8", errors="replace").decode("utf-8"))
        else:
            product_description.append(" ")
        # Pour récupérer la catégorie qui se trouve dans le breadcrumbs qu'on va
        # transformer en liste et dont on va récupérer l'avant dernière valeur
        # on ne récupère que le texte
        category_l = soup_livre.select(".breadcrumb > li")
        category.append(category_l[-2].find("a").string)
        # pour l'url de l'image, on va dans la classe "active" pour récupérer
        # l'attribut "src" et il faut remplacer "../.." par la racine du site
        image_url_l = soup_livre.select(".active > img")
        image_url_l = image_url_l[0]
        image_url_l = image_url_l.get("src")
        image_url.append(image_url_l.replace("../..", "https://books.toscrape.com"))
        # Pour récupérer le nombre d'étoiles, on peut voir qu'il est clairement
        # mis dans la classe, qu'il faut donc récupérer
        review_rating_l = soup_livre.find("p", {"class": "star-rating"}).get("class")
        review_rating_l = review_rating_l[1]
        if review_rating_l == "One":
            review_rating.append("1 star")
        elif review_rating_l == "Two":
            review_rating.append("2 stars")
        elif review_rating_l == "Three":
            review_rating.append("3 stars")
        elif review_rating_l == "Four":
            review_rating.append("4 stars")
        elif review_rating_l == "Five":
            review_rating.append("5 stars")

        # On rempli le fichier ligne par ligne avec une boucle,
    for product_page_urlcsv, \
        universal_product_codecsv, \
        titlecsv, \
        price_including_taxcsv, \
        price_excluding_taxcsv, \
        number_availablecsv, \
        product_descriptioncsv, \
        categorycsv, \
        review_ratingcsv, \
        image_urlcsv \
        in zip(product_page_url, \
        universal_product_code, \
        title, \
        price_including_tax, \
        price_excluding_tax, \
        number_available, \
        product_description, \
        category, \
        review_rating, \
        image_url) :
        titrecsv2 = titlecsv.replace(",", " ")

        # pour éviter les erreurs CSV on remplace les "," des titres par " " et ";" par "-"
        product_descriptioncsv2 = product_descriptioncsv.replace(",", " ")
        product_descriptioncsv2 = product_descriptioncsv2.replace(";", "-")

        ligne = [product_page_urlcsv, \
        universal_product_codecsv, \
        titrecsv2, \
        price_including_taxcsv, \
        price_excluding_taxcsv, \
        number_availablecsv, \
        product_descriptioncsv2, \
        categorycsv, \
        review_ratingcsv, \
        image_urlcsv]

        #enregistrement dans le CSV
        #On ne veut plus modifier le CSV en write (w) mais en add (a)
        fonctions.CSV_manip(dossier, "a", delimiteur, ligne)

        #On télécharge et renomme les images dans le répertoire voulu
        fonctions.recup_image(image_urlcsv, product_page_urlcsv, categorycsv)

#une petite phrase gentille pour indiquer que le travail est terminé
print("Je sais que c'était long, mais il y avait beaucoup de pages à visiter. Vous pouvez donc maintenant consulter les dossiers csv et images")