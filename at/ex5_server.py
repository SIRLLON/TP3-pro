import socket

# Exercicio 5 http
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", 8080))
    s.listen(5)
    print("http rodando")
    for _ in range(3):
        try:
            conn, addr = s.accept()
            req = conn.recv(2048).decode(errors="ignore")
            if not req:
                conn.close()
                continue
            
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
            print("req:", path, "status:", status)
            conn.close()
        except Exception as e:
            print("erro:", e)
            break
    s.close()

if __name__ == "__main__":
    main()
