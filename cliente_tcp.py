import socket
import requests
import time

fastapi_url = "http://localhost:8000/arduino_data"

tcp_ip = "127.0.0.1" #IP do servidor TCP
tcp_port = 5001  # Porta do servidor TCP

while True:
    try:
        # 1. Requisição para o servidor FastAPI
        response = requests.get(fastapi_url)
        if response.status_code == 200:
            arduino_data = response.json().get("data")
            if arduino_data:
                print(f"Dados obtidos do FastAPI: {arduino_data}")

                # 2. Enviar para o servidor TCP
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((tcp_ip, tcp_port))
                    s.sendall(arduino_data.encode('utf-8'))
                    print("Dados enviados ao servidor TCP.")
            else:
                print("Nenhum dado recebido do Arduino ainda.")
        else:
            print(f"Erro ao obter dados do FastAPI: {response.status_code}")

        time.sleep(5)  

    except Exception as e:
        print(f"Erro: {e}")
        time.sleep(5)
