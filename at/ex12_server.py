import socket
import ssl
import threading
import os

# Exercicio 12 integracao final
def handle(conn, addr):
    try:
        req = conn.recv(2048).decode(errors="ignore")
        if req:
            line = req.split("\r\n")[0]
            parts = line.split()
            path = parts[1] if len(parts) > 1 else "/"
            
            if path == "/":
                body = "integracao home"
                status = "200 OK"
            elif path == "/health":
                body = "integracao ok"
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
            print("integracao req:", path, "status:", status)
    except Exception as e:
        print("erro:", e)
    finally:
        conn.close()

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cert_path = os.path.join(script_dir, "server.crt")
    key_path = os.path.join(script_dir, "server.key")
    
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=cert_path, keyfile=key_path)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", 8444))
    s.listen(10)
    print("servidor integracao rodando")
    threads = []
    for _ in range(2):
        try:
            conn, addr = s.accept()
            tconn = context.wrap_socket(conn, server_side=True)
            t = threading.Thread(target=handle, args=(tconn, addr))
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
