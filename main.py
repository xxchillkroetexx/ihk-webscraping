# Module
import time
import requests
from requests.structures import CaseInsensitiveDict
import pandas as pd

headers = CaseInsensitiveDict()

# Variablen
# Link, der abgefragt werden soll
link = "https://pes.ihk.de/Auswertung.cfm?Beruf={}"

# Berufenummern aus Datei in Liste speichern
file = open("berufe_nummern.txt", "r")
berufids = file.readlines()
file.close()
# Standorte in Liste speichern
file = open("standorte.txt", "r")
standorte = file.readlines()
file.close()
# Bundesländer in Liste speichern
file = open("bundesland.txt", "r")
laender = file.readlines()
file.close()

bundesweit = 999

# Prüfungszeitpunkte in Liste speichern
file = open("termine.txt", "r")
termine = file.readlines()
file.close()


# Letzten N Zeichen aus string entfernen
def removeLastN(string, n):
    size = len(string)
    string = string[:size - n]
    return string


for berufid in berufids:
    # \n in berufid entfernen
    berufid = removeLastN(berufid, 1)
    print(berufid)

    # Abfragelink  für jede ID erstellen
    abfragelink = link.format(berufid)

    # Post Request
    # Post-Daten
    termin = "20214"
    data = {"termin": termin, "Beruf": berufid, "action": "Beruf+w%C3%A4hlen"}
    # URL für Sessionstart
    url_0 = "https://pes.ihk.de/Auswertung.cfm"
    # Session initiieren
    s = requests.session()
    s.get(url_0)
    # Post-request senden
    p = s.post(abfragelink, data)
    print(p.status_code)
    # Antwort aus der Abfrage in Variable speichern
    postresponse = p.text

    time.sleep(1)

    """
    # Webantwort in Datei speichern
    savepath = "H:/temp/python/{0}-{1}-{2}.html"
    savepath = savepath.format(berufid, termin, bundesweit)
    savefile = open(savepath, "w")
    savefile.write(postresponse)
    savefile.close()
    """

    print("file saved! - Bund")
    # Abfrage der Länder und IHK-Standorte
    for land in laender:
        # Zeilenumbruch entfernen
        land = removeLastN(land, 1)
        # neuer Abfragelink
        requrl = abfragelink + "&pm1=" + str(land) + "&pm2=" + str(land) + "&pm3=" + str(land)
        print(requrl)

        # GET-Request an Server stellen
        get = s.get(requrl)
        getresponse = get.text
        print(get.status_code)
        time.sleep(1)
        """
        # Webantwort in Datei speichern
        savepath = "H:/temp/python/{0}-{1}-{2}.html"
        savepath = savepath.format(berufid, termin, land)
        savefile = open(savepath, "w")
        savefile.write(getresponse)
        savefile.close()

        print("file saved! - " + savepath)
        """
        print("Tabelle wird in Datenbank gespeichert!")
        tables = pd.read_html(getresponse)
        # df => Dataframe
        df = tables[1]

        ###
        # Datenbank modellieren - Kommentare/Vorschläge ausstehend
        # Verbindung mit MariaDB herstellen
        # Felder aus Dataframe in MariaDB schreiben
        # Skalieren -> Jahre abfragen; Standorte anfragen
        ###
