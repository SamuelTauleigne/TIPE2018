import sqlite3
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


conn = sqlite3.connect('Database.db')
c = conn.cursor()


# Données

lmm = '8054'
#day_l, day_c = input(), input()
day_l = 'mardi'
day_c = '2018-01-30'

print('Ceci applique la méthode 2 à la station ' + lmm + ' le ' + day_l + ' ' + day_c)


# Requête renvoyant la liste des disponibilités de tous les jours précédents correspondant au même jour de la semaine
req = """SELECT av_bikes
         FROM VELOV JOIN DATES ON jour = chiffres
         WHERE lettres = ? AND id_stand = ? AND jour < ? AND ? <= heure AND heure < ?
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

les_t = []
les_dispos = []
n = len(hours_list)
for k in range(n-1):
    t1 = hours_list[k]
    t2 = hours_list[k+1]
    # On exécute la requête pour chaque tranche d'une demi-heure.
    c.execute(req, [day_l, lmm, day_c, t1, t2])
    ans = c.fetchall()
    # On réécrit correctement le résultat de la requête.
    ans = [x[0] for x in ans]
    h = t1[:2]
    # Pour construire les_t, je trace toutes les demi-heures en notant au milieu donc 15 ou 45.
    if t1[3] == '0':
        les_t.append(h + ':15:00')
    else:
        les_t.append(h + ':45:00')
    # Pour construire les_dispos, je calcule la moyenne de toutes les dispos données par la requête.
    les_dispos.append(average(ans))

plt.clf()
# plt.style.use(['dark_background'])
x = [dt.datetime.strptime(t,'%H:%M:%S') for t in les_t]
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H'))
plt.gca().xaxis.set_major_locator(mdates.HourLocator())
plt.plot(x, les_dispos, label = 'Vélos disponibles')
plt.xlabel('Heure')
plt.ylabel('Nombre de vélos disponibles')
plt.title('Graphe de disponibilité à la station ' + lmm + ' : ' + day_c)
plt.legend()
plt.grid(True)
plt.gcf().autofmt_xdate()
#plt.show()
plt.savefig('Courbe_2_du_' + day_c + '_en_' + lmm + '.png')
# Horizon
r = 5
print('A horizon ' + str(r))
prev = les_dispos[-27:-27+r]
