import socket

# Exercicio 2 cliente
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(2.0)
    server_addr = ("127.0.0.1", 5000)
    
    for i in range(1, 11):
        msg = f"msg {i}"
        s.sendto(msg.encode(), server_addr)
        try:
            data, addr = s.recvfrom(65535)
            print("recebido id:", i, "payload:", data.decode())
        except socket.timeout:
            print("timeout id:", i)
            
    sizes = [100, 1000, 5000, 10000, 50000]
    for size in sizes:
        msg = b"A" * size
        s.sendto(msg, server_addr)
        try:
            data, addr = s.recvfrom(65535)
            print("enviei:", size, "recebi:", len(data))
        except socket.timeout:
            print("timeout tam:", size)
            
    # Fecha servidor no final
    s.sendto(b"sair", server_addr)
    s.close()

if __name__ == "__main__":
    main()
