import csv
import unPaquet

class ListePaquets:
    def __init__(self):
        self.__paquets = []
        self.__inputFile = None
        self.__csvFile = None

    def __str__(self):
        idx = 1
        strComment = "Liste des paquets\n"
        if len(self.__paquets) > 0:
            for pqt in self.__paquets:
                if pqt != None and isinstance(pqt, unPaquet.UnPaquet):
                    strComment = strComment + f"{idx} - {pqt}\n"
                    idx += 1
        else:
            strComment = strComment + "vide."

        return strComment

    def getLstOfDebianPackages(self):
        return self.__paquets

    #Construit un fichier CSV lisible sur Excel pour présenter la liste des paquets Debian installés
    def createCSVfile(self, nomfichierSortie, separator=','):
        return ListePaquets.creerFichierCSV(self.__paquets, nomfichierSortie, ";")

    # charge un fichier texte de la liste des paquets Debian
    def loadListePaquets(self, fichier, debug=False):
        if debug:
            print("DEBUT loading")
        with open(fichier, 'r') as inputFile:
            for line in inputFile:
                ligne = line.strip()
                if len(ligne) > 0 and ligne.lower().startswith("ii "):
                    fields={"status":"", "nomPaquet":"", "version":"", "archi":"", "description":""}
                    # on doit avoir 5 champs
                    field=""
                    prevcar=''
                    cntField=0
                    for car in ligne:
                        if car != ' ' or cntField == 4:
                            field = field + str(car)
                        elif prevcar != ' ':
                            cntField += 1
                            if cntField == 1:
                                fields["status"] = field.strip()
                                if debug:
                                    print("status= ", field.strip())
                            elif cntField == 2:
                                fields["nomPaquet"] = field.strip()
                                if debug:
                                    print("nomPaquet= ", field.strip())
                            elif cntField == 3:
                                fields["version"] = field.strip()
                                if debug:
                                    print("version= ", field.strip())
                            elif cntField == 4:
                                fields["archi"] = field.strip()
                                if debug:
                                    print("archi= ", field.strip())
                              ##
                            field = ""
                        prevcar = car

                     #################################################
                    if cntField == 4:
                        cntField += 1
                        fields["description"] = field.strip()
                        if debug:
                            print("description= ", field.strip())
                    #################################################
                    if cntField == 5:
                        paquet = unPaquet.UnPaquet(fields["nomPaquet"], fields["version"], fields["archi"] , fields["description"])
                        self.__paquets.append(paquet)

        if debug:
            print("FIN loading: cntField= ", cntField, "; nb paquets=  " , str(len(self.__paquets)))

    #Affiche le contenu d'un fichier texte
    @classmethod
    def afficherFichierInput(cls, fichier):
        with open(fichier, 'r') as inputFile:
            for ligne in inputFile:
                print(ligne)

    #Construit un fichier CSV lisible sur Excel pour présenter une liste des paquets Debian
    @classmethod
    def creerFichierCSV(cls, paquets, nomfichierSortie, separator=';'):
        status=True
        if paquets != None and len(paquets) > 0:
            with open(nomfichierSortie, 'w') as fichier_output:
                writer = csv.writer(fichier_output, delimiter=separator)
                writer.writerow(['paquet', 'version', 'archi', 'description'])
                for pqt in paquets:
                    writer.writerow([pqt.getNom(), pqt.getVersion(), pqt.getArchitecture(), pqt.getDescription()])

        else:
            status = False

        return status
