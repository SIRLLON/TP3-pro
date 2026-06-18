import socket
import ssl

# Exercicio 7 tls cliente
def main():
    host = "www.google.com"
    context = ssl.create_default_context()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn = context.wrap_socket(s, server_hostname=host)
    try:
        conn.connect((host, 443))
        cert = conn.getpeercert()
        cipher = conn.cipher()
        version = conn.version()
        
        issuer = dict(x[0] for x in cert['issuer'])
        issuer_cn = issuer.get('commonName', '')
        not_before = cert.get('notBefore', '')
        not_after = cert.get('notAfter', '')
        
        print("host:", host)
        print("tls version:", version)
        print("cipher:", cipher[0])
        print("issuer cn:", issuer_cn)
        print("validade de:", not_before, "ate:", not_after)
        
        pem_cert = ssl.DER_cert_to_PEM_cert(conn.getpeercert(binary_form=True))
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        cert_path = os.path.join(script_dir, "google_cert.pem")
        with open(cert_path, "w") as f:
            f.write(pem_cert)
        print("certificado salvo pem")
    except Exception as e:
        print("erro:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
