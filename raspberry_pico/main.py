import network
import socket
import time
import json
import random
from machine import ADC, Pin

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

# sensores
ph_sensor = ADC(26)  # GP26 (ADC0)
boia_pin = Pin(15, Pin.IN)

def ler_sensores():
    # Leitura do sensor de pH
    raw_ph = ph_sensor.read_u16()
    volt_ph = (raw_ph / 65535) * 3.3
    ph_valor = round((volt_ph - 0.5) * 3.5, 2)
    
    # Leitura do sensor de boia
    boia = boia_pin.value()
    status = "Alto" if boia == 1 else "Baixo"

    return {
        "ph": ph_valor,
        "boia": boia,
        "status": status
    }


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
