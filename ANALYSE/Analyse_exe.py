# Analyse_exe.py : Comporte un préliminaire à l'analyse des méthodes de prévision



import sqlite3
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
from scipy import stats


# Connection à la base de donnée
conn = sqlite3.connect('Database.db')
c = conn.cursor()


#############################################
########## Méthode naïve :

# Requête
# Cette requête permet de recolter les informations de disponibilité relatives
# à un jour et à une heure donnée.
req_naive = '''SELECT jour, heure, av_bikes
               FROM VELOV
               WHERE id_stand = ?
                     AND
                     jour = ?
               '''

def trace(r, dv, id_station, d):
    """trace(r, dv, id_station, d) renvoie les listes des données originales
    et des deux méthodes naïves de prédiction au jour d avec
    un paramêtre de régression linéaire dv à un horizon r."""
    c.execute(req_naive, [id_station, d])
    data = c.fetchall()
    times = [x[0]+' '+x[1] for x in data]
    x = [dt.datetime.strptime(t,'%Y-%m-%d %H:%M:%S') for t in times]
    y = [x[2] for x in data]

    heures=[]
    for k in range(len(times)):
        a=int(times[k][11:13])*3600+int(times[k][14:16])*60+int(times[k][17:])
        heures.append(a)

    slope,intercept,r_value,p_value,std_err = stats.linregress(heures[-dv-26:-26],y[-dv-26:-26])
    fitline=[slope*x+intercept for x in heures[-dv-26:-26]]

    slope2,intercept2,r_value2,p_value2,std_err2 = stats.linregress(heures[:-26], y[:-26])
    fitline2=[slope2*x+intercept2 for x in heures[:-26]]
    
    return y[-27:-27+r], [slope*k+intercept for k in heures[-27:-27+r]], [slope2*k+intercept2 for k in heures[-27:-27+r]]




# Calcul de la moyenne des valeurs d'une liste d'entiers
def average(val_list):
    """Calcule la moyenne des entiers donnés en entrée sous forme de liste."""
    n = len(val_list)
    s = 0
    for x in val_list:
        s += x
    return s/n




# Méthode 2

# Requête

req2 = """SELECT av_bikes
         FROM VELOV JOIN DATES ON jour = chiffres
         WHERE lettres = ? AND id_stand = ? AND jour < ? AND ? <= heure AND heure < ?
         """

hours_list = ['0'+ str(k) + ':00:00' for k in range(10)] + [str(k) + ':00:00' for k in range(10, 24)] + ['0'+ str(k) + ':30:00' for k in range(10)] + [str(k) + ':30:00' for k in range(10, 24)]
hours_list = sorted(hours_list)
n = len(hours_list)
lmm = '8054'



def trace2(id_stand, r, day_l, day_c):
    les_t = []
    les_dispos = []
    for k in range(n-1):
        t1 = hours_list[k]
        t2 = hours_list[k+1]
        # On exécute la requête pour chaque tranche d'une demi-heure.
        c.execute(req2, [day_l, id_stand, day_c, t1, t2])
        ans = c.fetchall()
        # on réécrit correctement le résultat de la requête.
        ans = [x[0] for x in ans]
        h = t1[:2]
        # Pour construire les_t, je trace toutes les demi-heure en notant au milieu donc 15 ou 45.
        if t1[3] == '0':
            les_t.append(h + ':15:00')
        else:
            les_t.append(h + ':45:00')
        # Pour construire les_dispos, je calcule la moyenne de toutes les dispos données par la requête.
        les_dispos.append(average(ans))
    prev = les_dispos[-27:-27+r]
    return prev




# Recherche du minimum et de son indice
def minimum(liste):
    n = len(liste)
    assert n > 0
    i_min = 0
    min_step = liste[0]
    for k in range(1, n):
        if liste[k] <= min_step:
            # inférieur ou égal : on prend la valeur la plus récente
            i_min = k
            min_step = liste[k]
    return (i_min, min_step)





# Méthode 3 :

# Heure du dernier relevé
hour = '15:00:00'
# Nombre de jours précédents dans notre base de données
r = 25


# Requête

# Requête renvoyant les données de la journée
tem = """SELECT AVG(av_bikes)
             FROM VELOV
             WHERE jour = ? AND heure >= ? AND heure < ? AND id_stand = ?
             """

hours_tem = ['00:00:00', '00:30:00', '01:00:00', '01:30:00', '02:00:00', '02:30:00', '03:00:00', '03:30:00', '04:00:00', '04:30:00', '05:00:00', '05:30:00', '06:00:00', '06:30:00', '07:00:00', '07:30:00', '08:00:00', '08:30:00', '09:00:00', '09:30:00', '10:00:00', '10:30:00', '11:00:00', '11:30:00', '12:00:00', '12:30:00', '13:00:00', '13:30:00', '14:00:00', '14:30:00', '15:00:00']

# Requête renvoyant la liste des disponibilités moyennes de chaque jour
req3 = """SELECT AVG(av_bikes), jour
             FROM VELOV
             WHERE id_stand = ? AND jour < ? AND ? <= heure AND heure < ?
             GROUP BY jour
             """

hours_list = ['0'+ str(k) + ':00:00' for k in range(10)] + [str(k) + ':00:00' for k in range(10, 24)] + ['0'+ str(k) + ':30:00' for k in range(10)] + [str(k) + ':30:00' for k in range(10, 24)]
hours_list = sorted(hours_list)


n = len(hours_tem)


req3bis = """SELECT heure, av_bikes
             FROM VELOV
             WHERE id_stand = ? AND jour = ?
             """



def trace3(w, day_l, day_c, id_stand):
    
    # res0 contient les valeurs du jour témoin (celui qu'on étudie) pour chaque tranche horaire
    res0 = []
    for k in range(n-1):
        T0 = hours_tem[k]
        T1 = hours_tem[k+1]
        c.execute(tem, [day_c, T0, T1, id_stand])
        res = c.fetchall()
        res0.append(res[0][0])
    
    # Initialisation de la liste des écarts : Première tranche horaire
    step = [] # Liste des écarts : on ajoute à chaque fois le carré de la différence !
    t1 = hours_list[0]
    t2 = hours_list[1]
    c.execute(req3, [id_stand, day_c, t1, t2])
    ans = c.fetchall()[-r:] # On prend les valeurs des r derniers jours.
    ini = res0[0]
    if ini != None:
        for k in range(r):
            step.append((ans[k][0]-ini)**2)

    # Hérédité
    for k in range(1, n-1):
        t1 = hours_list[k]
        t2 = hours_list[k+1]
        c.execute(req3, [id_stand, day_c, t1, t2])
        ans = c.fetchall()[-r:]
        ini = res0[k]
        if ini != None:
            for l in range(r):
                step[l] += (ans[l][0]-ini)**2 # step[l] contient la somme des carrés des écarts pour chaque jour
                # On pourra alors chercher le jour le plus proche du jour témoin étudié !

    # Traçons !
    i_min = minimum(step)[0]
    date = ans[i_min][1]

    # On trace le graphe du jour semblable déterminé précédemment :

    c.execute(req3bis, [id_stand, date])
    vect = c.fetchall()
    vect_1 = [x[0] for x in vect] # Les heures
    vect_2 = [x[1] for x in vect] # Les disponibilités

    prev = vect_2[-27:-27+w]
    return prev







# Méthode 3 bis :

# Heure du dernier relevé
hour = '15:00:00'
# Nombre de jours précédents dans notre base de données
r = 110
# dv est le nombre de demi-heures considérées

# Requête

# Requête renvoyant les données de la journée
tem = """SELECT AVG(av_bikes)
             FROM VELOV
             WHERE jour = ? AND heure >= ? AND heure < ? AND id_stand = ?
             """

hours_tem = ['00:00:00', '00:30:00', '01:00:00', '01:30:00', '02:00:00', '02:30:00', '03:00:00', '03:30:00', '04:00:00', '04:30:00', '05:00:00', '05:30:00', '06:00:00', '06:30:00', '07:00:00', '07:30:00', '08:00:00', '08:30:00', '09:00:00', '09:30:00', '10:00:00', '10:30:00', '11:00:00', '11:30:00', '12:00:00', '12:30:00', '13:00:00', '13:30:00', '14:00:00', '14:30:00', '15:00:00']

# Requête renvoyant la liste des disponibilités moyennes de chaque jour
req3 = """SELECT AVG(av_bikes), jour
             FROM VELOV
             WHERE id_stand = ? AND jour < ? AND ? <= heure AND heure < ?
             GROUP BY jour
             """

hours_list = ['0'+ str(k) + ':00:00' for k in range(10)] + [str(k) + ':00:00' for k in range(10, 24)] + ['0'+ str(k) + ':30:00' for k in range(10)] + [str(k) + ':30:00' for k in range(10, 24)]
hours_list = sorted(hours_list)


n = len(hours_tem)


req3bis = """SELECT heure, av_bikes
             FROM VELOV
             WHERE id_stand = ? AND jour = ?
             """



def trace3bis(w, dv, day_l, day_c, id_stand):
    
    # res0 contient les valeurs du jour témoin (celui qu'on étudie) pour chaque tranche horaire
    res0 = []
    for k in range(n-1-dv, n-1):
        T0 = hours_tem[k]
        T1 = hours_tem[k+1]
        c.execute(tem, [day_c, T0, T1, id_stand])
        res = c.fetchall()
        res0.append(res[0][0])
    
    # Initialisation de la liste des écarts : Première tranche horaire
    step = [] # Liste des écarts : on ajoute à chaque fois le carré de la différence !
    t1 = hours_list[n-dv-1]
    t2 = hours_list[n-dv]
    c.execute(req3, [id_stand, day_c, t1, t2])
    ans = c.fetchall()[-r:] # On prend les valeurs des r derniers jours.
    ini = res0[0]
    if ini != None:
        for k in range(r):
            step.append((ans[k][0]-ini)**2)

    # Hérédité
    for k in range(n-dv, n-1):
        t1 = hours_list[k]
        t2 = hours_list[k+1]
        c.execute(req3, [id_stand, day_c, t1, t2])
        ans = c.fetchall()[-r:]
        ini = res0[k-n+dv+1]
        if ini != None:
            for l in range(r):
                step[l] += (ans[l][0]-ini)**2 # step[l] contient la somme des carrés des écarts pour chaque jour
                # On pourra alors chercher le jour le plus proche du jour témoin étudié !

    # Traçons !
    i_min = minimum(step)[0]
    date = ans[i_min][1]

    # On trace le graphe du jour semblable déterminé précédemment :

    c.execute(req3bis, [id_stand, date])
    vect = c.fetchall()
    vect_1 = [x[0] for x in vect] # Les heures
    vect_2 = [x[1] for x in vect] # Les disponibilités

    prev = vect_2[-27:-27+w]
    return prev
