import subprocess
import os

# Exercicio 8 gera certificado
def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    key_path = os.path.join(script_dir, "server.key")
    crt_path = os.path.join(script_dir, "server.crt")
    cmd = [
        "openssl", "req", "-newkey", "rsa:2048", "-nodes",
        "-keyout", key_path, "-x509", "-days", "365",
        "-out", crt_path, "-subj", "/CN=localhost"
    ]
    res = subprocess.run(cmd, capture_output=True)
    if res.returncode == 0:
        print("cert ok")
    else:
        print("erro:", res.stderr.decode())

if __name__ == "__main__":
    main()
