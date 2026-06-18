import socket
import ssl
import sys

def main():
    HOST = "127.0.0.1"
    PORT = 8443
    
    # Cria o contexto SSL para o lado do Servidor
    # PROTOCOL_TLS_SERVER é o padrão moderno seguro que desabilita SSLv2, SSLv3, TLS 1.0, 1.1 por padrão.
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    
    try:
        # Carrega o certificado autoassinado e a respectiva chave privada
        context.load_cert_chain(certfile="server.crt", keyfile="server.key")
        print("Certificado TLS carregado com sucesso.")
    except Exception as e:
        print(f"Erro ao carregar certificado/chave: {e}")
        sys.exit(1)
        
    # Inicializa o socket TCP bruto
    bind_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bind_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        bind_sock.bind((HOST, PORT))
        bind_sock.listen(5)
        print(f"Servidor TLS escutando em segura https://{HOST}:{PORT}")
        
        while True:
            # Aceita a conexão TCP bruta
            client_sock, client_addr = bind_sock.accept()
            try:
                # Envelopa o socket TCP na camada SSL/TLS
                with context.wrap_socket(client_sock, server_side=True) as tls_sock:
                    print(f"\n[CONEXÃO TLS ESTABELECIDA] Origem: {client_addr[0]}:{client_addr[1]}")
                    
                    # Lê os dados criptografados recebidos (e os descriptografa na pilha SSL)
                    data = tls_sock.recv(1024)
                    if data:
                        message = data.decode('utf-8', errors='ignore')
                        print(f"  Mensagem descriptografada recebida: '{message}'")
                        
                        # Resposta segura
                        response = f"Confirmado TLS: Recebido '{message}'"
                        tls_sock.sendall(response.encode('utf-8'))
                        
                        if "SHUTDOWN" in message:
                            print("Comando SHUTDOWN recebido. Encerrando servidor TLS...")
                            break
            except Exception as e:
                print(f"Erro ao estabelecer sessão TLS com o cliente: {e}")
            finally:
                client_sock.close()
    finally:
        bind_sock.close()
        print("Servidor TLS finalizado.")

if __name__ == "__main__":
    main()
