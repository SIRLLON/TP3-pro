import socket

def main():
    # Definição dos tipos de sockets solicitados
    socket_configs = [
        ("IPv4 + TCP", socket.AF_INET, socket.SOCK_STREAM),
        ("IPv4 + UDP", socket.AF_INET, socket.SOCK_DGRAM),
        ("IPv6 + TCP", socket.AF_INET6, socket.SOCK_STREAM),
        ("IPv6 + UDP", socket.AF_INET6, socket.SOCK_DGRAM),
    ]
    
    print("=== INVENTÁRIO MÍNIMO DE SOCKETS ===")
    
    for name, family, sock_type in socket_configs:
        try:
            # Criação do socket
            sock = socket.socket(family, sock_type)
            
            # Leitura programática das propriedades
            f_val = sock.family
            t_val = sock.type
            timeout_val = sock.gettimeout()
            
            # Mapeamento para nomes amigáveis das propriedades (se disponível no enum)
            family_name = socket.AddressFamily(f_val).name if hasattr(socket, "AddressFamily") else str(f_val)
            type_name = socket.SocketKind(t_val).name if hasattr(socket, "SocketKind") else str(t_val)
            
            print(f"\nSocket: {name}")
            print(f"  Família (Int/Enum): {f_val} ({family_name})")
            print(f"  Tipo (Int/Enum): {t_val} ({type_name})")
            print(f"  Timeout Padrão: {timeout_val}")
            
            # Encerramento correto do socket
            sock.close()
            
        except Exception as e:
            print(f"Erro ao configurar {name}: {e}")

if __name__ == "__main__":
    main()
