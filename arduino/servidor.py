import socket
import mysql.connector
import json

# CONFIGURAÇÃO DO BANCO DE DADOS
db_config = {
    'user': 'root',
    'password': 'osOvMtonkwxcbEphriXeJGPKdOxSfAzl',
    'host': 'ballast.proxy.rlwy.net',
    'port': 56724,
    'database': 'railway'
}

HOST = '0.0.0.0'
PORT = 5001

# --- FUNÇÕES DE INSERÇÃO ---

def salvar_ph(valor_ph, dispositivo=None, dispositivo_id=None, usuario_id=None):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        campos = ["ph"]
        valores = [valor_ph]
        if dispositivo is not None:
            campos.append("dispositivo")
            valores.append(dispositivo)
        if dispositivo_id is not None:
            campos.append("dispositivo_id")
            valores.append(dispositivo_id)
        if usuario_id is not None:
            campos.append("usuario_id")
            valores.append(usuario_id)
        sql = f"INSERT INTO ph_niveis ({', '.join(campos)}) VALUES ({', '.join(['%s']*len(valores))})"
        cursor.execute(sql, valores)
        conn.commit()
        cursor.close()
        conn.close()
        print("Valor de pH salvo no banco.")
    except Exception as e:
        print("Erro ao salvar pH:", e)

def salvar_nivel_agua(boia=None, status=None, dispositivo=None, dispositivo_id=None, usuario_id=None):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        campos = []
        valores = []
        if boia is not None:
            campos.append("boia")
            valores.append(boia)
        if status is not None:
            campos.append("status")
            valores.append(status)
        if dispositivo is not None:
            campos.append("dispositivo")
            valores.append(dispositivo)
        if dispositivo_id is not None:
            campos.append("dispositivo_id")
            valores.append(dispositivo_id)
        if usuario_id is not None:
            campos.append("usuario_id")
            valores.append(usuario_id)
        if len(campos) == 0:
            print("Nenhum campo válido para salvar em niveis_agua.")
            cursor.close()
            conn.close()
            return
        sql = f"INSERT INTO niveis_agua ({', '.join(campos)}) VALUES ({', '.join(['%s']*len(valores))})"
        cursor.execute(sql, valores)
        conn.commit()
        cursor.close()
        conn.close()
        print("Nível de água salvo no banco.")
    except Exception as e:
        print("Erro ao salvar nível de água:", e)

# --- PROCESSAMENTO DA MENSAGEM RECEBIDA ---

def processar_mensagem(mensagem):
    mensagem = mensagem.strip()
    try:
        dados = json.loads(mensagem)
        # Busca o identificador de dispositivo (nome ou id, se vier)
        dispositivo = dados.get("dispositivo")
        dispositivo_id = dados.get("dispositivo_id")
        usuario_id = dados.get("usuario_id")
        # Salva pH, se presente
        if "ph" in dados:
            valor_ph = dados["ph"]
            salvar_ph(valor_ph, dispositivo, dispositivo_id, usuario_id)
        # Salva nível/boia, se presente
        if "boia" in dados or "status" in dados:
            boia = dados.get("boia")
            status = dados.get("status")
            salvar_nivel_agua(boia, status, dispositivo, dispositivo_id, usuario_id)
    except Exception as e:
        print("Mensagem recebida em formato desconhecido ou erro de JSON:", mensagem)
        print("Erro:", e)

# --- SERVIDOR TCP PRINCIPAL ---

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Servidor TCP escutando em {HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        with conn:
            print(f"Conexão de {addr}")
            data = conn.recv(1024)
            if data:
                mensagem = data.decode('utf-8')
                print(f"Mensagem recebida: {mensagem}")
                processar_mensagem(mensagem)