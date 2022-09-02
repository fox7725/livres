import os
import csv
import requests
from bs4 import BeautifulSoup
import urllib.request

#on test l'existence des répertoires pour l'enregistrement du CSV et des images sinon les créer,
#grace à "exist_ok=True", l'erreur est ignorée si les répertoires existent
os.makedirs("csv", exist_ok=True)
os.makedirs("images", exist_ok=True)

#On créé le fichier CSV et on y place l'entête
#On place la future entête du CSV dans une liste
entete = ["product_page_url", "universal_product_code (UPC)", "title", "price_including_tax", "price_excluding_tax", \
          "number_available", "product_description", "category", "review_rating", "image_url"]

#On créé un fichier CSV en "write" et on y insère l'entête
with open("csv/livres.csv", "w") as fichier_csv:
    writer = csv.writer(fichier_csv, delimiter=",")
    writer.writerow(entete)

#On se connecte à la page d'accueil du site
url_categories = "https://books.toscrape.com/index.html"
page_categories = requests.get(url_categories)
soup_categories = BeautifulSoup(page_categories.content, "html.parser")

print("Je mémorise l'ensemble des catégories à parcourir")
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
    # Dans le dossiers images on créé des sous dossiers pour classer les images téléchargées
    sous_dossier = "images/" + nom_cat_texte
    os.makedirs(sous_dossier, exist_ok=True)
print("J'ai compté "+str(len(categories))+" catégories, j'ai donc créé un dossier par catégorie pour y ordonner les images.")

#On de mande s'il s'agit d'une démo
demo = " "
while (demo != "oui") and (demo != "non") :
    demo = input("Voulez vous juste faire un test rapide ? ('oui' ou 'non') ")
    oui = "oui"
    non = "non"
    if (demo != oui) and (demo != non) :
        print("la réponse '"+str(demo)+"' n'est pas valable ! Merci de répondre par 'oui' ou par 'non'.")
    elif (demo == oui) :
        print("Parfait, je ne vais traiter que les trois première catégories")
    elif (demo == non) :
        print("Je vais donc réaliser le travail en entier et parcourir les "+str(len(categories))+" catégories.")

#On créé un dictionnaire avec les catégories et un compteur pour faire le suivi de l'avancement du programme
suivi = dict(zip(liens, noms))
compteur = len(categories)

#On créé une boucle pour récupérer les liens des livres de chaque page de chaque catégorie
for category_url in liens:

    #on vérifie s'il s'agit du mode démo
    if demo=="oui" and compteur==(len(categories)-3) :
        break

    #maintenant que le mode démo est vérifier on continue le travail
    compteur -= 1
    print("J'attaque les livres de la catégorie '"+suivi[category_url]+"'. Il restera encore "+str(compteur)+" catégories à traiter.")
    page_page = requests.get(category_url)
    soup_page = BeautifulSoup(page_page.content, 'html.parser')
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
        next_page_url = category_url.rsplit("/", 1)[0] + "/" + next_page.find("a").get("href")
        page_page = requests.get(next_page_url)
        soup_page = BeautifulSoup(page_page.content, 'html.parser')
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
        page_livre = requests.get(url_livre)
        soup_livre = BeautifulSoup(page_livre.content, "html.parser")

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
            product_description.append(product_description_l[0].text.encode("utf-8", errors="replace"))
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
        # pour éviter les erreurs CSV on remplace les "," des titres par " "
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
        ligne = [product_page_urlcsv, \
        universal_product_codecsv, \
        titrecsv2, \
        price_including_taxcsv, \
        price_excluding_taxcsv, \
        number_availablecsv, \
        product_descriptioncsv, \
        categorycsv, \
        review_ratingcsv, \
        image_urlcsv]
        with open("csv/livres.csv", "a") as fichier_csv:
            writer = csv.writer(fichier_csv, delimiter=",")
            writer.writerow(ligne)

            #On télécharge et renomme les images dans le répertoire voulu
            lien_image = image_urlcsv
            nom_image = "images/"+product_page_urlcsv.replace("https://books.toscrape.com/catalogue", categorycsv)
            nom_image = nom_image.replace("/index.html", ".jpg")
            urllib.request.urlretrieve(lien_image, nom_image)

#une petite phrase gentille pour indiquer que le travail est terminé
print("Je sais que c'était long, mais il y avait beaucoup de pages à visiter. Vous pouvez donc maintenant consulter les dossiers csv et images")