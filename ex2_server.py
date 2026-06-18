import socket
import sys

def main():
    HOST = "127.0.0.1"
    PORT = 9999
    
    # Criação do socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        sock.bind((HOST, PORT))
        print(f"Servidor UDP escutando em {HOST}:{PORT}")
        sock.settimeout(30.0)  # Timeout de 30s para evitar travamento indefinido
        
        while True:
            try:
                data, addr = sock.recvfrom(65535)
                payload_size = len(data)
                print(f"[RECEBIDO] Origem: {addr[0]}:{addr[1]} | Tamanho: {payload_size} bytes")
                
                # Echo de volta
                sock.sendto(data, addr)
                
                # Permite desligamento gracioso via comando especial do cliente
                if b"SHUTDOWN" in data:
                    print("Comando SHUTDOWN recebido. Desligando servidor...")
                    break
                    
            except socket.timeout:
                print("Inatividade detectada (timeout de 10s). Encerrando servidor.")
                break
    finally:
        sock.close()
        print("Servidor UDP finalizado.")

if __name__ == "__main__":
    main()
