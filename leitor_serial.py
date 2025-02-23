import serial
import json

# Substitua pelo nome correto da porta do seu Arduino
porta_serial = serial.Serial('/dev/tty.usbserial-110', 9600)

# Variáveis para armazenar o estado anterior
ultimo_nivel = None

while True:
    try:
        # Lê e formata os dados
        dados = porta_serial.readline().decode().strip()
        print(f"Recebido: {dados}")

        # Converte a string JSON em um dicionário Python
        dados_json = json.loads(dados)

        # Acessa os dados do sensor
        leitura = dados_json["leitura"]
        status = dados_json["status"]

        # Verifica se houve mudança no nível
        if leitura != ultimo_nivel:
            print(f"Novo status: {status}")
            ultimo_nivel = leitura

    except Exception as e:
        print(f"Erro: {e}")

