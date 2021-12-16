import cloudscraper # pip3 install cloudscraper
import json
from bs4 import BeautifulSoup # pip3 install BeautifulSoup4

def sacar_resultados():
    scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False}) # Pongo de navegador firefox en windows
    URL = scraper.get("https://footballdatabase.com/league-scores-tables/spain-primera-division-2021-2022").content
    soup = BeautifulSoup(URL, 'html.parser')
    table = soup.find('table', attrs={'class':'table table-hover table-condensed'}) # Clasificacion
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')

    data = []
    for row in rows: # Creo una lista con la cadena de la clasificacion
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])

    try: # Abro o creo el archivo clasificacion
        f = open("/bot/ProyectoDAM/datos/clasificacion.json","w+")
    except FileNotFoundError:
        print("Archivo no existe")
        exit()
    except PermissionError:
        print("No se tienen permisos para leer el archivo")
        exit()

    data = str(data).encode('utf-8')
    data = str(data).replace('b', '')
    data = str(data).replace('"', '')
    f.write(str(data))
    f.close()

    equipo1 = [] # Almaceno el primer equipo
    equipo2 = [] # Almaceno el segundo equipo
    resultados_partidos = [] # Almaceno el resultado
    resultados_partidos_final = [] # Sumo equipo1 + resultado + equipo2

    equipo1_texto = soup.find_all('a', attrs={'class':'sm_logo-name limittext'}) # Obtengo el primer equipo
    for texto in equipo1_texto:
        texto = quito_elementos_str(texto)
        equipo1.append(texto)

    equipo2_texto = soup.find_all('a', attrs={'class':'sm_logo-name sm_logo-name_away'}) # Obtengo el segundo equipo
    for texto in equipo2_texto:
        texto = quito_elementos_str(texto)
        equipo2.append(texto)
    
    resultados_partidos_texto = soup.find_all('div', attrs={'class':'club-gamelist-match-score text-center'}) # Obtengo el resultado
    for texto in resultados_partidos_texto:
        texto = quito_elementos_str(texto)
        resultados_partidos.append(texto)

    for i in range(len(resultados_partidos)): # Recorro el tamaño de la cadena y los sumo: equipo1 + resultado + equipo2
        suma_resultado = equipo1[i] + ' ' + resultados_partidos[i] + ' ' + equipo2[i]
        resultados_partidos_final.append(suma_resultado)

    try: # Abro o creo el archivo resultados
        f = open("/bot/ProyectoDAM/datos/resultados.json","w+")
    except FileNotFoundError:
        print("Archivo no existe")
        exit()
    except PermissionError:
        print("No se tienen permisos para leer el archivo")
        exit()

    f.write(str(resultados_partidos_final))
    f.close()

def quito_elementos_str(palabra): # Elimino 'b' y "'" de las cadenas obtenidas
    palabra = str(palabra.get_text().encode('utf-8'))
    palabra = palabra.replace('b', '')
    palabra = palabra.replace("'", '')

    return palabra

if __name__ == '__main__':
    sacar_resultados()