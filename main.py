# Module
import csv
import sys
import time
import requests
from requests.structures import CaseInsensitiveDict
import pandas as pd
import mariadb

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

# CSV-File erstellen, das in die Datenbank geschrieben werden soll
toWrite = [
    ["berufID", "standortID", "pruefung", "teilnehmeranzahl", "bestanden", "noteEins", "noteZwei", "noteDrei",
     "noteVier", "noteFuenf", "noteSechs"]
]
file = open("ihkData.csv", "w")
with file:
    writer = csv.writer(file)
    for row in toWrite:
        writer.writerow(row)
file.close()


# Letzten N Zeichen aus string entfernen
def removeLastN(string, n):
    size = len(string)
    string = string[:size - n]
    return string


for termin in termine:

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

            # Daten aus Frame auswählen
            # selectedValue = df.iat[Zeile, Spalte]
            berufID = berufid
            standortID = land
            pruefung = termin
            teilnehmeranzahl = df.iat[2, 2]
            bestanden = df.iat[3, 2]
            noteEins = df.iat[6, 2]
            noteZwei = df.iat[7, 2]
            noteDrei = df.iat[8, 2]
            noteVier = df.iat[9, 2]
            noteFuenf = df.iat[10, 2]
            noteSechs = df.iat[11, 2]

            # ihkData.csv mit Daten füllen
            toWrite = [
                [berufID, standortID, pruefung, teilnehmeranzahl, bestanden, noteEins, noteZwei, noteDrei, noteVier,
                 noteFuenf, noteSechs]
            ]

            file = open("ihkData.csv", "a")

            with file:
                writer = csv.writer(file)

                for row in toWrite:
                    writer.writerow(row)
            file.close()

            print("Daten an CSV angehängt!")

# CSV in DB schreiben
# Verbindung zur Datenbank herstellen
try:
    conn = mariadb.connect(
        host="127.0.0.1",
        port=3306,
        user="admin",
        password="admin")
except mariadb.Error as e:
    print(f"Error connecting to the database: {e}")
    sys.exit(1)

# Cursor wird für die Kommunikation genutzt
cursor = conn.cursor()

# Verbindung nutzen
sql_createTable = "CREATE TABLE IF NOT EXISTS ihk." + termin \
                  + " (" \
                    "id INT PRIMARY KEY AUTO_INCREMENT, " \
                    "berufID INT(15), " \
                    "standortID INT(5), " \
                    "pruefung INT(5), " \
                    "teilnehmeranzahl INT(10), " \
                    "bestanden INT(10), " \
                    "noteEins INT(10)" \
                    "noteZwei INT(10)" \
                    "noteDrei INT(10)" \
                    "noteVier INT(10)" \
                    "noteFuenf INT(10)" \
                    "noteSechs INT(10)" \
                    ") ENGINE=InnoDB;"

cursor.execute(sql_createTable)

# Verbindung zur Datenbank schließen
conn.close()

###
# Datenbank modellieren - Kommentare/Vorschläge ausstehend
# Verbindung mit MariaDB herstellen
# Felder aus Dataframe in MariaDB schreiben
# Skalieren -> Jahre abfragen; Standorte anfragen
###
