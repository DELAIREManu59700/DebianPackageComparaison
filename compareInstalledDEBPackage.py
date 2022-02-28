import sys
import unPaquet
import analyseListePaquetsDeb

class DebianPackageComparator:
    def __init__(self):
            self.__listEQUALPack = []                   #liste d'objets instance de UnPaquet pour des paquets Debian installés à l'identique dans les deux listes de paquets comparés
            self.__listDIFFPack = []                    #liste d'objets instance de UnPaquet pour des paquets Debian installés (i.e. présents) dans les deux listes de paquets comparés, mais de version ou d'archi différentes
            self.__list1EXTRAPack = []                   #liste d'objets instance de UnPaquet pour des paquets Debian seulement présents dans la première liste de paquets
            self.__list2EXTRAPack = []                   #liste d'objets instance de UnPaquet pour des paquets Debian seulement présents dans la deuxième listes de paquets

        # Compare deux listes d'objets instance de UnPaquet pour en tirer trois listes
        # 1- les paquets présents et égaux dans les deux listes,
        # 2- les paquets présents mais différents entre les deux listes,
        # 3- les paquets seulement présents dans l'une des listes.
    def compareLists(self, lstPack1, lstPack2):
        status=True
        if lstPack1 != None and lstPack2 != None and isinstance(lstPack1, analyseListePaquetsDeb.ListePaquets) and isinstance(lstPack2, analyseListePaquetsDeb.ListePaquets):

                paquets1 = lstPack1.getLstOfDebianPackages()                #Première liste d'objets instance de UnPaquet
                paquets2 = lstPack2.getLstOfDebianPackages()                #Deuxième liste d'objets instance de UnPaquet

                list1=paquets1
                self.__list1EXTRAPack = list1.copy()
                list2=paquets2
                self.__list2EXTRAPack = list2.copy()

                for pqt1 in list1:
                        for pqt2 in list2:
                                if pqt1.getNom().lower() == pqt2.getNom().lower() and pqt1.getVersion().lower()  == pqt2.getVersion().lower()  and pqt1.getArchitecture().lower()  == pqt2.getArchitecture().lower() :
                                        self.__listEQUALPack.append(unPaquet.UnPaquet(pqt1.getNom(), pqt1.getVersion(), pqt1.getArchitecture(), pqt1.getDescription()))
                                        self.__list1EXTRAPack.remove(pqt1)
                                        self.__list2EXTRAPack.remove(pqt2)
                                        break
                                elif pqt1.getNom().lower() == pqt2.getNom().lower() :
                                        self.__listDIFFPack.append(unPaquet.UnPaquet(pqt1.getNom(), pqt1.getVersion(), pqt1.getArchitecture(), pqt1.getDescription()))
                                        self.__list1EXTRAPack.remove(pqt1)
                                        self.__list2EXTRAPack.remove(pqt2)
                                        break

        else:
                status = False

        return status

    def getEqualPackages(self):
        return self.__listEQUALPack

    def getDifferentPackages(self):
        return self.__listDIFFPack

    def getExtraPackagesFromList1(self):
        return self.__list1EXTRAPack

    def getExtraPackagesFromList2(self):
        return self.__list2EXTRAPack

    def clearLists(self):
        self.__listEQUALPack.clear()
        self.__listDIFFPack.clear()
        self.__list1EXTRAPack.clear()
        self.__list2EXTRAPack.clear()


def main(argv):
        if len(argv) != 3:
                print("Appel du programme de comparaison invalide !\nIl faut 2 arguments !")
                exit(2)

        fic1InstalledDEBPack = argv[1]                  #fichier texte produit via la commande Linux : dpkg --list , depuis une machine
        fic2InstalledDEBPack = argv[2]                  #Le fichier texte produit via la commande Linux : dpkg --list , depuis une autre machine

        #instances d'objets liste de paquets Debian installés extraits de chacun des deux fichiers textes donnés en arguments
        list1OfPackages = analyseListePaquetsDeb.ListePaquets()
        list2OfPackages = analyseListePaquetsDeb.ListePaquets()

        #objet de comparaison des listes
        comparator = DebianPackageComparator()

        #chargement des objets liste de paquets Debian avec les données extraites des deux fichiers textes donnés en arguments
        list1OfPackages.loadListePaquets(fic1InstalledDEBPack)
        list2OfPackages.loadListePaquets(fic2InstalledDEBPack)

        #Comparaison des deux listes à l'aide du comparateur
        if comparator.compareLists(list1OfPackages, list2OfPackages):
                print("Les deux listes ont été comparées avec succès.\n---------------------------------\n")
                print ("a) Il y a au total " + str(len(list1OfPackages.getLstOfDebianPackages())) + " paquets Debian installés sur la machine de la première liste.")
                print ("b) Il y a au total " + str(len(list2OfPackages.getLstOfDebianPackages())) + " paquets Debian installés sur la machine de la deuxième liste.")
                print("---------------------------------\n\n")

                equalPackages = comparator.getEqualPackages()
                diffPackages = comparator.getDifferentPackages()
                extra1Packages = comparator.getExtraPackagesFromList1()
                extra2Packages = comparator.getExtraPackagesFromList2()

                if equalPackages != None and len(equalPackages) > 0:
                        analyseListePaquetsDeb.ListePaquets.creerFichierCSV(equalPackages, "EQUALPackages.csv", separator=';')
                        print("Il y a " + str(len(equalPackages)) +" paquets Debian installés sur les deux machines, avec des versions et des architecture identiques.")
                else:
                        print("Aucun des paquets installés ne sont identiques !")

                if diffPackages != None and len(diffPackages) > 0:
                        analyseListePaquetsDeb.ListePaquets.creerFichierCSV(diffPackages, "DIFFERENTPackages.csv", separator=';')
                        print("Il y a " + str(len(diffPackages)) +" paquets Debian installés sur les deux machines, mais avec des versions et/ou des architecture différentes.")
                else:
                        print("Il n'y a aucun paquets installés qui sont différents !")

                if extra1Packages != None and len(extra1Packages) > 0:
                        analyseListePaquetsDeb.ListePaquets.creerFichierCSV(extra1Packages, "EXTRAPackagesList1.csv", separator=';')
                        print("Il y a " + str(len(extra1Packages)) +" paquets Debian seulement présents dans la liste1.")
                else:
                        print("Aucun paquet Debian n'est présent seulement dans la liste 1 !")

                if extra2Packages != None and len(extra2Packages) > 0:
                        analyseListePaquetsDeb.ListePaquets.creerFichierCSV(extra2Packages, "EXTRAPackagesList2.csv", separator=';')
                        print("Il y a " + str(len(extra2Packages)) +" paquets Debian seulement présents dans la liste2.")
                else:
                        print("Aucun paquet Debian n'est présent seulement dans la liste 2 !")

        else:
                print("Problème !\nL'une des deux listes est invalide car certainement que l'un des fichiers est vide ou absent !")

if __name__ == "__main__":
        argstr = ""
        ctx = 0
        for arg in sys.argv:
                if ctx == 0:
                        argstr = arg + " "
                else:
                        argstr = argstr + arg
                        if ctx < len(sys.argv)-1:
                                argstr = argstr + ", "
                ctx += 1
        print(argstr)
        main(sys.argv)
