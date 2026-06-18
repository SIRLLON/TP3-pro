import socket

# Exercicio 9 servidor ipv6
def main():
    try:
        s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("::1", 9000))
        s.listen(5)
        print("ipv6 rodando")
    except Exception as e:
        print("erro ipv6, fallback ipv4:", e)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("127.0.0.1", 9000))
        s.listen(5)
        print("ipv4 rodando")
        
    while True:
        try:
            conn, addr = s.accept()
            data = conn.recv(1024)
            if data:
                print("recv:", data.decode())
                conn.sendall(b"ok")
            conn.close()
            if data == b"sair":
                break
        except Exception as e:
            print("erro:", e)
            break
    s.close()

if __name__ == "__main__":
    main()
