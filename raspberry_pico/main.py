import network
import time

ssid = "DIGITAL-GABRIEL" #alterar nome da rede
password = "07102017" # || senha

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

print("Conectando ao Wi-Fi...")

max_wait = 10
while max_wait > 0:
    if wlan.isconnected():
        break
    print("Aguardando conexão...")
    time.sleep(1)
    max_wait -= 1

if wlan.isconnected():
    print("Conectado com sucesso!")
    print("IP:", wlan.ifconfig()[0])
else:
    print("Falha ao conectar.")

