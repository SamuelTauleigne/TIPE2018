# Ce script permet la construction de la base de données,
# il ne reste plus qu'à importer les fichiers csv nécessaires.

import sqlite3

db = sqlite3.connect("BaseDonnees.db")
c = db.cursor()

c.execute("""CREATE TABLE VELOV(
statut VARCHAR(8),
bike_stands INTEGER,
id_stand INTEGER,
jour VARCHAR(42),
heure VARCHAR(42),
av_stands INTEGER,
av_bikes INTEGER,
FOREIGN KEY(id_stand) REFERENCES STATIONS(number))
;""")

c.execute("""CREATE TABLE STATIONS(
Number INTEGER,
Name VARCHAR(1515),
Address VARCHAR(1515),
Latitude REAL,
Longitude REAL)
;""")

c.execute("""CREATE TABLE DATES(
chiffres VARCHAR(12) REFERENCES VELOV(jour),
lettres VARCHAR(12))
;""")

c.execute("""CREATE TABLE METEO(
Date VARCHAR(42) REFERENCES VELOV(jour),
Heure VARCHAR(42) REFERENCES VELOV(heure),
VitesseVent REAL,
Temperature REAL,
Humidité INT,
rr1 REAL,
rr3 REAL,
rr6 REAL,
rr12 REAL,
rr24 REAL)
;""")



print(".import Sorted_Data.csv VELOV")
print(".import donnees_stations.csv STATIONS")
print(".import Dates.csv DATES")
print(".import Meteo.csv METEO")




######Ceci#aurait#pu#marcher#####
"""
import pandas

df = pandas.read_csv("Sorted_Data.csv")
df.to_sql("VELOV", db, if_exists='append', index=False)

df = pandas.read_csv("donnees_stations.csv")
df.to_sql("STATIONS", db, if_exists='append', index=False)

df = pandas.read_csv("Dates.csv")
df.to_sql("DATES", db, if_exists='append', index=False)
"""
