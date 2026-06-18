# Falha e Diagnóstico com connect_ex()

Diagnóstico prático de conectividade TCP utilizando a função nativa `connect_ex()` para inferir o estado de portas (aberta, fechada, filtrada) com medição de tempo de resposta sob ambiente Linux.

## 1. Execução do Script de Diagnóstico no Linux

O script [ex4.py](file:///c:/Users/sirll/OneDrive/Área de Trabalho/Estrutura/TP3/ex4.py) foi copiado e executado dentro da VM Linux.

Comando executado:
```bash
python3 ex4.py
```

### Saída de Evidência (Logs de Diagnóstico no Linux)
```text
=== DIAGNÓSTICO DE PORTAS COM connect_ex() ===

--- Teste 1: Porta Aberta (Servidor temporário local na porta 9997) ---
Alvo: 127.0.0.1:9997
  Código retornado: 0
  Estado inferido: ABERTA (Success)
  Tempo decorrido: 0.33 ms

--- Teste 2: Porta Fechada (Porta local 12345) ---
Alvo: 127.0.0.1:12345
  Código retornado: 111
  Estado inferido: FECHADA (Connection Refused)
  Tempo decorrido: 0.61 ms

--- Teste 3: Porta Conhecida do Sistema / Externa (google.com:80) ---
Alvo: google.com:80
  Código retornado: 0
  Estado inferido: ABERTA (Success)
  Tempo decorrido: 32.78 ms

--- Teste 4: Porta Filtrada (IP inalcançável 10.255.255.1:80 com timeout de 1.5s) ---
Alvo: 10.255.255.1:80
  Código retornado: 11
  Estado inferido: FILTRADA (Timeout atingido no socket não-bloqueante)
  Tempo decorrido: 1501.99 ms
```

---

## 2. Justificativa Técnica

### Como os códigos retornados permitem inferir o estado da porta?
A função `connect_ex()` do socket TCP retorna o código de erro diretamente da pilha de rede do sistema operacional (C-style socket API) em vez de lançar exceções Python.
- **Código `0`**: Indica sucesso. A conexão TCP completou o handshake de três vias (SYN-SYNACK-ACK). A porta está **aberta** e há um serviço ativamente escutando.
- **Código `111` (`ECONNREFUSED` no Linux)**: O host remoto respondeu imediatamente com um pacote TCP com a flag RST (Reset). A pilha TCP do destino informou que o host está ativo, mas a porta alvo está **fechada** (nenhum serviço escutando nela).
- **Código `11` (`EAGAIN`/`EWOULDBLOCK` no Linux)** ou **`110` (`ETIMEDOUT` / Timeout)**: Ocorre quando nenhuma resposta (nem SYNACK, nem RST) é recebida antes do timeout expirar. Isso indica que os pacotes foram descartados silenciosamente na rede, sugerindo uma porta **filtrada** por firewall ou que o host remoto está offline.

### Por que essa abordagem é preferível a tratar apenas exceções genéricas?
1. **Evita overhead de exceções**: Em Python, disparar e capturar exceções (`try-except`) é computacionalmente caro quando executado milhares de vezes (ex: em scanners de portas). O uso de `connect_ex()` simplifica o fluxo usando estruturas de decisão `if-else` mais rápidas e limpas.
2. **Granularidade do Diagnóstico**: Tratar apenas uma exceção genérica (`socket.error` ou `ConnectionError`) agrupa falhas diferentes sob uma mesma categoria. Com `connect_ex()`, diferenciamos instantaneamente uma rejeição direta (RST, porta fechada) de um timeout silencioso (firewall filtrando). Isso permite decisões de automação de rede muito mais precisas, como indicar ao operador se o problema é o serviço estar inativo (Closed) ou um firewall bloqueando o tráfego (Filtered).
