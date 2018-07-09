# Analyse_res.py : Analyse les résultats obtenus par chacune des méthodes sur des journées données



import Analyse_exe as exe # On importe les fonctions permettant d'avoir les résultats de tracé pour chaque méthode.


dates = [('samedi', '2018-01-27'), ('dimanche', '2018-01-28'), ('lundi', '2018-01-29')] # liste des dates considérées

dv = 25
r = 5 # horizon de prévision

[e1, e2, e3, e4] = [0, 0, 0, 0]
[f1, f2, f3, f4] = [0, 0, 0, 0]

# Parcours de la liste 'dates' :
for d in dates:
    # Collecte des données
    orig, naif1, naif2 = exe.trace(r, dv, d[1])
    method2 = exe.trace2(r, d[0], d[1])
    method3 = exe.trace3(r, d[0], d[1])
    
    for k in range(15, r):
        
        tem = orig[k]
        
        n1 = (tem - naif1[k])**2
        n2 = (tem - naif2[k])**2
        m2 = (tem - method2[k])**2
        m3 = (tem - method3[k])**2
        
        n11 = abs(tem - naif1[k])
        n22 = abs(tem - naif2[k])
        m22 = abs(tem - method2[k])
        m33 = abs(tem - method3[k])
        
        e1 += n1
        e2 += n2
        e3 += m2
        e4 += m3
        
        f1 += n11/tem
        f2 += n22/tem
        f3 += m22/tem
        f4 += m33/tem

print(e1, e2, e3, e4)
print(f1, f2, f3, f4)
rmse = [(e1/r)**0.5, (e2/r)**0.5, (e3/r)**0.5, (e4/r)**0.5]
print(rmse)
mape = [e1/r, e2/r, e3/r, e4/r]
print(mape)
