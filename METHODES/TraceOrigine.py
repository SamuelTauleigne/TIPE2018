# TraceOrigine.py : Permet de tracer la courbe de disponibilité de vélos un jour donné



import sqlite3
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates


# Connection à la base de données
conn = sqlite3.connect('Database.db')
c = conn.cursor()

d = '2018-01-30'


# Pour tracer la vraie courbe du jour que tu veux tester :

def trace(d, id_stand):
    """trace(d, id_stand) enregistre la courbe des disponibilités du jour souhaité à la station donnée"""
    # Cette requête permet d'obtenir la liste des données exactes
    # (nombre de vélos disponibles à chaque heure du jour d).
    req = '''SELECT jour, heure, av_bikes
             FROM VELOV
             WHERE id_stand = ?
                   AND
                   jour = ?
             '''
    # Tracé
    plt.clf()
    # On execute la requête et on recupère la liste des données.
    c.execute(req, [id_stand, d])
    data = c.fetchall()
    # Gestion du tracé en fonction du temps
    times = [x[0]+' '+x[1] for x in data]
    x = [dt.datetime.strptime(t,'%Y-%m-%d %H:%M:%S') for t in times]
    y = [x[2] for x in data]
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator())
    plt.plot(x, y, label = 'Vélos disponibles')
    plt.xlabel('Heure')
    plt.ylabel('Vélos disponibles')
    plt.title('Graphe de disponibilité original à la station ' + str(id_stand) +' : ' + str(d))
    plt.legend()
    plt.grid(True)
    plt.gcf().autofmt_xdate()
    plt.savefig('Courbe_0_du_' + str(d) + '_en_' + str(id_stand) + '.png')
