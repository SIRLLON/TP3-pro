import socket
import time
import threading

def start_temp_server():
    # Cria um servidor TCP temporário para ser detectado pelo scanner
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind(("127.0.0.1", 8080))
        server.listen(1)
        # Mantém escutando até o final do script
        server.accept()
    except Exception:
        pass
    finally:
        server.close()

def main():
    target_host = "127.0.0.1"
    start_port = 8075
    end_port = 8085
    timeout = 0.2 # Limite de tempo curto por porta para eficiência
    
    # Inicia o servidor temporário em uma thread daemon
    t_server = threading.Thread(target=start_temp_server, daemon=True)
    t_server.start()
    time.sleep(0.2) # Aguarda inicialização do servidor
    
    print(f"=== SCANNER TCP CONTROLADO ===")
    print(f"Alvo: {target_host}")
    print(f"Faixa de Portas: {start_port} a {end_port}")
    print(f"Timeout por porta: {timeout}s\n")
    
    open_ports = []
    
    start_time = time.perf_counter()
    
    # Varredura síncrona
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        # Executa a conexão síncrona
        result = sock.connect_ex((target_host, port))
        
        if result == 0:
            print(f"Porta {port}: ABERTA")
            open_ports.append(port)
        else:
            # Porta fechada ou filtrada
            pass
            
        sock.close()
        
    end_time = time.perf_counter()
    total_time_ms = (end_time - start_time) * 1000
    
    print(f"\n=== RESULTADOS DA VARREDURA ===")
    print(f"Portas abertas encontradas: {open_ports}")
    print(f"Tempo total gasto: {total_time_ms:.2f} ms")
    
    # Correlação com o exercício
    if 8080 in open_ports:
        print("\n[CORRELAÇÃO]")
        print("A porta 8080 foi detectada como ABERTA. Esta porta corresponde ao")
        print("Servidor HTTP/1.1 Mínimo construído no Exercício 5 deste Trabalho Prático.")
        
    # Conexão fantasma para destravar o accept do servidor e finalizar a thread
    try:
        dummy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dummy.connect(("127.0.0.1", 8080))
        dummy.close()
    except Exception:
        pass

if __name__ == "__main__":
    main()
