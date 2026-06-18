import socket
import threading

# Exercicio 3 servidor
def handle(conn, addr):
    try:
        data = conn.recv(1024)
        if data:
            print("con:", addr[0], addr[1], "msg:", data.decode())
            conn.sendall(b"OK")
    except Exception as e:
        print("erro:", e)
    finally:
        conn.close()

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", 6000))
    s.listen(5)
    print("servidor ouvindo")
    threads = []
    for _ in range(5):
        try:
            conn, addr = s.accept()
            t = threading.Thread(target=handle, args=(conn, addr))
            t.daemon = True
            t.start()
            threads.append(t)
        except Exception:
            break
    for t in threads:
        t.join(timeout=1.0)
    s.close()

if __name__ == "__main__":
    main()
