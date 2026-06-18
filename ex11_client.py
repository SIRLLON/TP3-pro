import socket
import os
import sys

def generate_sample_file(filename, size_kb=50):
    # Gera um arquivo de texto com frases repetidas de tamanho aproximado
    print(f"[CLIENTE] Gerando arquivo de teste '{filename}' com {size_kb} KB...")
    line = "Esta e uma linha de teste para verificar a transferencia de arquivos via socket TCP puro.\n"
    line_bytes = line.encode('utf-8')
    repeats = (size_kb * 1024) // len(line_bytes)
    
    with open(filename, "wb") as f:
        for _ in range(repeats):
            f.write(line_bytes)
            
    print(f"[CLIENTE] Arquivo '{filename}' gerado com {os.path.getsize(filename)} bytes.")

def main():
    HOST = "127.0.0.1"
    PORT = 9995
    INPUT_FILENAME = "original_file.txt"
    
    # Se o arquivo não existir, gera um arquivo de teste de 50 KB
    if not os.path.exists(INPUT_FILENAME):
        generate_sample_file(INPUT_FILENAME, size_kb=50)
        
    file_size = os.path.getsize(INPUT_FILENAME)
    
    print(f"\n=== CLIENTE DE ARQUIVOS TCP INICIANDO TRANSMISSÃO ===")
    print(f"Arquivo de Origem: '{INPUT_FILENAME}' ({file_size} bytes)")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
        print(f"[CONECTADO] Envio iniciado para {HOST}:{PORT}")
        
        # 1. Envia o cabeçalho de 8 bytes com o tamanho do arquivo em formato big-endian
        size_header = file_size.to_bytes(8, byteorder='big')
        sock.sendall(size_header)
        print("  Cabeçalho de tamanho enviado.")
        
        # 2. Envia o arquivo em blocos de 4096 bytes
        block_size = 4096
        sent_bytes = 0
        
        with open(INPUT_FILENAME, "rb") as f:
            while True:
                chunk = f.read(block_size)
                if not chunk:
                    break
                sock.sendall(chunk)
                sent_bytes += len(chunk)
                
        print(f"  Envio de conteúdo concluído!")
        print(f"  Total de bytes transmitidos: {sent_bytes} bytes")
        
    except Exception as e:
        print(f"Erro durante o envio do arquivo: {e}")
    finally:
        sock.close()
        print("Conexão fechada.")

if __name__ == "__main__":
    main()
