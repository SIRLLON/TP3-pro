import socket
import threading

# Exercicio 6 http concorrente
def handle(conn, addr):
    try:
        req = conn.recv(2048).decode(errors="ignore")
        if req:
            line = req.split("\r\n")[0]
            parts = line.split()
            path = parts[1] if len(parts) > 1 else "/"
            
            if path == "/":
                body = "home"
                status = "200 OK"
            elif path == "/health":
                body = "ok"
                status = "200 OK"
            else:
                body = "erro"
                status = "404 Not Found"
                
            res = (
                f"HTTP/1.1 {status}\r\n"
                f"Content-Type: text/plain\r\n"
                f"Content-Length: {len(body)}\r\n"
                f"Connection: close\r\n\r\n"
                f"{body}"
            )
            conn.sendall(res.encode())
            print("concorrente req:", path, "status:", status)
    except Exception as e:
        print("erro:", e)
    finally:
        conn.close()

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", 8081))
    s.listen(10)
    print("http concorrente rodando")
    threads = []
    for _ in range(3):
        try:
            conn, addr = s.accept()
            t = threading.Thread(target=handle, args=(conn, addr))
            t.daemon = True
            t.start()
            threads.append(t)
        except Exception as e:
            print("erro loop:", e)
            break
    for t in threads:
        t.join(timeout=1.0)
    s.close()

if __name__ == "__main__":
    main()
