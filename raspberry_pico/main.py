import network
import socket
import time
import json
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

# Sensores
ph_sensor = ADC(26)      # GP26 (ADC0)
boia_pin = Pin(15, Pin.IN)

# Variáveis de controle
ultimo_estado_boia = -1
ph_fora_faixa = False

# Função de leitura e cálculo do pH
def ler_ph():
    raw = ph_sensor.read_u16()
    voltage = (raw / 65535) * 3.3
    ph = 7 + ((2.5 - voltage) / 0.18)  # mesmo cálculo da ESP32
    return round(ph, 2), round(voltage, 3)

# Loop principal
while True:
    try:
        # Leitura dos sensores
        ph, voltage = ler_ph()
        boia = boia_pin.value()
        status_boia = "ALTO" if boia == 1 else "BAIXO"

        # Alerta de pH
        if (ph > 9 or ph < 3) and not ph_fora_faixa:
            print("ALERTA: pH fora da faixa segura!")
            print("Valor do pH:", ph)
            ph_fora_faixa = True
        elif (3 <= ph <= 9) and ph_fora_faixa:
            print("O pH voltou à faixa segura.")
            print("Valor do pH:", ph)
            ph_fora_faixa = False

        # Envio apenas se o estado da boia mudou
        if boia != ultimo_estado_boia:
            dados = {
                "ph": ph,
                "voltagem": voltage,
                "boia": boia,
                "status": status_boia,
                "dispositivo_id": 3
            }
            print("Enviando:", dados)

            # Envio via socket TCP
            addr = socket.getaddrinfo("10.123.115.196", 8081)[0][-1]
            s = socket.socket()
            s.connect(addr)
            s.send(json.dumps(dados).encode())
            s.close()

            ultimo_estado_boia = boia

    except Exception as e:
        print("Erro ao enviar:", e)

    time.sleep(2)

