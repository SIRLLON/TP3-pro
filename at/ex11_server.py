import socket
import os

# Exercicio 11 servidor arquivo
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", 9999))
    s.listen(1)
    print("servidor arquivo rodando")
    while True:
        try:
            conn, addr = s.accept()
            size_data = conn.recv(20).decode().strip()
            if not size_data:
                conn.close()
                continue
            total_size = int(size_data)
            print("tamanho esperado:", total_size)
            
            received = 0
            script_dir = os.path.dirname(os.path.abspath(__file__))
            out_path = os.path.join(script_dir, "recebido.txt")
            with open(out_path, "wb") as f:
                while received < total_size:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    f.write(chunk)
                    received += len(chunk)
            
            print("recebido:", received)
            conn.close()
            break
        except Exception as e:
            print("erro:", e)
            break
    s.close()

if __name__ == "__main__":
    main()
