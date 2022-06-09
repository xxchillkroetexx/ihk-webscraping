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
    session = requests.session()
    session.get(url_0)
    # Post-request senden
    # Beruf und Termin wird ausgewählt
    post = session.post(abfragelink, data)
    # Alle Länder mit dem "Ländervergleich" abrufen
    url_vergleich = "https://pes.ihk.de/laedervergleich.cfm"
    vergleich = session.get(url_vergleich)

    print(post.status_code)

    # Antwort aus der Abfrage in Variable speichern
    response = vergleich.text

    time.sleep(1)

    # Webantwort in Datei speichern
    savepath = "H:/temp/python/{0}-{1}-{2}.html"
    savepath = savepath.format(berufid, termin, bundesweit)
    savefile = open(savepath, "w")
    savefile.write(response)
    savefile.close()

    print("file saved! - Bund")

    # Auswertung mit Pandas - IN ARBEIT -
    tables = pd.read_html(response)
    print(tables[0])
    print(tables[1])

    """
    # Abfrage der IHK-Standorte
    for standort in standorte:
        # Zeilenumbruch entfernen
        land = removeLastN(land, 1)
        # neuer Abfragelink
        requrl = abfragelink + "&pm1=" + str(standort) + "&pm2=" + str(standort) + "&pm3=" + str(standort)
        print(requrl)

        # GET-Request an Server stellen
        get = session.get(requrl)
        getresponse = get.text
        print(get.status_code)
        time.sleep(1)
        # Webantwort in Datei speichern
        savepath = "H:/temp/python/{0}-{1}-{2}.html"
        savepath = savepath.format(berufid, termin, land)
        savefile = open(savepath, "w")
        savefile.write(getresponse)
        savefile.close()

        print("file saved! - " + savepath)
    """