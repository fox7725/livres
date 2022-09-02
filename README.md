# Books Online
Ceci est un projet de scrapper python dans le cadre du projet 2 de la formation Développeur d'applications Python chez Open ClassRooms.

# Un scrapper ? 

Ce script Python récupère différentes informations sur l'ensemble des livres du site Books to Scrape et il télécharge les photos et les classe par catégorie.

# Comment utiliser le fichier python
## Etape 1 : Créer votre environnement virtuel :
Pour chaque nouveau projet, il est recommandé d'installer un environnement virtuel pour partir sur de nouvelles bases
- Ouvrez votre Terminal
- Dans le dossier où vous avez copié les fichiers du projet, tappez la commande `python -m venv env`
- Puis lancez l'environnement virtuel en tapant `env\Scripts\activate.bat`
- Pour faire fonctionner le scrapper, vous aurez besoin de quelques packages. Installez les depuis requierement.txt : `pip install -r requirements.txt`

## Etape 2 : Lancer le scrapper
Nous avons presque terminé, il ne vous reste plus qu'à démarrer le script, et pour ça rien de plus simple il vous suffit d'écrire la commande `python main.py`.
Maintenant servez vous un café, prenez même un biscuit et faites une caresse à votre animal préféré ... il y a 1000 pages à visiter et ça prend un peu de temps.
Une fois le script terminé un petite phrase gentille vous l'indiquera.

## Etape 3 : Quitter l'environnement virtuel
N'oubliez pas de fermer la porte de votre environnement virtuel (et d'y éteindre la lumière) avec la commande `deactivate`
Vous pouvez maintenant aller chercher les fichiers image dans le dossier **"images"**, elles sont toutes classées dans des sous-dossiers aux noms des catégories.
Vous trouverez le fichier **livres.csv** dans le dossier CSV.

# Remerciements
Un grand merci à mon mentor **Serigne Fallou Ndiaye** qui a su me guider tout en douceur et à **Zozor** (l'ancienne mascotte du site) de revenir sur **le Site du Zéro** pour apprendre