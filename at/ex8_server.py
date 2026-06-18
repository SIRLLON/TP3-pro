import socket
import ssl
import os

# Exercicio 8 servidor tls
def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cert_path = os.path.join(script_dir, "server.crt")
    key_path = os.path.join(script_dir, "server.key")
    
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=cert_path, keyfile=key_path)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", 8443))
    s.listen(5)
    
    print("servidor tls rodando")
    while True:
        try:
            conn, addr = s.accept()
            tconn = context.wrap_socket(conn, server_side=True)
            data = tconn.recv(1024)
            if data:
                print("recv:", data.decode())
                tconn.sendall(b"ok")
            tconn.close()
            # Flag para encerrar apos primeira conexao nos testes
            if data == b"sair":
                break
        except Exception as e:
            print("erro:", e)
            break
    s.close()

if __name__ == "__main__":
    main()
