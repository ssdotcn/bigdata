from bs4 import BeautifulSoup as bs
import pandas as pd
import operator as op
import requests as rq


# LINKS DE PAGINAS USADAS
urlA = 'https://www.cyberpuerta.mx/index.php?cl=details&anid=583f47990391e6914205331e0a2c3024&utm_source=Kingston&utm_medium=referral&utm_campaign=KingstonMemoryFinder'
urlB = 'https://articulo.mercadolibre.com.mx/MLM-1494073387-unidad-ssd-kingston-kc3000-512g-nvme-40-7000mbs-y-3900mbs-_JM'
urlC = 'https://www.xtremetecpc.com/public/producto/m-2-2280-ssd-512gb-kingston-kc3000-nvme-pcie-4-0-skc3000s-512g'

# OBTENIENDO DATOS
rqA = rq.get(urlA)
rqB = rq.get(urlB)
rqC = rq.get(urlC)

# GUARDANDO ESTADO DE CADA PAGINA
sttsA = rqA.status_code
sttsB = rqB.status_code
sttsC = rqC.status_code

# CREANDO DICCIONARIO CON NOMBRE DE PAGINAS DONDE SE GUARDARAN LOS PRECIOS
precios = {'CYBER PUERTA': None, 'MERCADO LIBRE': None, 'XTREMETECPC': None}

# VALIDANDO ESTADO DE PAGINAS
if sttsA == 200 & sttsB == 200 & sttsC == 200:

    # EXTRAYENDO DATOS DE PAGINAS
    soupA = bs(rqA.text,'lxml')
    soupB = bs(rqB.text,'lxml')
    soupC = bs(rqC.text,'lxml')

    # FILTRANDO DATOS
    valA = soupA.find('span', class_='priceText')
    valB = soupB.find('meta', itemprop='price')
    valC = soupC.find('price', class_='total_price')

    # GUARDANDO VALOR DE PRECIOS DE CADA PAGINA
    precios[list(precios.keys())[0]] = float(valA.text.split('$')[1])
    precios[list(precios.keys())[1]] = float(valB.get('content'))
    precios[list(precios.keys())[2]] = float(valC.text.strip().split('$')[1])

else:

    # ESTADOS DE ERROR (SI HUBIESE ERROR CON ALGUNA PAGINA)
    print ('STATUS: {}'.format(sttsA))
    print ('STATUS: {}'.format(sttsB))
    print ('STATUS: {}'.format(sttsC))

# ORDENANDO PRECIOS SEGUN DE MENOR A MAYOR
precios = dict(sorted(precios.items(), key=op.itemgetter(1)))

# PASANDO EL DOCCIONARIO A UN DATAFRAME PARA PODER EXPORTARLO
dfP = pd.DataFrame([precios])

# AÑADIENDO NOMBRE DEL ARTICULO AL INDEX DEL DATAFRAME PARA PODER IDENTIFICARLO MEJOR
dfP = dfP.set_index(pd.Index(['SSD Kingston KC3000 NVMe, 512GB, PCI Express 4.0, M.2']))

# IMPRIMIENDO DATAFRAME CON LOS DATOS
print('\nPAGINAS CON PRECIOS')
print(dfP)

# IMPRIMIENDO DATAFRAME MOSTRANDO SOLO LA PAGINA CON EL PRECIO MENOR
print('\nPAGINA CON EL MENOR PRECIO')
print(dfP.iloc[:, [0]])

# EXPORTANDO DATAFRAME EN UN ARCHIVO CSV
# GENERANDO REPORTE
urlCSV = 'data/ReportePrecios.csv'
dfP.to_csv(urlCSV,index='columns')
