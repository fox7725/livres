import csv
import urllib.request
import requests
from bs4 import BeautifulSoup
import os

def dictCategories (categories) :
    #Fonction qui crée un dictionnaire avec noms et liens des catégories
    # On créé une boucle pour récupérer les liens des catégories
    liens = []
    for lien in categories:
        lien_complet = "https://books.toscrape.com/" + lien.get("href")
        liens.append(lien_complet)

    # On créé une boucle pour récupérer les noms des catégories
    noms = []
    for nom_cat in categories:
        nom_cat_texte = nom_cat.text.strip()
        noms.append(nom_cat_texte)
        # Dans le dossiers images on créé des sous dossiers pour classer les images téléchargées
        sous_dossier = "images/" + nom_cat_texte
        os.makedirs(sous_dossier, exist_ok=True)

    # On créé un dictionnaire avec les catégories
    return dict(zip(liens, noms))

def CSV_manip (dossier, option, delimiteur, ecrire) :
    #Fonction pour manipuler le CSV, soit en write (w) soit en add (a)
    with open(dossier, option) as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=delimiteur)
        writer.writerow(ecrire)

def lectureSite (url) :
    #Fonction d'accès au site sur la page désirée
    page = requests.get(url)
    return BeautifulSoup(page.content, "html.parser")


def recup_image (lien_image, page_produitCSV, categoriecsv) :
    #Fonction pour télécharger, renommer et classer les images
    nom_image = "images/" + page_produitCSV.replace("https://books.toscrape.com/catalogue", categoriecsv)
    nom_image = nom_image.replace("/index.html", ".jpg")
    urllib.request.urlretrieve(lien_image, nom_image)

if __name__ == "__main__":
    print("Vous êtes dans le fichier de fonctions. merci de lancer main.py")