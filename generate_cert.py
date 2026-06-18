import datetime
import ipaddress
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_self_signed_cert():
    print("Gerando chave privada RSA de 2048 bits...")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    
    print("Configurando metadados do certificado...")
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "BR"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Rio de Janeiro"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Rio de Janeiro"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Desenvolvimento Local"),
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
    ])
    
    # Certificado válido a partir de agora por 365 dias
    now = datetime.datetime.now(datetime.timezone.utc)
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now)
        .not_valid_after(now + datetime.timedelta(days=365))
        .add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.IPAddress(ipaddress.ip_address("127.0.0.1")),
            ]),
            critical=False,
        )
        .sign(private_key, hashes.SHA256())
    )
    
    # Salvando a chave privada
    print("Salvando chave privada em 'server.key'...")
    with open("server.key", "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )
        
    # Salvando o certificado
    print("Salvando certificado em 'server.crt'...")
    with open("server.crt", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
        
    print("Certificado e chave privada gerados com sucesso!")

if __name__ == "__main__":
    generate_self_signed_cert()
