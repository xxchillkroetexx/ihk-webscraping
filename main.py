# Module
import time
import requests
from bs4 import BeautifulSoup

# Variablen
link = "https://pes.ihk.de//Auswertung.cfm?Beruf={}"

# Code
# Berufenummern aus Datei in Liste speichern
idfile = open(
    "H:/Nextcloud/Dokumente/Programming/Python/webscraping/berufe_nummern.txt", "r")
berufids = idfile.readlines()
idfile.close()

for berufid in berufids:
    # Abfragelink  für jede ID erstellen
    abfrage = link.format(berufid)

    # Abfrage pro Bundesland oder IHK Standort
    for zeile in ihkliste:
        abfrage = abfrage + "&pm=" + \
            str(zeile) + "&pm=" + str(zeile) + \
            "&pm=" + str(zeile)  # neuer Abfragelink
    # Webabfrage erstellen
    r = requests.get(abfrage)
    # Antwort aus der Abfrage in Variable speichern
    response = r.text

    # Webantwort in Datei für später speichern
    savefile = open("H:/temp/python/{0}.txt".format(berufid), "w")
    savefile.write(response)
    savefile.close()

    # 5 Sekunden warten, bis nächste Abfrage ausgeführt wird
    time.sleep(5)
