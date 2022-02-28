import sys
import unPaquet
import analyseListePaquetsDeb

def main(argv):
    listOfPackages = analyseListePaquetsDeb.ListePaquets()

    #analyseListePaquetsDeb.ListePaquets.afficherFichierInput(argv[1])

    listOfPackages.loadListePaquets(argv[1])

    print (f"Les paquets chargés:\n {listOfPackages}")

    listOfPackages.createCSVfile(argv[2], ';')

    analyseListePaquetsDeb.ListePaquets.afficherFichierInput(argv[2])

if __name__ == "__main__":
    argstr = ""
    ctx = 0
    for arg in sys.argv:
        argstr = argstr + arg
        if ctx < len(sys.argv):
            argstr = argstr + ", "
        ctx += 1
    print(argstr)
    main(sys.argv)