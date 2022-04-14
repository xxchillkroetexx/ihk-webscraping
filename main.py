# Module
import time
import requests
from bs4 import BeautifulSoup

# Variablen
# Link, der abgefragt werden soll
link = "https://pes.ihk.de//Auswertung.cfm?Beruf={}"


# Code
# Berufenummern aus Datei in Liste speichern
idfile = open(
    "H:/Nextcloud/Dokumente/Programming/Python/webscraping/berufe_nummern.txt", "r")
berufids = idfile.readlines()
idfile.close()


def removeLastN(string, n):  # Letzen N Zeichen aus string entfernen
    size = len(string)
    string = string[:size - n]
    return string


for berufid in berufids:
    # \n in berufid entfernen
    berufid = removeLastN(berufid, 1)

    # Abfragelink  für jede ID erstellen
    abfrage = link.format(berufid)
    print(abfrage)
    # Abfrage pro Bundesland oder IHK Standort
    # for zeile in ihkliste:
    #    abfrage = abfrage + "&pm=" + \
    #        str(zeile) + "&pm=" + str(zeile) + \
    #        "&pm=" + str(zeile)  # neuer Abfragelink

    # Webabfrage erstellen
    r = requests.get(abfrage)
    # Antwort aus der Abfrage in Variable speichern
    response = r.text

    # Webantwort in Datei speichern
    savepath = "H:/temp/python/{0}.html"

    savepath = savepath.format(berufid)

    savefile = open(savepath, "w")
    savefile.write(response)
    savefile.close()
