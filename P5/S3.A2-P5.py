from bs4 import BeautifulSoup as bs
import pandas as pd
import requests as rq
import json as js

def getDataAtWorks(linkW):

    rqW = rq.get(linkW)

    sttsW = rqW.status_code

    if sttsW == 200:
        soupW = bs(rqW.text,'lxml')

        datosW = soupW.find('dl', class_ = 'deflist o-blocks__block')

        title = datosW.find('dd', itemprop = 'name').text

        detListCuadros[list(detListCuadros.keys())[0]].append(title.split('\n')[1])

        place = datosW.find('dd', itemprop = 'locationCreated').text

        detListCuadros[list(detListCuadros.keys())[1]].append(place.split('\n')[1])

        date = datosW.find('dd', itemprop = 'dateCreated').find('a').text.strip()

        detListCuadros[list(detListCuadros.keys())[2]].append(date)

        dimen = datosW.find('dd', itemprop = 'size').text

        detListCuadros[list(detListCuadros.keys())[3]].append(dimen.split('\n')[1])


        detListCuadros[list(detListCuadros.keys())[4]].append(linkW)
        
    else:
        print ('STATUS: {}'.format(sttsW))


url = 'https://www.artic.edu/collection?artist_ids=Jos%C3%A9%20Clemente%20Orozco'

rqP = rq.get(url)

stts = rqP.status_code

autor = {'PINTOR': None}
listCuadros = {'NOMBRE': [], 'LINK': []}
detListCuadros = {'NOMBRE': [], 'LUGAR': [], 'AÑO': [], 'TAMAÑO': [], 'LINK': []}

if stts == 200:

    soup = bs(rqP.text,'lxml')

    pinturas = soup.find('ul', id = 'artworksList')

    cuadros = pinturas.find_all('li')

    nomArtista = pinturas.find('span', class_ = 'subtitle f-tertiary').text

    autor[list(autor.keys())[0]] = nomArtista

    for aValue in cuadros[:3]:

        data = aValue.find_all('a')

        for dValue in data:

            link = dValue.get('href')
            listCuadros[list(listCuadros.keys())[1]].append(link)

            nomrbe = dValue.find_all('strong')

            for nom in nomrbe:
                listCuadros[list(listCuadros.keys())[0]].append(nom.text.split(',')[0])
            
            getDataAtWorks(link)

else:
    print ('STATUS: {}'.format(stts))


dfL = pd.read_json(js.dumps(listCuadros))
dfDL = pd.read_json(js.dumps(detListCuadros))

dfP = pd.DataFrame([autor])
dfC = pd.DataFrame(dfL)
dfDC = pd.DataFrame(dfDL)

pinturas = pd.concat([dfP, dfC])
print(pinturas)

detPint = pd.concat([dfP, dfDC])
print(pinturas)

urlCSV = 'data/ReportePinturas.csv'
pinturas.to_csv(urlCSV, index=False, encoding='latin-1')

urlCSVD = 'data/ReporteDetallePinturas.csv'
detPint.to_csv(urlCSVD, index=False, encoding='latin-1')