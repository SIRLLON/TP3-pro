import socket
import ssl

# Exercicio 8 cliente tls
def main():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn = context.wrap_socket(s, server_hostname="localhost")
    try:
        conn.connect(("127.0.0.1", 8443))
        conn.sendall(b"sair")
        res = conn.recv(1024)
        print("res:", res.decode())
    except Exception as e:
        print("erro:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
