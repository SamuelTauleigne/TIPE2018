# naif.py : Méthode naïve n'utilisant que les dernières données et effectuant une régression linéaire



import sqlite3
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
from scipy import stats


# Connection à la base de données

conn = sqlite3.connect('Database.db')
c = conn.cursor()
# Les jours doivent être donnés sous cette forme :
#d = '2018-01-30'


# Fonction de récupération des données réelles et des prévisions à l'aide de deux méthodes

def trace(r, dv, id_stand, d):
    '''trace(r, d, id_stand) renvoie les listes des données d'origine, des données de prévision
    avec les deux méthodes utilisées à l'horizon r et trace la prévision du jour, pour la station donnée.
    r est un entier strictement positif
    d est une chaine de caractères 'aaaa-mm-jj' donnant le jour de la prévision voulue'''
    # req est la requête renvoyant les données (jour, heure, av_bikes) relatives à la station désignée
    # par id_stand au jour voulu.
    req = '''SELECT jour, heure, av_bikes
             FROM VELOV
             WHERE id_stand = ?
                   AND
                   jour = ?
             '''
    # On commence le tracé en nettoyant la figure.
    plt.clf()
    # Si on veut un fond noir ...
    #plt.style.use(['dark_background'])
    # Executons la requête req :
    c.execute(req, [id_stand, d])
    # On récupère les données collectées.
    data = c.fetchall()
    # La liste times contient les dates et heures des mesures collectées.
    times = [x[0]+' '+x[1] for x in data]
    # On crée alors les listes x et y correspondant aux dates et aux mesures adaptées au tracé.
    x = [dt.datetime.strptime(t,'%Y-%m-%d %H:%M:%S') for t in times]
    y = [x[2] for x in data]
    # Ici, ce sont seulement des fonctions permettant d'avoir un affichage convenable des heures
    # et des données correspondantes.
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator())
    plt.plot(x, y, label = 'Vélos disponibles')
    plt.xlabel('Heure')
    plt.ylabel('Nombre de vélos disponibles')
    plt.title('Graphe de disponibilité à la station ' + str(id_stand) + ' : ' + str(d))
    plt.legend()
    plt.grid(True)
    plt.gcf().autofmt_xdate()
    # Il reste maintenant à tracer les régressions linéaires après calcul.
    # La liste heures contient la liste des horaires en secondes des mesures collectées.
    heures=[]
    for k in range(len(times)):
        a=int(times[k][11:13])*3600+int(times[k][14:16])*60+int(times[k][17:])
        heures.append(a)
    # On utilise le module stats afin de tracer des régressions linéaires ...
    # ... sur les r dernières mesures
    slope,intercept,r_value,p_value,std_err = stats.linregress(heures[-dv-26:-26],y[-dv-26:-26])
    fitline=[slope*x+intercept for x in heures[-dv-26:-26]]
    # ... sur toutes les mesures passées de la journée
    slope2,intercept2,r_value2,p_value2,std_err2 = stats.linregress(heures[:-26], y[:-26])
    fitline2=[slope2*x+intercept2 for x in heures[:-26]]
    # On trace les deux courbes afin d'avoir une modélisation et une prévision :
    plt.plot(x[:-26],fitline2, c='b')
    plt.plot(x[-27:-21],[slope2*k+intercept2 for k in heures[-27:-21]],c='r')
    plt.plot(x[-r-26:-26],fitline,c='b')
    plt.plot(x[-27:-21],[slope*k+intercept for k in heures[-27:-21]],c='r')
    plt.savefig('Courbe_1_0_du_' + str(d) + '_en_' + str(id_stand) + '_horizon_' + str(r) + '.png')
    # On renvoie les listes de valeurs qu'on peut vouloir récupérer.
    return y[-27:-27+r], [slope*k+intercept for k in heures[-27:-27+r]], r_value**2
