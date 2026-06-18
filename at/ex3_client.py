import socket
import sys

# Exercicio 3 cliente
def main():
    name = sys.argv[1] if len(sys.argv) > 1 else "cli_default"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("127.0.0.1", 6000))
        s.sendall(name.encode())
        res = s.recv(1024)
        print("cli:", name, "res:", res.decode())
    except Exception as e:
        print("erro:", name, e)
    finally:
        s.close()

if __name__ == "__main__":
    main()
