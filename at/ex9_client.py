import socket

# Exercicio 9 cliente ipv6
def main():
    try:
        s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        s.connect(("::1", 9000))
        print("ipv6 ok")
    except Exception as e:
        print("erro ipv6, tentando ipv4:", e)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 9000))
        print("ipv4 ok")
        
    try:
        s.sendall(b"sair")
        res = s.recv(1024)
        print("res:", res.decode())
    except Exception as e:
        print("erro:", e)
    finally:
        s.close()

if __name__ == "__main__":
    main()
