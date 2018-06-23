import sqlite3
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

conn = sqlite3.connect('Database.db')
c = conn.cursor()

# Données

lmm = '8054'
day_l = 'mardi'
day_c = '2018-01-30'
# Heure du dernier relevé
hour = '15:00:00'
# Nombre de jours précédents dans notre base de données
r = 125

# Recherche de semblables

# Requête renvoyant les données de la journée
tem = """SELECT AVG(av_bikes)
         FROM VELOV
         WHERE jour = ? AND heure >= ? AND heure < ? AND id_stand = ?
         """

hours_tem = ['00:00:00', '00:30:00', '01:00:00', '01:30:00', '02:00:00', '02:30:00',
             '03:00:00', '03:30:00', '04:00:00', '04:30:00', '05:00:00', '05:30:00',
             '06:00:00', '06:30:00', '07:00:00', '07:30:00', '08:00:00', '08:30:00',
             '09:00:00', '09:30:00', '10:00:00', '10:30:00', '11:00:00', '11:30:00',
             '12:00:00', '12:30:00', '13:00:00', '13:30:00', '14:00:00', '14:30:00',
             '15:00:00']

# Requête renvoyant la liste des disponibilités moyennes de chaque jour
req = """SELECT AVG(av_bikes), jour
         FROM VELOV
         WHERE id_stand = ? AND jour < ? AND ? <= heure AND heure < ?
         GROUP BY jour
         """

hours_list = ['0'+ str(k) + ':00:00' for k in range(10)] + [str(k) + ':00:00' for k in range(10, 24)] + ['0'+ str(k) + ':30:00' for k in range(10)] + [str(k) + ':30:00' for k in range(10, 24)]
hours_list = sorted(hours_list)

# Calculons la moyenne des valeurs d'une liste d'entiers
def average(val_list):
    """Calcule la moyenne des entiers donnés en entrée sous forme de liste."""
    n = len(val_list)
    s = 0
    for x in val_list:
        s += x
    return s/n



# Tracé

# res0 contient les valeurs du jour témoin (celui qu'on étudie) pour chaque tranche horaire
n = len(hours_tem)
res0 = []
for k in range(n-1):
    T0 = hours_tem[k]
    T1 = hours_tem[k+1]
    c.execute(tem, [day_c, T0, T1, lmm])
    res = c.fetchall()
    res0.append(res[0][0])


# Initialisation de la liste des écarts : Première tranche horaire
step = [] # Liste des écarts : on ajoute à chaque fois le carré de la différence !
t1 = hours_list[0]
t2 = hours_list[1]
c.execute(req, [lmm, day_c, t1, t2])
ans = c.fetchall()[-r:] # On prend les valeurs des r derniers jours.
ini = res0[0]
if ini != None:
    for k in range(r):
        step.append((ans[k][0]-ini)**2)


# Hérédité
for k in range(1, n-1):
    t1 = hours_list[k]
    t2 = hours_list[k+1]
    c.execute(req, [lmm, day_c, t1, t2])
    ans = c.fetchall()[-r:]
    ini = res0[k]
    if ini != None:
        for l in range(r):
            step[l] += (ans[l][0]-ini)**2 # step[l] contient la somme des carrés des écarts pour chaque jour
            # On pourra alors chercher le jour le plus proche du jour témoin étudié !

# Recherche du minimum et de son indice
def minimum(liste):
    n = len(liste)
    assert n > 0
    i_min = 0
    min_step = liste[0]
    for k in range(1, n):
        if step[k] <= min_step:
            # inférieur ou égal : on prend la valeur la plus récente
            i_min = k
            min_step = step[k]
    return (i_min, min_step)

# Traçons !
i_min = minimum(step)[0]
date = ans[i_min][1]

# On trace le graphe du jour semblable déterminé précédemment :
req = """SELECT heure, av_bikes
         FROM VELOV
         WHERE id_stand = ? AND jour = ?
         """

c.execute(req, [lmm, date])
vect = c.fetchall()
vect_1 = [x[0] for x in vect] # Les heures
vect_2 = [x[1] for x in vect] # Les disponibilités

plt.clf()
# plt.style.use(['dark_background'])
x = [dt.datetime.strptime(t,'%H:%M:%S') for t in vect_1]
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H'))
plt.gca().xaxis.set_major_locator(mdates.HourLocator())
plt.plot(x, vect_2, label = 'Vélos disponibles')
plt.xlabel('Heure')
plt.ylabel('Nombre de vélos disponibles')
plt.title('Graphe de disponibilité à la station ' + lmm + ' : ' + day_c)
plt.legend()
plt.grid(True)
plt.gcf().autofmt_xdate()
#plt.show()
plt.savefig('Courbe_3_du_' + day_c + '_en_' + lmm + '.png')
# Horizon
r = 5
prev = vect_2[-27: -27+r]
