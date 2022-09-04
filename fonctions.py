import csv
import urllib.request
import requests
from bs4 import BeautifulSoup

def tableCategories (url_categories) :
    print(" ")

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