import socket
import threading
import time

def run_single_client(client_id):
    HOST = "127.0.0.1"
    PORT = 9998
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        
        # Envia mensagem identificada
        msg = f"Requisicao do Cliente #{client_id}"
        print(f"[CLIENTE #{client_id}] Enviando: '{msg}'")
        sock.sendall(msg.encode('utf-8'))
        
        # Recebe resposta
        data = sock.recv(1024)
        response = data.decode('utf-8')
        print(f"[CLIENTE #{client_id}] Resposta recebida: '{response}'")
        
        sock.close()
    except Exception as e:
        print(f"[CLIENTE #{client_id}] Erro: {e}")

def main():
    threads = []
    print("=== CLIENTE TCP CONCORRENTE INICIANDO ===")
    
    # Lançando 5 conexões de clientes em threads paralelas
    for i in range(1, 6):
        t = threading.Thread(target=run_single_client, args=(i,))
        threads.append(t)
        t.start()
        time.sleep(0.05) # Pequeno delay para ordenar visualmente a inicialização
        
    # Aguarda todas as threads terminarem
    for t in threads:
        t.join()
        
    print("\n--- Conexões dos 5 clientes finalizadas. Enviando sinal de SHUTDOWN para o servidor. ---")
    
    # Conexão final para desligar o servidor
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("127.0.0.1", 9998))
        sock.sendall(b"SHUTDOWN")
        sock.close()
    except Exception as e:
        print(f"Erro ao enviar SHUTDOWN: {e}")

if __name__ == "__main__":
    main()
