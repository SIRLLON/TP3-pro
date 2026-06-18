import socket
import ssl
import sys
import time

def run_client(message):
    HOST = "localhost"
    PORT = 8443
    
    # Cria o contexto de cliente TLS
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    
    # Para validar um certificado autoassinado de forma correta, dizemos ao cliente
    # para confiar explicitamente no arquivo do certificado 'server.crt'
    try:
        context.load_verify_locations("server.crt")
    except Exception as e:
        print(f"Erro ao carregar trust store: {e}")
        sys.exit(1)
        
    try:
        raw_sock = socket.create_connection((HOST, PORT), timeout=5.0)
        with context.wrap_socket(raw_sock, server_hostname=HOST) as tls_sock:
            # Informações do handshake
            print(f"\n[CLIENTE] Conectado via {tls_sock.version()} usando {tls_sock.cipher()[0]}")
            
            # Envio seguro
            print(f"[CLIENTE] Enviando: '{message}'")
            tls_sock.sendall(message.encode('utf-8'))
            
            # Leitura segura
            data = tls_sock.recv(1024)
            response = data.decode('utf-8')
            print(f"[CLIENTE] Recebido do Servidor: '{response}'")
            
    except Exception as e:
        print(f"[CLIENTE] Erro na comunicação segura: {e}")

def main():
    print("=== CLIENTE TLS SEGURO INICIANDO ===")
    
    # Envio de mensagem padrão
    run_client("Conexao segura via socket TLS puro!")
    
    time.sleep(0.5)
    
    # Envio do sinal de desligamento
    print("\n--- Enviando comando de finalização para o servidor ---")
    run_client("SHUTDOWN")

if __name__ == "__main__":
    main()
