import socket
import ssl
import sys

def main():
    hostname = "www.google.com"
    port = 443
    
    print(f"=== CLIENTE TLS: CONECTANDO A HTTPS://{hostname}:{port} ===")
    
    # Cria o contexto SSL padrão (carrega os certificados CA confiáveis do sistema)
    context = ssl.create_default_context()
    
    try:
        # Abre conexão TCP
        raw_sock = socket.create_connection((hostname, port), timeout=5.0)
        
        # Realiza o handshake TLS sobre a conexão TCP
        with context.wrap_socket(raw_sock, server_hostname=hostname) as tls_sock:
            print("\n[Handshake TLS Completado com Sucesso]")
            
            # 1. Informações do canal seguro
            tls_version = tls_sock.version()
            cipher_negotiated = tls_sock.cipher()
            print(f"  Versão TLS: {tls_version}")
            print(f"  Cipher Negociado: {cipher_negotiated[0]} ({cipher_negotiated[1]} - {cipher_negotiated[2]} bits)")
            
            # 2. Informações estruturadas do certificado (JSON-like)
            cert = tls_sock.getpeercert()
            print("\n[Detalhes do Certificado do Servidor]")
            
            # Extrai o Issuer
            issuer = dict(x[0] for x in cert.get('issuer', []))
            print(f"  Emissor (Issuer):")
            for key, val in issuer.items():
                print(f"    {key}: {val}")
                
            # Extrai a Validade
            not_before = cert.get('notBefore')
            not_after = cert.get('notAfter')
            print(f"  Período de Validade:")
            print(f"    Válido a partir de (Not Before): {not_before}")
            print(f"    Válido até (Not After): {not_after}")
            
            # 3. Obtém o certificado bruto (DER) e o converte para PEM (Base64)
            der_cert = tls_sock.getpeercert(binary_form=True)
            pem_cert = ssl.DER_cert_to_PEM_cert(der_cert)
            
            # Escreve o certificado PEM em arquivo
            pem_filename = "google_cert.pem"
            with open(pem_filename, "w", encoding="utf-8") as f:
                f.write(pem_cert)
                
            print(f"\nCertificado PEM obtido e salvo em '{pem_filename}' com sucesso.")
            
            # Exibe as primeiras 4 linhas do certificado PEM como evidência
            print("\nTrecho inicial do Certificado PEM (Evidência):")
            pem_lines = pem_cert.strip().split("\n")
            for line in pem_lines[:5]:
                print(f"  {line}")
            print("  ...")
            for line in pem_lines[-2:]:
                print(f"  {line}")
                
    except Exception as e:
        print(f"Erro na conexão TLS: {e}")

if __name__ == "__main__":
    main()
