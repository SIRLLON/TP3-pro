import socket
import threading
import sys
import time

# Evento global para sinalizar desligamento
shutdown_event = threading.Event()
server_socket = None

def handle_client(client_sock, client_addr):
    print(f"[CONEXÃO ACEITA] Cliente: {client_addr[0]}:{client_addr[1]}")
    try:
        client_sock.settimeout(5.0)
        data = client_sock.recv(1024)
        if data:
            message = data.decode('utf-8', errors='ignore')
            print(f"[REQUISIÇÃO] De {client_addr[0]}:{client_addr[1]}: '{message}'")
            
            # Resposta de confirmação
            response = f"Echo Servidor TCP Concorrente: Recebido '{message}'"
            client_sock.sendall(response.encode('utf-8'))
            
            if "SHUTDOWN" in message:
                print("Comando de SHUTDOWN recebido de um cliente. Iniciando desligamento...")
                shutdown_event.set()
    except Exception as e:
        print(f"[ERRO NO CLIENTE] {client_addr[0]}:{client_addr[1]} - {e}")
    finally:
        client_sock.close()
        print(f"[CONEXÃO FECHADA] Cliente: {client_addr[0]}:{client_addr[1]}")

def listen_loop():
    global server_socket
    HOST = "127.0.0.1"
    PORT = 9998
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(10)
        print(f"Servidor TCP concorrente escutando em {HOST}:{PORT}")
        server_socket.settimeout(1.0) # Permite checar o shutdown_event regularmente
        
        while not shutdown_event.is_set():
            try:
                client_sock, client_addr = server_socket.accept()
                # Cria uma thread para tratar o cliente concorrentemente
                t = threading.Thread(target=handle_client, args=(client_sock, client_addr), daemon=True)
                t.start()
            except socket.timeout:
                continue
            except Exception as e:
                if not shutdown_event.is_set():
                    print(f"Erro no accept: {e}")
                break
    finally:
        server_socket.close()
        print("Servidor TCP finalizado.")

def main():
    t_server = threading.Thread(target=listen_loop, daemon=False)
    t_server.start()
    
    # Aguarda o sinal de desligamento
    while t_server.is_alive():
        try:
            t_server.join(0.5)
        except KeyboardInterrupt:
            print("KeyboardInterrupt recebido no servidor.")
            shutdown_event.set()
            break

if __name__ == "__main__":
    main()
