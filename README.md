# Projet INF421

## Mise en place

Ok alors petit tuto sur comment coder à plusieurs : 
- Faut utiliser GIT [TUTO du BR](https://gitlab.binets.fr/br/td-formation-git)
- Faut mettre en place un environnement virtuel [DOC](https://docs.python.org/3/library/venv.html)
  - L'avantage c'est que tu fais un dossier qui contient toutes les librairies utiles de ton projet et ca te pourri pas les dépendances avec d'autres librairies.
- Utiliser VSCode (c'est la vie ce truc) faut setup ton compte github avec VSCode [TUTO](https://code.visualstudio.com/docs/sourcecontrol/github)
  - Installer quelques extensions utiles sur VScode : Python, Jupyter, Markdown (all in One et Pdf), Material Icon Theme (c joli), [Copilot](https://github.com/features/copilot) (très utile ca aussi, je te laisse te renseigner )

## Installation 

Une fois que tout le bordel du haut est installé, faut installer les requirements !

C'est un petit fichier requirements.txt qui contient toutes les libriries python qu'on installe pour le projet. C'est super utile pour dire à ton python d'environnement virtuel qu'il doit installer tout un tas de libriraies et comme ca on a tout ca en commun toi et moi. 

Ici on va utiliser les libraires classiques de maths donc a priori j'installe simplement : Numpy, matplotlib, Pandas et comme on fait des graphes, j'ai choisi networkX en plus.

Globalement faut activer ton environnement virtuel (sous linux faut taper ça ) :

    source env/bin/activate 

Et après faut installer avec pip : 

    pip install -r requirements.txt

Si jamais tu ajoutes une lib faut update requirements.txt : 

    pip freeze > requirements.txt

Pour desactiver l'envrionnement virtuel : 

    deactivate 

### Remarques : 

J'ai pas trop les equivalents Windows donc je te conseille de faire un peu de recherche. Y'a un fichier .gitignore dans le repo ca correpsond à des règles en plus pour que git copie pas l'historique de certains fichiers. En gros je lui demande de pas copier mon environnemnt virtuel, tout le monde sait qu'il est la mais pas besoin d'allourdir le projet en copiant tout l'historique quoi, je gère ca à côté avec pip :blush:

Bon courage et hesite pas à me MP si besoin Martin.