# Importamos las librerias necesarias
import requests
import threading
import time
import webbrowser
from win10toast_click import ToastNotifier

# Definimos la URL donde nos redirijirá la notificación
urlWeb = 'https://tauros.io/'

# Definimos la función que nos permite abrir la URL de la web del cliente
def openUrl():
    try:
        webbrowser.open_new(urlWeb)
        print('Redirigiendo...')
    except:
        print('Fallo al intentar abrir la URL')

# instanciamos un objeto de tipo ToastNotifier llamado toaster para mostrar las notificaciones
toaster = ToastNotifier()


# URL de la API Yahoo
url = "https://yfapi.net/v6/finance/quote/marketSummary"

querystring = {"symbols": "AAPL,BTC-USD,EURUSD=X"}

headers = {
    'x-api-key': "FnuYa0IExl9Q0nI3XFSC51WGf94dQzzG7PuM9KgN"
}

response = requests.request("GET", url, headers=headers, params=querystring)


# Función que verifica la API y se ejecuta cada determinado tiempo
def verificarApi():
    json = response.json() # Obtenemos los datos del endpoint en formato JSON
    results = json['marketSummaryResponse']['result'] # Almacenamos los resultados del archivo JSON en una variable
    
    #Buscamos el RegularMarketChangePercent de la bolsa Nikkem (elemento 15) y Nasdaq (elemento 13) y establecemos un valor inicial a comparar
    percentageInitNikkem = results[15]['regularMarketChangePercent']['fmt'] 
    percentageInitNikkem = percentageInitNikkem[0:-1] # Eliminamos el caracter % para su conversión de String a Float
    percentageInitNikkem = float(percentageInitNikkem) # Convertimos el porcentaje inicial en dato primitivo de tipo Float para operar sobre el 
    
    percentageInitNasdaq = results[13]['regularMarketChangePercent']['fmt']
    percentageInitNasdaq = percentageInitNasdaq[0:-1] # Eliminamos el caracter % para su conversión de String a Float
    percentageInitNasdaq = float(percentageInitNasdaq) # Convertimos el porcentaje inicial en dato primitivo de tipo Float para operar sobre el 
    
    # Iniciamos un bucle infinito que nos permitirá realizar la verificación de los datos del EndPoint consumido
    while True:
        # Almacenamos nuevamente los resultados del archivo JSON en una variable para comparar con los primeros datos recibidos
        response2 = requests.request("GET", url, headers=headers, params=querystring) 
        json = response2.json() # Creamos otro archivo JSON
        results = json['marketSummaryResponse']['result'] # Almacenamos los resultados del archivo JSON en una variable
        
        # Leemos los datos obtenidos de la bolsa Nikkem y procesamos para su manipulación
        percentageNikkem = results[15]['regularMarketChangePercent']['fmt'] 
        percentageNikkem = percentageNikkem[0:-1]
        percentageNikkem = float(percentageNikkem)
        
        # Leemos los datos obtenidos de la bolsa Nasdaq y procesamos para su manipulación
        percentageNasdaq = results[13]['regularMarketChangePercent']['fmt']
        percentageNasdaq = percentageNasdaq[0:-1]
        percentageNasdaq = float(percentageNasdaq)
        
        # Comparamos los valores iniciales con los actuales y los asignamos a una variable de tipo Bool
        nikkemChanged = True if percentageNikkem < percentageInitNikkem or percentageNikkem > percentageInitNikkem else False
        nasdaqChanged = True if percentageNasdaq < percentageInitNasdaq or percentageNasdaq > percentageInitNasdaq else False 
        
        # Mientras no cambia los valores, muestra un mensaje local que nos indica que esta revisando los datos
        print('Revisando...')
        print('Nasdaq %', percentageNasdaq, 'Nikkem', percentageNikkem) # Mostramoms los valores de las bolsas
        if nikkemChanged or nasdaqChanged: # Si existe un cambio, mandamos una notificación para indicar la compra
            # Mostramos la notificación de tipo Push
            toaster.show_toast(
                title='Nikkei 225, DAX Index y Nasdaq',
                msg='Acciones a precios historicos, compra ahora!>>',
                icon_path='Tauros.ico',
                duration=5,
                threaded=False,
                callback_on_click=openUrl
            )
            
        time.sleep(60)  # Tiempo establecido en segundos para su verificación del EndPoint


# Iniciamos la ejecución en segundo plano
t = threading.Thread(target=verificarApi)
t.start()
