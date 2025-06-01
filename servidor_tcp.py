import socket
import mysql.connector
import json
from datetime import datetime

HOST = '127.0.0.1'  # IP para escutar
PORT = 5001    # Porta para escutar

def get_db_connection():
    return mysql.connector.connect(
        user='root',
        password='',
        host='localhost',
        database='banco_de_dados'
    )

def inserir_ph_no_banco(ph_valor, data_valor, usuario_id_valor):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO ph_niveis (ph, data, usuario_id) VALUES (%s, %s, %s)"
        cursor.execute(sql, (ph_valor, data_valor, usuario_id_valor))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Dados de pH inseridos: {ph_valor}, {data_valor}, {usuario_id_valor}")
        return "Inserção OK para pH"
    except Exception as e:
        print("Erro ao inserir dados de pH:", e)
        return "Erro na inserção de pH"

def inserir_agua_no_banco(boia_valor, status_valor, data_valor, usuario_id_valor):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO niveis_agua (boia, status, data, usuario_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (boia_valor, status_valor, data_valor, usuario_id_valor))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Dados de nível de água inseridos: {boia_valor}, {status_valor}, {data_valor}, {usuario_id_valor}")
        return "Inserção OK para Nível de Água"
    except Exception as e:
        print("Erro ao inserir dados de Nível de Água:", e)
        return "Erro na inserção de Nível de Água"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Servidor TCP ouvindo em {HOST}:{PORT} ...")

    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Conectado por {addr}")
            data = conn.recv(1024)
            if not data:
                continue
            
            texto = data.decode('utf-8').strip()

            try:
                dados = json.loads(texto)
                # Definindo data atual como timestamp
                data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                usuario_id_valor = 1  # Pode ser ajustado conforme necessidade

                # Inserir dados de pH
                if 'ph' in dados:
                    ph_valor = float(dados['ph'])
                    inserir_ph_no_banco(ph_valor, data_atual, usuario_id_valor)

                # Inserir dados de Nível de Água
                if 'boia' in dados and 'status' in dados:
                    boia_valor = int(dados['boia'])
                    status_valor = dados['status']
                    inserir_agua_no_banco(boia_valor, status_valor, data_atual, usuario_id_valor)

                resposta = "Inserção OK para ambos"
            except Exception as e:
                print("Erro ao processar dados JSON:", e)
                resposta = f"Erro ao processar dados JSON: {e}"

            conn.sendall(resposta.encode('utf-8'))
