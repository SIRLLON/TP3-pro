import socket
import os

# Exercicio 11 cliente arquivo
def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(script_dir, "enviar.txt")
    with open(filename, "w") as f:
        f.write("A" * 5000)
        
    size = os.path.getsize(filename)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("127.0.0.1", 9999))
        s.sendall(f"{size:<20}".encode())
        
        with open(filename, "rb") as f:
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break
                s.sendall(chunk)
        print("enviado:", size)
    except Exception as e:
        print("erro:", e)
    finally:
        s.close()

if __name__ == "__main__":
    main()
