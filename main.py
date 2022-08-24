"""####################################################################################
MEDUSA.....

Ampliacion de Neptuno Pico
Se usa una Pico W para darle conectividad a Neptuno y que pueda enviar alarmas PUSH al movil a traves
de pushsafer.
Con una sola Pico W se puede dotar de conectividad a unas 10 picos
Falta:
    - crear un servidor web que corra en otro core y que devuelva una pagina estatica con los estados
    - comunicacion uart entre picos para enviar datos y poder dar mas info en la pagina

#######################################################################################"""

import network
import time
from pushsafer import Client
import secrets
from machine import Pin

"""######### FIN IMPORTS ###########"""

"""######### BLOQUE FUNCIONES ##########"""
def conect():
    wlan = network.WLAN(network.STA_IF)
    print("levantando...")
    wlan.active(True)
    time.sleep(1)
    print("LEVANTADO")
    print("conectando...")
    wlan.connect(secrets.SSID,secrets.PASS)
    time.sleep(.5)
    while not wlan.isconnected() and wlan.status() >= 0:
        print("Esperando conexion....")
        time.sleep(1)
    
    stats = wlan.ifconfig()
    print("CONECTADO")
    print(f"IP: {stats[0]}\nNETMASK: {stats[1]}\nGATEWAY: {stats[2]}\nDNS: {stats[3]}")
    print("Connection Status:",wlan.status())
    print("Connected:",wlan.isconnected())

def envia_alarma(x):
    client = Client(secrets.KEY)
#1 = alarma agua; 2 = alarma suelo
    titulo="ALERTA NEPTUNO"
    if x == 1:
        mens = "Alerta de Deposito, no hay agua"
        client.send_message(mens, titulo, "56054", "33", "5", "3")
    elif x == 2:
        mens = "Alerta de sonda suelo, los valores son incorrectos. Revisar"
        client.send_message(mens, titulo, "56054", "33", "5", "3")
"""################# FIN BLOQUE FUNCIONES ################"""

sig_awa = Pin(0,Pin.IN)
sig_sonda = Pin(1,Pin.IN)
print("MEDUSA v0.1")
print("Cargando...................")
conect()


while True:
    if sig_sonda.value() == 1:
        print("Alarma de sonda")
        envia_alarma(2)
        time.sleep(2)
    elif sig_awa.value() == 1:
        print("Alarma de deposito")
        envia_alarma(1)
        time.sleep(2)
    elif sig_awa.value() == 0:
        continue
    elif sig_sonda.value() == 1:
        continue
