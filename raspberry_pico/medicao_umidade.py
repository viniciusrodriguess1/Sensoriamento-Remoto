import network
import socket
import time
import json
from machine import ADC, Pin

# ========= CONFIG Wi-Fi =========
ssid = "NOME_WIFI"     # coloque aqui o SSID exato
password = "SENHA_WIFI"        # coloque a senha correta

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

print("Conectando ao Wi-Fi...")

# Timeout de 15 segundos para não travar indefinidamente
timeout = 15
start = time.time()
while not wlan.isconnected():
    if time.time() - start > timeout:
        print("Falha ao conectar no Wi-Fi!")
        break
    time.sleep(1)

if wlan.isconnected():
    print("Conectado com sucesso!")
    print("Configuração de rede:", wlan.ifconfig())
else:
    # Se não conectar, não continua
    raise RuntimeError("Não foi possível conectar ao Wi-Fi")

# ========= SENSOR DE UMIDADE =========
sensor_umidade = ADC(Pin(26))  # GP26 (ADC0)

def ler_umidade():
    raw = sensor_umidade.read_u16()
    umidade = (65535 - raw) / 65535 * 100  # converte para %
    return raw, round(umidade, 2)

# ========= LOOP PRINCIPAL =========
while True:
    try:
        raw, umidade = ler_umidade()

        if raw > 50000:
            status = "SECO"
        elif raw > 24000:
            status = "UMIDO"
        else:
            status = "ENCHARCADO"

        dados = {
            "raw": raw,
            "umidade_percentual": umidade,
            "status": status,
            "dispositivo_id": 3
        }

        print("Enviando:", dados)

        # Envio via socket TCP
        addr = socket.getaddrinfo("10.179.117.232", 5001)[0][-1]  # IP do servidor
        s = socket.socket()
        s.connect(addr)
        s.send(json.dumps(dados).encode())
        s.close()

    except Exception as e:
        print("Erro ao enviar:", e)

    time.sleep(5)

