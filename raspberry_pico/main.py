import network
import socket
import time
import random

# configuração da rede
ssid = "CAFOFOEMNARNIA-2.4G"
password = "narniahouse"

server_ip = "192.168.0.100"
server_port = 5001

# conexão wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

print("Conectando ao Wi-Fi...")
while not wlan.isconnected():
    time.sleep(1)
print("Conectado!")
print("IP local:", wlan.ifconfig()[0])

while True:
    try:
        print("🔌 Tentando conectar ao servidor...")
        addr = socket.getaddrinfo(server_ip, server_port)[0][-1]
        s = socket.socket()
        s.connect(addr)

        numero = random.randint(1000, 9000)
        msg = f"Mensagem da Pico W: {numero}\n"
        s.send(msg.encode('utf-8'))
        print("Mensagem enviada:", msg.strip())
        s.close() 
    except Exception as e:
        print("Erro ao conectar/enviar:", e)

    time.sleep(5)
