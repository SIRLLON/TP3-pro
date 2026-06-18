import socket
import sys

def main():
    HOST_V6 = "::1"
    HOST_V4 = "127.0.0.1"
    PORT = 9996
    
    # Verifica se o teste quer forçar apenas IPv4 para testar o fallback do cliente
    force_ipv4 = len(sys.argv) > 1 and sys.argv[1] == "ipv4_only"
    
    server_sock = None
    used_ipv6 = False
    
    if not force_ipv4:
        try:
            # Tenta criar e bindar em IPv6
            server_sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_sock.bind((HOST_V6, PORT))
            used_ipv6 = True
            print(f"Servidor TCP iniciado com sucesso em IPv6: [{HOST_V6}]:{PORT}")
        except Exception as e:
            print(f"Não foi possível iniciar em IPv6 ({e}). Iniciando fallback para IPv4...")
            server_sock = None
            
    if server_sock is None:
        # Fallback para IPv4
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((HOST_V4, PORT))
        used_ipv6 = False
        print(f"Servidor TCP iniciado (modo Fallback IPv4): {HOST_V4}:{PORT}")
        
    try:
        server_sock.listen(5)
        while True:
            client_sock, client_addr = server_sock.accept()
            try:
                family = "IPv6" if used_ipv6 else "IPv4"
                print(f"\n[CONEXÃO RECEBIDA ({family})] Origem: {client_addr}")
                
                data = client_sock.recv(1024)
                if data:
                    message = data.decode('utf-8')
                    print(f"  Mensagem: '{message}'")
                    
                    response = f"Confirmado {family}: Recebido '{message}'"
                    client_sock.sendall(response.encode('utf-8'))
                    
                    if "SHUTDOWN" in message:
                        print("Comando SHUTDOWN recebido. Desligando servidor...")
                        break
            except Exception as e:
                print(f"Erro ao tratar cliente: {e}")
            finally:
                client_sock.close()
    finally:
        server_sock.close()
        print("Servidor finalizado.")

if __name__ == "__main__":
    main()
