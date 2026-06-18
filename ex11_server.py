import socket
import sys

def main():
    HOST = "127.0.0.1"
    PORT = 9995
    OUTPUT_FILENAME = "received_file.txt"
    
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_sock.bind((HOST, PORT))
        server_sock.listen(1)
        print(f"Servidor de Arquivos TCP escutando em {HOST}:{PORT}")
        
        client_sock, client_addr = server_sock.accept()
        print(f"[CONEXÃO ACEITA] Recebendo arquivo de {client_addr[0]}:{client_addr[1]}")
        
        try:
            # 1. Lê o cabeçalho de 8 bytes contendo o tamanho total do arquivo
            size_header = client_sock.recv(8)
            if not size_header or len(size_header) < 8:
                print("Erro: Não foi possível ler o cabeçalho de tamanho do arquivo.")
                return
                
            total_size = int.from_bytes(size_header, byteorder='big')
            print(f"  Tamanho total do arquivo a receber: {total_size} bytes")
            
            # 2. Recebe o conteúdo do arquivo em blocos
            received_bytes = 0
            block_size = 4096
            
            with open(OUTPUT_FILENAME, "wb") as f:
                while received_bytes < total_size:
                    # Calcula quantos bytes restam ler para não ler dados extras da conexão
                    remaining = total_size - received_bytes
                    bytes_to_read = min(block_size, remaining)
                    
                    chunk = client_sock.recv(bytes_to_read)
                    if not chunk:
                        print("Aviso: Conexão fechada prematuramente pelo cliente.")
                        break
                        
                    f.write(chunk)
                    received_bytes += len(chunk)
                    
            print(f"  Arquivo recebido e salvo como '{OUTPUT_FILENAME}' com sucesso!")
            print(f"  Total de bytes gravados: {received_bytes} bytes")
            
        except Exception as e:
            print(f"Erro durante a recepção do arquivo: {e}")
        finally:
            client_sock.close()
    finally:
        server_sock.close()
        print("Servidor de Arquivos TCP finalizado.")

if __name__ == "__main__":
    main()
