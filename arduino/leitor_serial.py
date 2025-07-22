import serial
import socket
import time

# CONFIGURE AQUI os parâmetros:
SERIAL_PORT = 'COM7'          # Ex: 'COM3' no Windows, '/dev/ttyACM0' no Linux
BAUD_RATE = 9600            # Mesmo baudrate do Arduino

TCP_HOST = "172.26.8.127"        # IP do servidor TCP (ajuste, se for remoto pela rede)
TCP_PORT = 5001                             # Porta do servidor TCP

def envia_para_servidor(mensagem):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((TCP_HOST, TCP_PORT))
            s.sendall(mensagem.encode('utf-8'))
    except Exception as e:
        print(f"Falha ao enviar para o servidor: {e}")

def main():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Lendo {SERIAL_PORT} a {BAUD_RATE} baud e enviando para {TCP_HOST}:{TCP_PORT}")
        while True:
            if ser.in_waiting > 0:
                linha = ser.readline().decode("utf-8", errors="ignore").strip()
                if linha != "":
                    print(f"Lido da serial: {linha}")
                    envia_para_servidor(linha)
            time.sleep(0.05)
    except serial.SerialException as e:
        print(f"Erro na porta serial: {e}")
    except KeyboardInterrupt:
        print("Encerrando leitura serial.")
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        try:
            ser.close()
        except:
            pass

if __name__ == "__main__":
    main()