import re, datetime

sources = ['data_all_Lyon_Septembre_2017', 'data_all_Lyon_Octobre_2017', 'data_all_Lyon_Novembre_2017', 'data_all_Lyon_Decembre_2017', 'data_all_Lyon_Janvier_2018', 'data_all_Lyon_Fevrier_2018', 'data_all_Lyon_Mars_2018', 'data_all_Lyon_Avril_2018']


data_out = []
for src in sources:
    with open(src, 'r') as DB:
        DBread = DB.read()[:-3]
        # On a une chaine de caractères.
        data_in = DBread.split('}]\n[{')
        # On retire les données inutiles et on sépare.
        for line in data_in:
            n = len(line)
            line = line.split('}, {')
            # On retire les dernières données inutiles.
            for l in line:
                data_out.append(l)


n = len(data_out)
with open('Sorted_Data.csv', 'w') as cor:
    for k in range(n):
        raw = data_out[k]
        sep = ','
        
        stat = re.compile('"status": "(.*)", "contract_name": "Lyon", "download_date": (.*), "bike_stands": (.*), "number": (.*), "last_update": (.*), "available_bike_stands": (.*), "available_bikes": (.*)', re.I)
        # re.I permet d'ignorer la casse
        match = stat.search(raw)
        status = str(match.group(1))
        bike_stands = match.group(3)
        id_stand = match.group(4)

        date = match.group(5)
        date = str(datetime.datetime.fromtimestamp(int(date)/1000).strftime('%Y-%m-%d %H:%M:%S'))

        jour = date[:10]
        heure = date[11:]
        
        av_stands = match.group(6)
        av_bikes = match.group(7)
        raw = status + sep + bike_stands + sep + id_stand + sep + jour + sep + heure + sep + av_stands + sep + av_bikes
        cor.write(raw + '\n')
