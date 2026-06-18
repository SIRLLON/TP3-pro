import socket
import time

# Exercicio 4 conectividade
def test(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2.0)
    t0 = time.time()
    res = s.connect_ex((ip, port))
    dt = time.time() - t0
    s.close()
    print("porta:", port, "code:", res, "ms:", round(dt * 1000, 2))

def main():
    print("iniciando teste")
    test("127.0.0.1", 22)
    test("127.0.0.1", 9999)
    test("127.0.0.1", 80)

if __name__ == "__main__":
    main()
