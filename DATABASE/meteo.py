# meteo.py : Produit un fichier Meteo.csv contenant les relevés météo nécessaires


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
    for raw in text:
        raw = raw[0].split(";")

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
            f.write(date1[0:4]+'-'+date1[4:6]+'-'+date1[6:8] + ',' + date2[0:2]+':'+date2[2:4]+':00' + ',' + ff + ',' + t + ',' + u + ',' + rr1 + ',' + rr3 + ',' + rr6 + ',' + rr12 + ',' + rr24 + '\n')
