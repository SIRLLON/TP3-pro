import socket
import sys

def create_http_response(status_code, status_text, content_type, body_content):
    body_bytes = body_content.encode('utf-8')
    content_length = len(body_bytes)
    
    # Monta os cabeçalhos HTTP/1.1
    response = (
        f"HTTP/1.1 {status_code} {status_text}\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {content_length}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )
    return response.encode('utf-8') + body_bytes

def main():
    HOST = "127.0.0.1"
    PORT = 8080
    
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_sock.bind((HOST, PORT))
        server_sock.listen(5)
        print(f"Servidor HTTP puro rodando em http://{HOST}:{PORT}")
        
        while True:
            client_sock, client_addr = server_sock.accept()
            try:
                request_data = client_sock.recv(4096).decode('utf-8', errors='ignore')
                if not request_data:
                    client_sock.close()
                    continue
                
                # Parsing mínimo da Request Line (ex: "GET /health HTTP/1.1")
                lines = request_data.split("\r\n")
                request_line = lines[0]
                parts = request_line.split()
                
                if len(parts) >= 2:
                    method = parts[0]
                    path = parts[1]
                else:
                    method = "GET"
                    path = "/"
                
                print(f"[REQUISIÇÃO] {method} {path} de {client_addr[0]}:{client_addr[1]}")
                
                # Roteamento básico
                if method != "GET":
                    body = '{"error": "Método não suportado. Use apenas GET"}'
                    resp = create_http_response("405", "Method Not Allowed", "application/json", body)
                elif path == "/":
                    body = (
                        "<!DOCTYPE html>\n"
                        "<html>\n"
                        "<head><meta charset='utf-8'><title>Servidor HTTP Puro</title></head>\n"
                        "<body>\n"
                        "<h1>Servidor HTTP/1.1 Mínimo Puro</h1>\n"
                        "<p>Página inicial respondida com sucesso!</p>\n"
                        "</body>\n"
                        "</html>"
                    )
                    resp = create_http_response("200", "OK", "text/html; charset=utf-8", body)
                elif path == "/health":
                    body = '{"status": "healthy", "service": "http-socket-server"}'
                    resp = create_http_response("200", "OK", "application/json", body)
                elif path == "/shutdown":
                    body = '{"message": "Desligando servidor..."}'
                    resp = create_http_response("200", "OK", "application/json", body)
                    client_sock.sendall(resp)
                    client_sock.close()
                    print("Comando de desligamento recebido no endpoint /shutdown. Encerrando...")
                    break
                else:
                    body = '{"error": "Caminho não encontrado"}'
                    resp = create_http_response("404", "Not Found", "application/json", body)
                
                client_sock.sendall(resp)
            except Exception as e:
                print(f"Erro no processamento do cliente: {e}")
            finally:
                client_sock.close() # Encerramento obrigatório da conexão após resposta
    finally:
        server_sock.close()
        print("Servidor HTTP finalizado.")

if __name__ == "__main__":
    main()
