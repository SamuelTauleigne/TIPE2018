#station = 07481

sources = ['synop.201709.csv','synop.201710.csv', 'synop.201711.csv', 'synop.201712.csv', 'synop.201801.csv', 'synop.201802.csv', 'synop.201803.csv', 'synop.201804.csv']

text = []
for s in sources:
    with open(s) as f:
        f = f.readlines()
        i = 0
        for x in f:
            if i == 0:
                i = 1
            else:
                text.append(x.split('\t'))


with open('Meteo.csv', 'w') as f:
    for raw in text: # text[1:] ???
        raw = raw[0].split(";")
    
        #num_sta, date, pmer, tend, cod_tend, dd, ff, t, td, u, uv, ww, w1, w2, n, nbas, hbas, cl, cm, ch, pres, niv_bar, geop, tend24, tn12, tn24, tx12, tx24, tminsol, sw, tw, raf10, rafper, per, etat_sol, ht_neige, ssfrai, perssfrai, rr1, rr3, rr6, rr12, rr24, phenspe1, phenspe2, phenspe3, phenspe4, nnuage1, ctype1, hnuage1, nnuage2, ctype2, hnuage2, nnuage3, ctype3, hnuage3, nnuage4, ctype4, hnuage4 = raw.split(";")

        '''
        if int(num_sta) == 7481:
        print(date[:8] + ' ' + date[8:] + ' ' + pmer + ' ' + tend + ' ' + cod_tend + ' ' + dd + ' ' + ff + ' ' + t + ' ' + td + ' ' + u + ' ' + uv + ' ' + ww + ' ' + w1 + ' ' + w2 + ' ' + n + ' ' + nbas + ' ' + hbas + ' ' + cl + ' ' + cm + ' ' + ch + ' ' + pres + ' ' + niv_bar + ' ' + geop + ' ' + tend24 + ' ' + tn12 + ' ' + tn24 + ' ' + tx12 + ' ' + tx24 + ' ' + tminsol + ' ' + sw + ' ' + tw + ' ' + raf10 + ' ' + rafper + ' ' + per + ' ' + etat_sol + ' ' + ht_neige + ' ' + ssfrai + ' ' + perssfrai + ' ' + rr1 + ' ' + rr3 + ' ' + rr6 + ' ' + rr12 + ' ' + rr24 + ' ' + phenspe1 + ' ' + phenspe2 + ' ' + phenspe3 + ' ' + phenspe4 + ' ' + nnuage1 + ' ' + ctype1 + ' ' + hnuage1 + ' ' + nnuage2 + ' ' + ctype2 + ' ' + hnuage2 + ' ' + nnuage3 + ' ' + ctype3 + ' ' + hnuage3 + ' ' + nnuage4 + ' ' + ctype4 + ' ' + hnuage4)
        s += 1
    
        if int(num_sta) == 7481:
        print(date[:8] + ' ' + date[8:] + ' ' + rr1 + ' ' + rr3 + ' ' + rr6 + ' ' + rr12 + ' ' + rr24)
        s += 1
        '''

        num_sta = raw[0]
        date1 = raw[1][:8]
        date2 = raw[1][8:]
        ff = raw[6]
        t = raw[7]
        u = raw[9]
        rr1 = raw[38]
        rr3 = raw[39]
        rr6 = raw[40]
        rr12 = raw[41]
        rr24 = raw[42]
        if int(num_sta) == 7481:
            #print(date1 + ' ' + date2 + ' ' + ff + ' ' + t + ' ' + u + ' ' + rr1 + ' ' + rr3 + ' ' + rr6 + ' ' + rr12 + ' ' + rr24)
            f.write(date1[0:4]+'-'+date1[4:6]+'-'+date1[6:8] + ',' + date2[0:2]+':'+date2[2:4]+':00' + ',' + ff + ',' + t + ',' + u + ',' + rr1 + ',' + rr3 + ',' + rr6 + ',' + rr12 + ',' + rr24 + '\n')
