import serial
import pymysql
import json
import time

# Configuração da porta serial do Arduino
try:
    porta_serial = serial.Serial('COM6', 9600, timeout=2)
except serial.SerialException as e:
    print(f"Erro ao abrir porta serial: {e}")
    exit()

# Conexão com o banco de dados MySQL usando PyMySQL
try:
    db = pymysql.connect(
        host="localhost",
        user="root",
        database="banco_de_dados"
    )
    cursor = db.cursor()
    print("Conexão ao MySQL estabelecida com sucesso!")
except pymysql.MySQLError as e:
    print(f"Erro ao conectar ao MySQL: {e}")
    exit()

while True:
    try:
        # Lê a linha da serial
        dados = porta_serial.readline().decode().strip()

        # Verifica se a linha recebida é vazia ou não contém JSON
        if not dados or not dados.startswith("{"):
            print(f"Ignorando entrada inválida: {dados}")
            continue
        
        print(f"Recebido da serial: {dados}")

        # Converte para JSON
        try:
            dados_json = json.loads(dados)
        except json.JSONDecodeError:
            print("Erro ao converter JSON. Verifique os dados recebidos.")
            continue

        # Extraindo os dados corretamente
        ph = dados_json.get('ph')
        voltagem = dados_json.get('voltagem')
        boia = dados_json.get('boia')
        status = dados_json.get('status')

        # Verifica se os dados são válidos antes de inserir no banco
        if ph is None or voltagem is None or boia is None or status is None:
            print("Dados inválidos recebidos, ignorando...")
            continue

        # Insere no banco de dados
        query = "INSERT INTO niveis_agua (ph, voltagem, boia, status) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (ph, voltagem, boia, status))
        db.commit()
        
        print(f"Dados inseridos: pH = {ph}, Voltagem = {voltagem}, Boia = {boia}, Status = {status}")

    except Exception as e:
        print(f"Erro: {e}")
        time.sleep(1)  # Aguarda um tempo antes de tentar novamente
