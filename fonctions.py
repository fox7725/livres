import csv

def tableCategories (url_categories) :
    print(" ")

def CSV_manip (dossier, option, delimiteur, ecrire) :
    with open(dossier, option) as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=delimiteur)
        writer.writerow(ecrire)

def lectureSite () :
    print(" ")

def recup_image () :
    print(" ")