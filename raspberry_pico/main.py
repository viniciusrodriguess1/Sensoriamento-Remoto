import network
import socket
import time
import json
import random

# Wi-Fi
ssid = "wifi"
password = "senha"
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
print("Conectando ao Wi-Fi...")
while not wlan.isconnected():
    time.sleep(1)
print("Conectado:", wlan.ifconfig()[0])

# Simulação de sensores
def ler_sensores():
    ph = round(random.uniform(6.5, 8.0), 2)
    boia = random.randint(0, 1)
    status = "Alto" if boia else "Baixo"
    return {"ph": ph, "boia": boia, "status": status}

# Loop principal
while True:
    try:
        #Enviar apenas o pH
        ph = round(random.uniform(6.5, 8.0), 2)
        dados_ph = {"ph": ph}
        print("Enviando pH:", dados_ph)
        addr = socket.getaddrinfo("192.168.1.13", 5001)[0][-1]
        s = socket.socket()
        s.connect(addr)
        s.send(json.dumps(dados_ph).encode())
        s.close()
        print("pH enviado")

        #Enviar apenas boia e status
        boia = random.randint(0, 1)
        status = "Alto" if boia else "Baixo"
        dados_boia = {"boia": boia, "status": status}
        print("Enviando boia:", dados_boia)
        addr = socket.getaddrinfo("192.168.1.13", 5001)[0][-1]
        s = socket.socket()
        s.connect(addr)
        s.send(json.dumps(dados_boia).encode())
        s.close()
        print("Nível da boia enviado")

    except Exception as e:
        print("Erro ao enviar:", e)

    time.sleep(5)
