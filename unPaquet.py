class UnPaquet:
    def __init__(self, nom, version, archi, description):
        self.__nom = nom
        self.__version = version
        self.__archi = archi
        self.__description = description

    def __str__(self):
        return self.__nom + "   " + self.__version + "   " + self.__archi + "   " + self.__description

    def getNom(self):
        return self.__nom
    def getVersion(self):
        return self.__version
    def getArchitecture(self):
        return self.__archi
    def getDescription(self):
        return self.__description