import socket
import time

# Exercicio 10 port scanner
def main():
    target = "127.0.0.1"
    ports = [22, 80, 6000, 8080, 8081, 8443, 9000]
    print("escanendo target:", target)
    t0 = time.time()
    open_ports = []
    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.2)
        res = s.connect_ex((target, port))
        if res == 0:
            print("aberta:", port)
            open_ports.append(port)
        s.close()
    dt = time.time() - t0
    print("tempo:", round(dt * 1000, 2), "ms")
    print("lista:", open_ports)

if __name__ == "__main__":
    main()
