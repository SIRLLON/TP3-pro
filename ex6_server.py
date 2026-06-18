import socket
import threading
import sys

# Evento global para sinalizar desligamento
shutdown_event = threading.Event()
server_socket = None

def create_http_response(status_code, status_text, content_type, body_content):
    body_bytes = body_content.encode('utf-8')
    content_length = len(body_bytes)
    
    response = (
        f"HTTP/1.1 {status_code} {status_text}\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {content_length}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )
    return response.encode('utf-8') + body_bytes

def handle_client(client_sock, client_addr):
    try:
        client_sock.settimeout(5.0)
        request_data = client_sock.recv(4096).decode('utf-8', errors='ignore')
        if not request_data:
            return
        
        # Parsing da Request Line
        lines = request_data.split("\r\n")
        request_line = lines[0]
        parts = request_line.split()
        
        if len(parts) >= 2:
            method = parts[0]
            path = parts[1]
        else:
            method = "GET"
            path = "/"
            
        print(f"[CONEXÃO CONCORRENTE] {method} {path} de {client_addr[0]}:{client_addr[1]}")
        
        if method != "GET":
            body = '{"error": "Método não suportado"}'
            resp = create_http_response("405", "Method Not Allowed", "application/json", body)
        elif path == "/":
            body = (
                "<!DOCTYPE html>\n"
                "<html>\n"
                "<head><meta charset='utf-8'><title>HTTP Concorrente</title></head>\n"
                "<body>\n"
                "<h1>Servidor HTTP/1.1 Concorrente</h1>\n"
                "<p>Resposta concorrente via Threads!</p>\n"
                "</body>\n"
                "</html>"
            )
            resp = create_http_response("200", "OK", "text/html; charset=utf-8", body)
        elif path == "/health":
            body = '{"status": "healthy", "service": "concurrent-http-socket-server"}'
            resp = create_http_response("200", "OK", "application/json", body)
        elif path == "/shutdown":
            body = '{"message": "Desligando servidor concorrente..."}'
            resp = create_http_response("200", "OK", "application/json", body)
            client_sock.sendall(resp)
            client_sock.close()
            print("Comando de desligamento recebido em /shutdown. Desligando servidor concorrente...")
            shutdown_event.set()
            return
        else:
            body = '{"error": "Caminho não encontrado"}'
            resp = create_http_response("404", "Not Found", "application/json", body)
            
        client_sock.sendall(resp)
    except Exception as e:
        print(f"Erro ao tratar cliente HTTP {client_addr}: {e}")
    finally:
        client_sock.close()

def listen_loop():
    global server_socket
    HOST = "127.0.0.1"
    PORT = 8081
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(15)
        print(f"Servidor HTTP concorrente escutando em http://{HOST}:{PORT}")
        server_socket.settimeout(1.0) # Permite checar shutdown_event a cada segundo
        
        while not shutdown_event.is_set():
            try:
                client_sock, client_addr = server_socket.accept()
                t = threading.Thread(target=handle_client, args=(client_sock, client_addr), daemon=True)
                t.start()
            except socket.timeout:
                continue
            except Exception as e:
                if not shutdown_event.is_set():
                    print(f"Erro no accept: {e}")
                break
    finally:
        server_socket.close()
        print("Servidor HTTP concorrente finalizado.")

def main():
    t_server = threading.Thread(target=listen_loop, daemon=False)
    t_server.start()
    
    while t_server.is_alive():
        try:
            t_server.join(0.5)
        except KeyboardInterrupt:
            print("KeyboardInterrupt recebido no servidor concorrente.")
            shutdown_event.set()
            break

if __name__ == "__main__":
    main()
