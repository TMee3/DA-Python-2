101 lines (85 sloc)  4.54 KB

# Scraping "books.toscrape.com"
Application python de récupération de données pour le site http://books.toscrape.com.

## *Table des matières*
1. [Prérequis](#1-prérequis)
2. [Informations générales](#2-informations-générales)
   - [scraping_one_book.py](#a-scraping_one_bookpy)
   - [scraping_one_category.py](#b-scraping_one_categorypy)
   - [scraping_all_category.py](#c-scraping_all_categorypy)
3. [Exécuter les scripts](#3-exécuter-les-scripts)
4. [Analyse du résultat](#4-analyse-du-résultat)
5. [Futures améliorations](#5-futures-améliorations)
6. [Auteur](#6-auteur)

## 1. Prérequis
L'installation de la version 3.11.1 de Python est requise pour exécuter les scripts : 
https://docs.python.org/release/3.11.1/download.html

## 2. Informations générales
Ce répertoire comporte quatre scripts, chacun ayant une fonction spécifique. 
Le but est de collecter des informations sur les livres sur le site https://books.toscrape.com/ et de télécharger les images de couverture correspondantes.

  Ces informations sont : 
- product_page_url 
- universal_product_code(upc)
- title
- price_including_tax
- price_excluding_tax
- number_available
- product_description
- category
- review_rating
- image_url

### A) scraping_one_book.py
Le script "scraping_one_book.py" sera utilisé pour collecter les données et l'image pour un seul livre. 
Il créera un répertoire intitulé "output" qui contiendra les résultats de son exécution et qui s'appellera "output/onebook.csv" et " output/onebook.jpg). 
Lors de l'exécution du script, il vous sera demandé de fournir l'URL d'un livre, par exemple : "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html".

### B) scraping_one_category.py
Le script "scraping_one_category.py" sera utilisé pour collecter les données et les images pour tous les livres dans une catégorie spécifique.
Un dossier appelé "output" sera créé pour stocker les résultats du script.
Lors de l'exécution du script, vous devrez fournir l'URL d'une catégorie de livres, par exemple : https://books.toscrape.com/catalogue/category/books/travel_2/index.html.

### C) scraping_all_category.py
Le script intitulé "scraping_all_category.py" aura pour tâche de collecter les données et les images pour l'ensemble des livres de toutes les catégories disponibles sur le site, soit tous les livres présents sur ce dernier. 
Un répertoire nommé "output" sera créé pour conserver les résultats du script.
Ce dernier s'exécutera automatiquement sans nécessiter de saisir une URL.

## 3. *Exécuter les scripts*
Après avoir téléchargé DA-Python-2-main.zip depuis GitHub, il faut l'extraire dans un dossier de votre choix.   
Ensuite, en utilisant l'invite de commandes Windows (ou le terminal si vous êtes sur Mac ou Linux) :  
- Placez vous dans le dossier  
- Créez un environnement virtuel  
- Activez le  
- Installez les modules depuis requirements.txt
```
$ CD ../chemin/vers/DA-Python-2-main
$ python -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```
Vous pouvez maintenant exécuter le script de votre choix en tapant l'une des commandes suivante.
```
$ python scraping_one_book.py
```
ou
```
$ python scraping_one_category.py
```
ou
```
$ python scraping_all_category.py
```

## 4. *Analyse du résultat*
Par exemple, après avoir exécuter ```$ python scraping_one_book.py```, un dossier "output" est créer dans le dossier courant.  

Le dossier "output" se décompose comme suit :
- Dossier : "output"
   - Fichier : onebook.csv
   - Fichier : onebook.jpg
   


Ainsi, pour ```$ python scraping_one_category.py``` le dossier "output" va contenir un fichier "onecategory.csv" ainsi un autre sous dossier "categoryimg" contenant les images de la category scrapper.

Pour ```$ python scraping_all_category.py``` le dossier "output" va contenir autant de sous-dossier "Nom-de-la-catégorie" que de catégories sur le site, c'est à dire cinquante et dans ces catégories il y aura une sous categories "img" ou il y aura les images de chaque catégories. Composé ainsi : 
   Dossier : " Output"
      Dossier : "Nom-de-la-catégorie"
         Fichier : "Nom-de-la-catégorie.csv"
         Dossier : "img"
            Fichier : "title.jpg"

## 5. *Futures améliorations*
Voici une liste des améliorations envisageable :
- Faire une interface GUI 
- Lancer un seul script qui nous donne le choix entre les trois déjà existant
- Optimiser l'éxécution du script

## 6. *Auteur*
- Theo Pdioux https://github.com/TMee3