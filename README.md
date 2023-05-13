Prérequis : 
- Python 3.10 minimum
- Pip 
- os
- shutil
- zipfile
- argparse
- xml.etree.ElementTree as ET
- re

Fonctionnement du programme : 
Il récupère le fichier EPUB donné en paramètre
Décompression du fichier dans un dossier temporaire 
Récupération du fichier OPF et de la balise metadata 
Ajout des balises meta
Récupération de tous les fichiers HTML
Remplacement des balises HTML et BODY
Recompression du fichier sous un nouveau nom
Export dans un dossier output 

Automatisation du programme : 
Faire un fichier Python qui récupère tout les fichiers epub dans le dossier courant 
Faire une boucle qui parcour la liste des fichiers et qui appel le programme en donnant le nom du fichier en paramètres


Vérifier le type d'epub
Formater correctement l'epub 
Condition si le dossiertemp existe
condition si le fichier dns ouput existe
