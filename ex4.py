import socket
import time
import errno

def translate_error(code, is_timeout_test=False):
    if code == 0:
        return "ABERTA (Success)"
    
    # WSA (Windows) e errno codes
    errors = {
        10061: "FECHADA (WSAECONNREFUSED - Connection Refused)",
        10060: "FILTRADA/TIMEOUT (WSAETIMEDOUT - Connection Timed Out)",
        10035: "FILTRADA/TIMEOUT (WSAEWOULDBLOCK - Operation Would Block)",
        errno.ECONNREFUSED: "FECHADA (Connection Refused)",
        errno.ETIMEDOUT: "FILTRADA/TIMEOUT (Connection Timed Out)",
    }
    
    if code == 10035 or code == errno.EWOULDBLOCK:
        if is_timeout_test:
            return "FILTRADA (Timeout atingido no socket não-bloqueante)"
        return "NÃO-BLOQUEANTE (Operação em andamento - WSAEWOULDBLOCK)"
        
    return errors.get(code, f"FALHA/OUTRO ERRO (Código: {code})")

def test_port(host, port, timeout=None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    is_timeout_test = False
    if timeout is not None:
        sock.settimeout(timeout)
        is_timeout_test = True
        
    start_time = time.perf_counter()
    result_code = sock.connect_ex((host, port))
    end_time = time.perf_counter()
    
    elapsed_ms = (end_time - start_time) * 1000
    status = translate_error(result_code, is_timeout_test)
    
    print(f"Alvo: {host}:{port}")
    print(f"  Código retornado: {result_code}")
    print(f"  Estado inferido: {status}")
    print(f"  Tempo decorrido: {elapsed_ms:.2f} ms\n")
    
    sock.close()
    return result_code, elapsed_ms

def main():
    print("=== DIAGNÓSTICO DE PORTAS COM connect_ex() ===\n")
    
    # 1. Porta aberta localmente
    temp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    temp_server.bind(("127.0.0.1", 9997))
    temp_server.listen(1)
    
    print("--- Teste 1: Porta Aberta (Servidor temporário local na porta 9997) ---")
    test_port("127.0.0.1", 9997)
    
    temp_server.close()
    
    # 2. Porta fechada localmente
    print("--- Teste 2: Porta Fechada (Porta local 12345) ---")
    test_port("127.0.0.1", 12345)
    
    # 3. Porta conhecida de sistema (google.com:80)
    print("--- Teste 3: Porta Conhecida do Sistema / Externa (google.com:80) ---")
    test_port("google.com", 80)
    
    # 4. Porta filtrada (causa timeout)
    print("--- Teste 4: Porta Filtrada (IP inalcançável 10.255.255.1:80 com timeout de 1.5s) ---")
    test_port("10.255.255.1", 80, timeout=1.5)

if __name__ == "__main__":
    main()
