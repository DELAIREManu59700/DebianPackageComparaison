# DebianPackageComparaison
Depuis une session Debian, pour visualiser la liste de tous les paquets Debian installé:
$>dpkg -i-list > listePaquetsDebInstallés 

Le fichier texte listePaquetsDebInstallés contient la liste des paquets debian installés sur la machine depusi laquelle on exécute la commande: dpkg --list

Le programme python écrit fait la comparaison entre deux fichiers texte construits avec une commande "dpkg --install"
--------------------------------------------------------------------------------------------------------------------
a) Il faut exécuter la commande "dpkg --install" sur la machine cible (de dev) sur laquelle on a installé l'environnement PFA.
--> dpkg --install  > lstPaqtsDebianCiblePFA
b) Il faut exécuter la commande "dpkg --install" depuis un container Docker créé sur base de l'image Docker PFA créée au préalable.
--> dpkg --install > listDebianPaquetsFromContainerPFA

c) Exécuter le programme Python suivant:
$>python3 compareInstalledDEBPackage.py PFA_ENV/lstPaqtsDebianCiblePFA PFA_ENV/listDebianPaquetsFromContainerPFA

Au préalable, on aura créé le répertoire "PFA_ENV", dans lequel on aura bien-sûr copié les deux fichiers textes "lstPaqtsDebianCiblePFA", et "listDebianPaquetsFromContainerPFA".

Ce programme charge ces deux fichiers, puis les compare et produit quatre fichier .csv, qui sont éditable avec Excel (voir le répertoire "Resultat"):
--------------------------------------------------------------------------------------------------------------------------------------------------------
EQUALPackages.csv : tous les paquets Debian installés sur les deux cibles, avec les mêmes versions et architectures.
DIFFPackages.csv : tous les paquets Debian qui sont présents sur les deux cibles, mais avec des versions (ou archi) différentes.
EXTRAPackagesList1.csv : Tous les paquets Debian seulement présents dans la première liste donnée en argument au programme.
EXTRAPackagesList2.csv : Tous les paquets Debian seulement présents dans la deuxième liste donnée en argument au programme.

Interprétation des résultats:
----------------------------
Il faut garder en tête que l'image Docker PFA construite avait pour objectif de recréer de façon virtuelle un environnement PFA minimal de DEV utile pour faire les compilations (gcc, cmake, gcc-6, g++, ...) et pour produire les livrables ".deb" (dpka, apt).

L'objectif de cette image Docker PFA n'était pas de reproduire à l'identique l'environnement PFA cible.

C'est pourquoi il existe des fichiers non-vide : DIFFPackages.csv, EXTRAPackagesList1.csv et EXTRAPackagesList2.csv.
L'environnement PFA virtualisé dans l'image Docker est plus réduit que l'environnement PFA cible, et contient donc moins de paquets Debian installés.

Les seuls paquets Debian qui ont été installés dans l'image docker PFA sont ceux qui avaient été identifiés comme nécessaires pour réaliser les compilations, et la génération des livrables.
Ces seuls paquages sont suffisants pour disposer d'un environnement virtualisé de génération dans lequel les compilateurs gcc, et g++, sont dans la version attendue pour réaliser les compilations pour la cible "Debian 9 - PFA".
