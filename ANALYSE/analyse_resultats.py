# Analyse des résultats:

import Analyse_exe as ae
from math import sqrt
import matplotlib.pyplot as plt



jan=['2018-01-0'+str(k) for k in range(1,10)]+['2018-01-'+str(k) for k in range(10,32)]
jan_l=['lundi','mardi','mercredi','jeudi','vendredi','samedi','dimanche']*4+['lundi','mardi','mercredi']

dec= ['2017-12-0'+str(k) for k in range(1,10)]+['2017-12-'+str(k) for k in range(10,32)]
dec_l= ['vendredi','samedi','dimanche','lundi','mardi','mercredi','jeudi']*4+['vendredi','samedi','dimanche']

nov= ['2017-11-0'+str(k) for k in range(1,10)]+['2017-11-'+str(k) for k in range(10,31)]
nov_l=['mercredi','jeudi','vendredi','samedi','dimanche','lundi','mardi']*4+['mercredi','jeudi']

octo= ['2017-10-0'+str(k) for k in range(1,10)]+['2017-10-'+str(k) for k in range(10,32)]
octo_l=['dimanche','lundi','mardi','mercredi','jeudi','vendredi','samedi']*4+['dimanche','lundi','mardi']

sep=['2017-09-0'+str(k) for k in range(1,10)]+['2017-09-'+str(k) for k in range(10,31)]
sep_l= ['vendredi','samedi','dimanche','lundi','mardi','mercredi','jeudi']*4+['vendredi','samedi']

jours= jan
jours_l= jan_l

def moy_liste(val_list):
    """Calcule la moyenne des entiers donnés en entrée sous forme de liste."""
    n = len(val_list)
    s = 0
    for x in val_list:
        s += x
    return s/n

def ecart_type(liste):
    n=len(liste)
    m=moy_liste(liste)
    s=0
    for k in range(n):
        s+=(liste[k]-m)**2
    return sqrt(s/n)


def rmse(obs,prev):
    H= len(prev)
    s=0
    for h in range(H):
        m=(obs[h]-prev[h])**2
        s+=m
    return (s/H)**(1/2)


# Tri Fusion

def split(l):
    if l == []:
        return [], []
    elif len(l) == 1:
        return l, []
    else:
        x = l[0]
        y = l[1]
        r = l[2:]
        l1, l2 = split(r)
        return [x]+l1, [y]+l2

def fusion(l1, l2):
    if l1 == []:
        return l2
    elif l2 == []:
        return l1
    else:
        x = l1[0]
        y = l2[0]
        if x < y:
            return [x]+fusion(l1[1:], l2)
        else:
            return [y]+fusion(l1, l2[1:])

def tri_fusion(l):
    n = len(l)
    if n <= 1:
        return l
    else:
        l1, l2 = split(l)
        return fusion(tri_fusion(l1), tri_fusion(l2))


# Médiane

def mediane(liste):
    triee = tri_fusion(liste)
    n = len(triee)
    if n%2 == 0:
        return 0.5*(triee[n//2]+triee[n//2+1])
    return triee[n//2]


# Efficacité

def eff_rmse(r,dv, id_stand, jours, jours_l):
    """retourne la moyenne des erreurs pour tous les jours à une même heure avec la méthode naïve"""
    n=len(jours)
    naif1=[]
    naif2=[]
    meth2=[]
    meth3=[]
    for i in range(n):
        j=jours[i]
        jl=jours_l[i]
        obs,prev1,prev2= ae.trace(r,dv, id_stand,j)
        naif1.append(rmse(obs,prev1))
        naif2.append(rmse(obs,prev2))
        prevm2=ae.trace2(id_stand, r,jl,j)
        meth2.append(rmse(obs,prevm2))
        #print('ii')
        prev3=ae.trace3(r,jl,j, id_stand)
        meth3.append(rmse(obs,prev3))
        #print('iii')
    '''x=[k for k in range(1,len(jours)+1)]
    plt.clf()
    plt.scatter(x,naif1,c='red',label='Naif r dernières valeurs')
    plt.scatter(x,naif2, c='orange', label='Naif journée entière')
    plt.scatter(x,meth2,c='b',label='saisons')
    plt.scatter(x,meth3,c='g',label='similarités')
    plt.title('Comparaisons des efficacités')
    plt.legend()
    plt.savefig('comparason_eff.png')'''
    return ('1', moy_liste(naif1), ecart_type(naif1), mediane(naif1)), ('2', moy_liste(naif2), ecart_type(naif2), mediane(naif2)), ('3', moy_liste(meth2), ecart_type(meth2), mediane(meth2)), ('4', moy_liste(meth3), ecart_type(meth3), mediane(meth3))
        
#('naif1',moy_liste(naif1), ecart_type(naif1)),
#('naif2',moy_liste(naif2), ecart_type(naif2)),
#('saison',moy_liste(meth2), ecart_type(meth2)),
#('similarite',moy_liste(meth3),ecart_type(meth3))


def all_res():
    # Comparaison des 4 méthodes à très court terme
    with open('res1.dat', 'w') as f:
        l1, l2, l3, l4 = eff_rmse(1, 3, 8054, jan, jan_l)
        for x in [l1, l2, l3, l4]:
            f.write(str(x[0]) + ' ' + str(x[1]) + ' ' + str(x[2]) + '\n')
    # Comparaison des 4 méthodes à moyen terme
    with open('res6.dat', 'w') as f:
        l1, l2, l3, l4 = eff_rmse(6, 3, 8054, jan, jan_l)
        for x in [l1, l2, l3, l4]:
            f.write(str(x[0]) + ' ' + str(x[1]) + ' ' + str(x[2]) + '\n')
    # Comparaison des 4 méthodes à long terme
    with open('res15.dat', 'w') as f:
        l1, l2, l3, l4 = eff_rmse(15, 3, 8054, jan, jan_l)
        for x in [l1, l2, l3, l4]:
            f.write(str(x[0]) + ' ' + str(x[1]) + ' ' + str(x[2]) + '\n')
