import socket
import sys
import time

def main():
    HOST = "127.0.0.1"
    PORT = 9999
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2.0)  # Timeout de 2 segundos para respostas
    
    # Criamos 10 mensagens de tamanhos variados
    # A última envia SHUTDOWN para encerrar o servidor
    messages = [
        (1, "Mensagem basica 1", 20),
        (2, "Mensagem basica 2", 50),
        (3, "Mensagem media", 1024),          # 1 KB
        (4, "Mensagem media-alta", 8192),      # 8 KB
        (5, "Mensagem grande", 32768),         # 32 KB
        (6, "Mensagem proxima ao limite", 60000), # 60 KB
        (7, "Mensagem no limite", 65507),      # Limite maximo teórico do UDP IPv4
        (8, "Mensagem excedendo limite", 70000), # 70 KB (deve gerar erro no envio)
        (9, "Outra mensagem basica", 30),
        (10, "Comando SHUTDOWN final", 100)
    ]
    
    print("=== CLIENTE UDP INICIANDO TRANSMISSÃO ===")
    
    received_ids = []
    
    for msg_id, label, size in messages:
        # Gerando payload com o tamanho especificado
        prefix = f"ID:{msg_id} | {label} | "
        if msg_id == 10:
            payload = (prefix + "SHUTDOWN").encode()
        else:
            padding_len = max(0, size - len(prefix))
            payload = (prefix + ("A" * padding_len)).encode()
            
        print(f"\n[ENVIO] ID {msg_id}: Enviando {len(payload)} bytes...")
        
        try:
            sock.sendto(payload, (HOST, PORT))
            
            # Tenta receber o eco
            try:
                data, addr = sock.recvfrom(65535)
                # Extrai o ID da mensagem retornada
                response_str = data.decode('utf-8', errors='ignore')
                if "ID:" in response_str:
                    ret_id = int(response_str.split(" | ")[0].split(":")[1])
                    received_ids.append(ret_id)
                print(f"[RETORNO] ID {msg_id} recebido com sucesso de {addr[0]}:{addr[1]}")
            except socket.timeout:
                print(f"[TIMEOUT] ID {msg_id} expirou (sem resposta)")
                
        except Exception as e:
            print(f"[ERRO NO ENVIO] ID {msg_id} falhou ao enviar: {e}")
            
        time.sleep(0.1) # Pequena pausa entre envios
        
    sock.close()
    
    print("\n=== RELATÓRIO DE ENTREGAS UDP ===")
    print(f"IDs enviados com sucesso no transporte: {[m[0] for m in messages]}")
    print(f"IDs ecoados e recebidos: {received_ids}")
    lost_ids = set([m[0] for m in messages if m[0] != 8]) - set(received_ids)
    print(f"IDs perdidos (excluindo erro de buffer excedido): {list(lost_ids)}")

if __name__ == "__main__":
    main()
