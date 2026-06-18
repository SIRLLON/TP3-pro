# Inventário Mínimo do Pacote Socket: TCP vs UDP e IPv4 vs IPv6

Inventário objetivo das configurações estruturais de sockets para demonstrar domínio de famílias de endereços, tipos de transporte e timeouts padrão sob o Linux (Ubuntu VirtualBox).

## 1. Execução do Script de Inventário

O script Python [ex1.py](file:///c:/Users/sirll/OneDrive/Área de Trabalho/Estrutura/TP3/ex1.py) foi copiado e executado dentro da VM Linux.

Comando executado:
```bash
python3 ex1.py
```

### Saída do Script (Evidência Objetiva no Linux)
```text
=== INVENTÁRIO MÍNIMO DE SOCKETS ===

Socket: IPv4 + TCP
  Família (Int/Enum): 2 (AF_INET)
  Tipo (Int/Enum): 1 (SOCK_STREAM)
  Timeout Padrão: None

Socket: IPv4 + UDP
  Família (Int/Enum): 2 (AF_INET)
  Tipo (Int/Enum): 2 (SOCK_DGRAM)
  Timeout Padrão: None

Socket: IPv6 + TCP
  Família (Int/Enum): 10 (AF_INET6)
  Tipo (Int/Enum): 1 (SOCK_STREAM)
  Timeout Padrão: None

Socket: IPv6 + UDP
  Família (Int/Enum): 10 (AF_INET6)
  Tipo (Int/Enum): 2 (SOCK_DGRAM)
  Timeout Padrão: None
```

---

## 2. Justificativa Técnica

### Por que TCP e UDP exigem estruturas de código diferentes?
O TCP (`SOCK_STREAM`) é um protocolo orientado a conexão e confiável. Ele opera como um fluxo contínuo de bytes (stream), exigindo um handshake de três vias antes da troca de dados. Estruturalmente, o servidor TCP precisa de `listen()` e `accept()` para receber conexões de entrada de novos sockets exclusivos para conversa, e o cliente precisa de `connect()`. A leitura/escrita ocorre via `recv()` e `send()`.

O UDP (`SOCK_DGRAM`) é um protocolo não orientado a conexão e não confiável, enviando dados em pacotes individuais delimitados (datagramas). Estruturalmente, não há handshake, `listen()`, `accept()` ou `connect()`. A comunicação ocorre diretamente enviando a mensagem e indicando o endereço de destino explicitamente em cada envio com `sendto()`, e lendo com `recvfrom()`, o qual fornece os dados e o par IP/porta de origem simultaneamente.

### Como essa distinção impacta os próximos exercícios do TP?
Essa distinção molda completamente a estrutura do código:
1. **Exercícios UDP (Ex. 2)**: O código usará `bind()`, `recvfrom()` e `sendto()`. Não haverá gerenciamento de estado de conexão nem laço para aceitar novos clientes.
2. **Exercícios TCP e HTTP (Ex. 3, 5, 6, 8, 9, 11 e 12)**: Exigirão a criação de conexões dedicadas e primitivas de controle, manipulação concorrente das conexões aceitas (threads) para evitar o bloqueio do socket de escuta, e o tratamento das mensagens como um fluxo de bytes, obrigando o encerramento explícito (`close()`) ou leitura em blocos.
