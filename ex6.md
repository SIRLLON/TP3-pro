# Servidor HTTP Concorrente

Demonstração prática de um servidor HTTP/1.1 concorrente capaz de receber e processar requisições HTTP paralelas sem bloqueio de E/S em ambiente Linux.

## 1. Execução do Servidor HTTP Concorrente e Teste de Carga no Linux

O servidor [ex6_server.py](file:///c:/Users/sirll/OneDrive/Área de Trabalho/Estrutura/TP3/ex6_server.py) foi iniciado em segundo plano na VM Linux na porta 8081. Um script em lote do shell disparou 5 requisições paralelas simuladas ao endpoint `/health`.

### Saída da Execução Paralela de Curls (Evidência Objetiva no Linux)
```text
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 65
Connection: close
{"status": "healthy", "service": "concurrent-http-socket-server"}

HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 65
Connection: close
{"status": "healthy", "service": "concurrent-http-socket-server"}

HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 65
Connection: close
{"status": "healthy", "service": "concurrent-http-socket-server"}

HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 65
Connection: close
{"status": "healthy", "service": "concurrent-http-socket-server"}

HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 65
Connection: close
{"status": "healthy", "service": "concurrent-http-socket-server"}
```

### Logs do Servidor Concorrente (Linux VM)
```text
Servidor HTTP concorrente escutando em http://127.0.0.1:8081
[CONEXÃO CONCORRENTE] GET /health de 127.0.0.1:47816
[CONEXÃO CONCORRENTE] GET /health de 127.0.0.1:47828
[CONEXÃO CONCORRENTE] GET /health de 127.0.0.1:47830
[CONEXÃO CONCORRENTE] GET /health de 127.0.0.1:47838
[CONEXÃO CONCORRENTE] GET /health de 127.0.0.1:47848
[CONEXÃO CONCORRENTE] GET /shutdown de 127.0.0.1:47854
Comando de desligamento recebido em /shutdown. Desligando servidor concorrente...
Servidor HTTP concorrente finalizado.
```

---

## 2. Justificativa Técnica

### Como a implementação evita o bloqueio?
A thread principal executa em um loop contínuo e fica aguardando conexões no método bloqueante `accept()`.
Assim que uma nova conexão chega, a thread principal aceita a conexão e, em vez de ler e processar os cabeçalhos HTTP de forma síncrona (o que bloquearia a escuta de novos clientes), ela instancia e inicia uma nova thread de execução:
```python
t = threading.Thread(target=handle_client, args=(client_sock, client_addr), daemon=True)
t.start()
```
A nova thread passa a ser responsável exclusiva por ler os dados da requisição com `recv()`, processá-la e enviar a resposta HTTP. A thread principal retorna imediatamente para a chamada `accept()` seguinte. Desse modo, se um cliente demorar para transmitir sua requisição, ele bloqueará apenas a sua thread dedicada, permitindo que outros clientes acessem o servidor normalmente.

### Limitações conhecidas do servidor construído
1. **Sem Pool de Threads (Thread Exhaustion)**: O servidor cria uma thread nova para cada conexão. Se receber uma rajada de milhares de requisições simultâneas, o sistema operacional gastará muita CPU com trocas de contexto e poderá ficar sem memória devido ao espaço de pilha reservado para cada thread, causando a queda do servidor.
2. **Sem persistência (HTTP Keep-Alive)**: O servidor fecha a conexão imediatamente após uma única resposta (`Connection: close`). Isso força o cliente a abrir um novo handshake TCP de 3 vias a cada imagem ou arquivo CSS carregado, aumentando a latência e o overhead na rede.
3. **GIL (Global Interpreter Lock) do Python**: O Python usa o bloqueio global da thread (GIL), o que significa que apenas uma thread Python pode executar código de bytecode Python de forma real em processadores multi-core de cada vez. Embora threads funcionem muito bem para I/O-bound (como esperar pacotes na rede), elas não se traduzem em ganho de desempenho real se o processamento envolver lógica pesada de computação (CPU-bound).
