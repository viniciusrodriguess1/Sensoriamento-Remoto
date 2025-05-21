import socket
import mysql.connector

HOST = '127.0.0.1'  # IP para escutar
PORT = 5001    # Porta para escutar

def get_db_connection():
    return mysql.connector.connect(
        user='root',
        password='',
        host='localhost',
        database='banco_de_dados'
    )

def inserir_no_banco(id_valor, ph_valor, data_valor, usuario_id_valor):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO ph_niveis (id, ph, data, usuario_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (id_valor, ph_valor, data_valor, usuario_id_valor))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Dados inseridos: {id_valor}, {ph_valor}, {data_valor}, {usuario_id_valor}")
        return "Inserção OK"
    except Exception as e:
        print("Erro ao inserir no banco:", e)
        return "Erro na inserção"

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
            valores = texto.split(',')

            if len(valores) == 4:
                id_valor = valores[0]
                ph_valor = valores[1]
                data_valor = valores[2]
                usuario_id_valor = valores[3]

                resposta = inserir_no_banco(id_valor, ph_valor, data_valor, usuario_id_valor)
            else:
                resposta = "Formato inválido. Use: id,ph,data,usuario_id"

            conn.sendall(resposta.encode('utf-8'))
