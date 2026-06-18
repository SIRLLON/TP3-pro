import socket
import sys
import time

def run_client(message):
    HOST_V6 = "::1"
    HOST_V4 = "127.0.0.1"
    PORT = 9996
    
    sock = None
    connected = False
    
    # Tentativa 1: IPv6
    print(f"\n[CLIENTE] Tentando conectar via IPv6 a [{HOST_V6}]:{PORT}...")
    try:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        sock.settimeout(2.0)
        sock.connect((HOST_V6, PORT))
        connected = True
        print("  [SUCESSO] Conectado via IPv6!")
    except Exception as e:
        print(f"  [FALHA] Erro de conexão IPv6: {e}")
        sock = None
        
    # Tentativa 2 (Fallback): IPv4
    if not connected:
        print(f"  [FALLBACK] Iniciando fallback automatizado para IPv4 em {HOST_V4}:{PORT}...")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2.0)
            sock.connect((HOST_V4, PORT))
            connected = True
            print("  [SUCESSO] Conectado via IPv4 (Fallback)!")
        except Exception as e:
            print(f"  [FALHA TOTAL] Erro ao conectar via IPv4: {e}")
            sock = None
            
    if sock and connected:
        try:
            # Envia a mensagem
            sock.sendall(message.encode('utf-8'))
            # Recebe resposta
            data = sock.recv(1024)
            print(f"  [RESPOSTA RECEBIDA] '{data.decode('utf-8')}'")
        except Exception as e:
            print(f"  Erro durante a transmissão: {e}")
        finally:
            sock.close()
            print("  Conexão fechada.")
    else:
        print("  Não foi possível estabelecer a comunicação.")

def main():
    print("=== CLIENTE TCP COM FALLBACK DE PILHA (IPv6 -> IPv4) ===")
    
    # Envia mensagem padrão
    run_client("Ola, testando conexao dual-stack!")
    
    time.sleep(0.5)
    
    # Envia sinal de desligamento
    print("\n--- Enviando sinal de finalização para o servidor ---")
    run_client("SHUTDOWN")

if __name__ == "__main__":
    main()
