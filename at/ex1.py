import socket

# Exercicio 1 socket
def main():
    configs = [
        ("IPv4 TCP", socket.AF_INET, socket.SOCK_STREAM),
        ("IPv4 UDP", socket.AF_INET, socket.SOCK_DGRAM),
        ("IPv6 TCP", socket.AF_INET6, socket.SOCK_STREAM),
        ("IPv6 UDP", socket.AF_INET6, socket.SOCK_DGRAM),
    ]
    for name, fam, tipo in configs:
        try:
            s = socket.socket(fam, tipo)
            print(name, "fam:", s.family, "tipo:", s.type, "timeout:", s.gettimeout())
            s.close()
        except Exception as e:
            print("erro:", name, e)

if __name__ == "__main__":
    main()
