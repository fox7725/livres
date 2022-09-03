import csv
import urllib.request
import requests


def tableCategories (url_categories) :
    print(" ")

def CSV_manip (dossier, option, delimiteur, ecrire) :
    with open(dossier, option) as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=delimiteur)
        writer.writerow(ecrire)

def lectureSite () :
    print(" ")

def recup_image (lien_image, page_produitCSV, categoriecsv) :
    nom_image = "images/" + page_produitCSV.replace("https://books.toscrape.com/catalogue", categoriecsv)
    nom_image = nom_image.replace("/index.html", ".jpg")
    urllib.request.urlretrieve(lien_image, nom_image)