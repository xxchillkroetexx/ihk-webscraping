# Module
import time
import requests
from requests.structures import CaseInsensitiveDict

headers = CaseInsensitiveDict()

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


def removeLastN(string, n):  # Letzten N Zeichen aus string entfernen
    size = len(string)
    string = string[:size - n]
    return string


for berufid in berufids:
    # \n in berufid entfernen
    berufid = removeLastN(berufid, 1)

    # Abfragelink  für jede ID erstellen
    abfragelink = link.format(berufid)
    print(abfragelink)

    '''
    # Abfrage pro Bundesland oder IHK Standort
    for land in laender:
        abfrage = abfragelink + "&pm1=" + \
                  str(land) + "&pm2=" + str(land) + \
                  "&pm3=" + str(land)  # neuer Abfragelink
    '''

    # Post Request ################################
    # URL für Sessionstart
    url_0 = "https://pes.ihk.de/Auswertung.cfm"
    # Post-Daten
    data = {"termin": "20214", "Beruf": berufid, "action": "Beruf+w%C3%A4hlen"}

    # Session initiieren
    s = requests.session()
    s.get(url_0)
    # Post-request senden
    p = s.post(abfragelink, data)

    ###############################################
    # r = requests.get(abfragelink)

    print(p.status_code)
    # print(p.text)
    # Antwort aus der Abfrage in Variable speichern
    response = p.text
    time.sleep(1)

    # Webantwort in Datei speichern
    savepath = "H:/temp/python/{0}.html"

    savepath = savepath.format(berufid)

    savefile = open(savepath, "w")
    savefile.write(response)
    savefile.close()
