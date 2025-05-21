import socket

HOST = '127.0.0.1'  # IP do servidor
PORT = 5001    # Porta do servidor

# Dados que você quer enviar (exemplo)
id_valor = 123
ph_valor = 7.2
data_valor = "2025-05-20 14:30:00"
usuario_id_valor = 42

mensagem = f"{id_valor},{ph_valor},{data_valor},{usuario_id_valor}"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(mensagem.encode('utf-8'))

    resposta = s.recv(1024)
    print('Resposta do servidor:', resposta.decode('utf-8'))
