import socket

HOST = '0.0.0.0'  # Escuta em todas as interfaces de rede
PORT = 5001       # Porta para escutar

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
                print(f"Mensagem recebida: {data.decode('utf-8')}")