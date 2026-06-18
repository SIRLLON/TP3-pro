import socket
import ssl
import threading
import sys

# Evento global para controle de desligamento
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
        
        # Parsing HTTP
        lines = request_data.split("\r\n")
        request_line = lines[0]
        parts = request_line.split()
        
        if len(parts) >= 2:
            method = parts[0]
            path = parts[1]
        else:
            method = "GET"
            path = "/"
            
        print(f"[REQUISIÇÃO HTTPS] {client_addr[0]}:{client_addr[1]} -> {method} {path}")
        
        # Roteamento
        if method != "GET":
            body = '{"error": "Metodo nao suportado"}'
            resp = create_http_response("405", "Method Not Allowed", "application/json", body)
        elif path == "/":
            body = (
                "<!DOCTYPE html>\n"
                "<html>\n"
                "<head><meta charset='utf-8'><title>Servico Consolidado</title></head>\n"
                "<body>\n"
                "<h1>Serviço HTTP Consolidado sobre TLS (HTTPS)</h1>\n"
                "<p>Integração final concluída com sucesso!</p>\n"
                "</body>\n"
                "</html>"
            )
            resp = create_http_response("200", "OK", "text/html; charset=utf-8", body)
        elif path == "/health":
            body = '{"status": "healthy", "service": "consolidated-https-server", "concurrency": "threads"}'
            resp = create_http_response("200", "OK", "application/json", body)
        elif path == "/shutdown":
            body = '{"message": "Desligando servico consolidado..."}'
            resp = create_http_response("200", "OK", "application/json", body)
            client_sock.sendall(resp)
            client_sock.close()
            print("[SHUTDOWN] Sinalizador de encerramento ativado.")
            shutdown_event.set()
            return
        else:
            body = '{"error": "Nao encontrado"}'
            resp = create_http_response("404", "Not Found", "application/json", body)
            
        client_sock.sendall(resp)
    except ssl.SSLError as se:
        print(f"Erro na negociação TLS de {client_addr}: {se}")
    except Exception as e:
        print(f"Erro ao tratar conexao de {client_addr}: {e}")
    finally:
        client_sock.close()

def listen_loop():
    global server_socket
    HOST = "127.0.0.1"
    PORT = 8443
    
    # Configura contexto TLS do servidor
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    try:
        context.load_cert_chain(certfile="server.crt", keyfile="server.key")
    except Exception as e:
        print(f"Erro crítico ao carregar certificados TLS: {e}")
        return
        
    # Inicializa socket TCP principal
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(20)
        print(f"Serviço HTTPS consolidado escutando em https://{HOST}:{PORT}")
        server_socket.settimeout(1.0)
        
        while not shutdown_event.is_set():
            try:
                raw_sock, client_addr = server_socket.accept()
                # Envelopa com TLS antes de disparar a thread
                try:
                    tls_sock = context.wrap_socket(raw_sock, server_side=True)
                    t = threading.Thread(target=handle_client, args=(tls_sock, client_addr), daemon=True)
                    t.start()
                except Exception as wrap_err:
                    print(f"Erro no handshake TLS inicial: {wrap_err}")
                    raw_sock.close()
            except socket.timeout:
                continue
            except Exception as e:
                if not shutdown_event.is_set():
                    print(f"Erro no accept: {e}")
                break
    finally:
        server_socket.close()
        print("Serviço HTTPS consolidado finalizado.")

def main():
    t_server = threading.Thread(target=listen_loop, daemon=False)
    t_server.start()
    
    while t_server.is_alive():
        try:
            t_server.join(0.5)
        except KeyboardInterrupt:
            print("KeyboardInterrupt recebido no serviço consolidado.")
            shutdown_event.set()
            break

if __name__ == "__main__":
    main()
