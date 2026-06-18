import socket

# Exercicio 2 servidor
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("0.0.0.0", 5000))
    print("servidor rodando")
    while True:
        data, addr = s.recvfrom(65535)
        if not data:
            break
        print("ip:", addr[0], "porta:", addr[1], "size:", len(data))
        s.sendto(data, addr)
        # Permite parar o loop se receber um comando vazio para facilitar testes
        if data == b"sair":
            break
    s.close()

if __name__ == "__main__":
    main()
