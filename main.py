# Module
import time
import requests
from bs4 import BeautifulSoup

# Variablen
# Link, der abgefragt werden soll
link = "https://pes.ihk.de/Auswertung.cfm?Beruf={}"

# Berufenummern aus Datei in Liste speichern
file = open(
    "berufe_nummern.txt", "r")
berufids = file.readlines()
file.close()
# Standorte in Liste speichern
file = open(
    "standorte.txt", "r")
standorte = file.readlines()
file.close()

file = open(
    "bundesland.txt", "r")
laender = file.readlines()
file.close()

bundesweit = 999


def removeLastN(string, n):  # Letzen N Zeichen aus string entfernen
    size = len(string)
    string = string[:size - n]
    return string


for berufid in berufids:
    # \n in berufid entfernen
    berufid = removeLastN(berufid, 1)

    # Abfragelink  für jede ID erstellen
    abfragelink = link.format(berufid)
    print(abfragelink)

    # Abfrage pro Bundesland oder IHK Standort
    for land in laender:
        abfrage = abfrage + "&pm1=" + \
            str(land) + "&pm2=" + str(land) + \
            "&pm3=" + str(land)  # neuer Abfragelink

    # Post Request ################################
    p = requests.post(abfragelink)
    ###############################################
    r = requests.get(abfragelink)
    # Antwort aus der Abfrage in Variable speichern
    response = r.text

    # Webantwort in Datei speichern
    savepath = "H:/temp/python/{0}.html"

    savepath = savepath.format(berufid)

    savefile = open(savepath, "w")
    savefile.write(response)
    savefile.close()
