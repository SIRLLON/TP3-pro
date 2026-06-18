# TCP: Servidor Concorrente Mínimo e Múltiplos Clientes

Demonstração prática de um servidor TCP capaz de tratar conexões de múltiplos clientes concorrentemente através de threads nativas em ambiente Linux.

## 1. Execução do Servidor e Clientes TCP Concorrentes no Linux

O servidor [ex3_server.py](file:///c:/Users/sirll/OneDrive/Área de Trabalho/Estrutura/TP3/ex3_server.py) foi executado em segundo plano e, em seguida, o script multi-cliente [ex3_client.py](file:///c:/Users/sirll/OneDrive/Área de Trabalho/Estrutura/TP3/ex3_client.py) foi disparado para iniciar 5 conexões simultâneas de clientes e enviar a mensagem final de desligamento.

### Logs do Servidor TCP (Linux VM)
```text
Servidor TCP concorrente escutando em 127.0.0.1:9998
[CONEXÃO ACEITA] Cliente: 127.0.0.1:53582
[REQUISIÇÃO] De 127.0.0.1:53582: 'Requisicao do Cliente #1'
[CONEXÃO FECHADA] Cliente: 127.0.0.1:53582
[CONEXÃO ACEITA] Cliente: 127.0.0.1:53596
[REQUISIÇÃO] De 127.0.0.1:53596: 'Requisicao do Cliente #2'
[CONEXÃO FECHADA] Cliente: 127.0.0.1:53596
[CONEXÃO ACEITA] Cliente: 127.0.0.1:53608
[REQUISIÇÃO] De 127.0.0.1:53608: 'Requisicao do Cliente #3'
[CONEXÃO FECHADA] Cliente: 127.0.0.1:53608
[CONEXÃO ACEITA] Cliente: 127.0.0.1:53618
[REQUISIÇÃO] De 127.0.0.1:53618: 'Requisicao do Cliente #4'
[CONEXÃO FECHADA] Cliente: 127.0.0.1:53618
[CONEXÃO ACEITA] Cliente: 127.0.0.1:53634
[REQUISIÇÃO] De 127.0.0.1:53634: 'Requisicao do Cliente #5'
[CONEXÃO FECHADA] Cliente: 127.0.0.1:53634
[CONEXÃO ACEITA] Cliente: 127.0.0.1:53636
[REQUISIÇÃO] De 127.0.0.1:53636: 'SHUTDOWN'
Comando de SHUTDOWN recebido de um cliente. Iniciando desligamento...
[CONEXÃO FECHADA] Cliente: 127.0.0.1:53636
Servidor TCP finalizado.
```

### Logs de Saída do Cliente TCP (Linux VM)
```text
=== CLIENTE TCP CONCORRENTE INICIANDO ===
[CLIENTE #1] Enviando: 'Requisicao do Cliente #1'
[CLIENTE #1] Resposta recebida: 'Echo Servidor TCP Concorrente: Recebido 'Requisicao do Cliente #1''
[CLIENTE #2] Enviando: 'Requisicao do Cliente #2'
[CLIENTE #2] Resposta recebida: 'Echo Servidor TCP Concorrente: Recebido 'Requisicao do Cliente #2''
[CLIENTE #3] Enviando: 'Requisicao do Cliente #3'
[CLIENTE #3] Resposta recebida: 'Echo Servidor TCP Concorrente: Recebido 'Requisicao do Cliente #3''
[CLIENTE #4] Enviando: 'Requisicao do Cliente #4'
[CLIENTE #4] Resposta recebida: 'Echo Servidor TCP Concorrente: Recebido 'Requisicao do Cliente #4''
[CLIENTE #5] Enviando: 'Requisicao do Cliente #5'
[CLIENTE #5] Resposta recebida: 'Echo Servidor TCP Concorrente: Recebido 'Requisicao do Cliente #5''

--- Conexões dos 5 clientes finalizadas. Enviando sinal de SHUTDOWN para o servidor. ---
```

---

## 2. Justificativa Técnica

### Modelo de Concorrência Adotado
Adotou-se o modelo **Multithreading** (Thread por Conexão ou *Thread-per-Connection*). O loop principal do servidor executa bloqueado em `accept()`. Ao aceitar uma nova conexão TCP, ele delega a leitura, processamento e resposta dos dados para uma nova thread independente criada via classe `threading.Thread`. O loop principal retorna imediatamente a escutar no `accept()`, permitindo que múltiplos clientes conectem em paralelo sem que um bloqueie o outro.

### Trade-off Observável
- **Vantagem (Simplicidade e Isolamento)**: A programação baseada em threads é altamente legível e sequencial de se codificar. Cada conexão é isolada em sua própria thread, impedindo que lentidões em um cliente (como latência de rede alta ou operações de I/O lentas) interfiram na velocidade de atendimento de outros clientes.
- **Desvantagem / Trade-off (Escalabilidade de Recursos)**: A criação de threads nativas do sistema operacional tem um custo computacional significativo de memória e CPU para alocação de pilhas (*stack space*) e troca de contexto (*context switching*). Em sistemas distribuídos com dezenas de milhares de conexões simultâneas (cenário C10K), o modelo de thread por conexão falha catastroficamente por esgotamento de memória. Abordagens mais robustas incluem um Pool de Threads limitando a concorrência física ou modelos orientados a eventos não-bloqueantes de E/S assíncrona (como `asyncio` em Python ou multiplexadores `select`/`poll`/`epoll`).
