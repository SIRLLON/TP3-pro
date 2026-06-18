# IPv6 no Socket e Fallback Controlado

Demonstração prática de conectividade TCP em pilhas dual-stack, comprovando estabelecimento de sessão via IPv6 local (`::1`) e resiliência com mecanismo de fallback automatizado para IPv4 (`127.0.0.1`) caso o IPv6 falhe sob o Linux VM.

## 1. Caso de Sucesso: Conexão Nativa em IPv6 no Linux

O servidor [ex9_server.py](file:///c:/Users/sirll/OneDrive/Área de Trabalho/Estrutura/TP3/ex9_server.py) foi iniciado em modo padrão (escutando em IPv6 `::1`). Em seguida, o cliente [ex9_client.py](file:///c:/Users/sirll/OneDrive/Área de Trabalho/Estrutura/TP3/ex9_client.py) foi executado na VM Linux.

### Logs do Servidor (IPv6 Nativo - Linux VM)
```text
Servidor TCP iniciado com sucesso em IPv6: [::1]:9996

[CONEXÃO RECEBIDA (IPv6)] Origem: ('::1', 58766, 0, 0)
  Mensagem: 'Ola, testando conexao dual-stack!'

[CONEXÃO RECEBIDA (IPv6)] Origem: ('::1', 58770, 0, 0)
  Mensagem: 'SHUTDOWN'
Comando SHUTDOWN recebido. Desligando servidor...
Servidor finalizado.
```

### Logs do Cliente (IPv6 Nativo - Linux VM)
```text
=== CLIENTE TCP COM FALLBACK DE PILHA (IPv6 -> IPv4) ===

[CLIENTE] Tentando conectar via IPv6 a [::1]:9996...
  [SUCESSO] Conectado via IPv6!
  [RESPOSTA RECEBIDA] 'Confirmado IPv6: Recebido 'Ola, testando conexao dual-stack!''
  Conexão fechada.

--- Enviando sinal de finalização para o servidor ---

[CLIENTE] Tentando conectar via IPv6 a [::1]:9996...
  [SUCESSO] Conectado via IPv6!
  [RESPOSTA RECEBIDA] 'Confirmado IPv6: Recebido 'SHUTDOWN''
  Conexão fechada.
```

---

## 2. Caso de Fallback: Servidor Somente IPv4 no Linux

Para simular um ambiente onde o IPv6 não está disponível ou o serviço só ouve em IPv4, o servidor foi iniciado forçando o binding apenas em IPv4 (`python3 ex9_server.py ipv4_only`). O cliente executou a mesma lógica padrão de tentativa IPv6 seguida de fallback.

### Logs do Servidor (Fallback IPv4 - Linux VM)
```text
Servidor TCP iniciado (modo Fallback IPv4): 127.0.0.1:9996

[CONEXÃO RECEBIDA (IPv4)] Origem: ('127.0.0.1', 40058)
  Mensagem: 'Ola, testando conexao dual-stack!'

[CONEXÃO RECEBIDA (IPv4)] Origem: ('127.0.0.1', 40070)
  Mensagem: 'SHUTDOWN'
Comando SHUTDOWN recebido. Desligando servidor...
Servidor finalizado.
```

### Logs do Cliente (Fallback IPv4 Ativado - Linux VM)
```text
=== CLIENTE TCP COM FALLBACK DE PILHA (IPv6 -> IPv4) ===

[CLIENTE] Tentando conectar via IPv6 a [::1]:9996...
  [FALHA] Erro de conexão IPv6: [Errno 111] Connection refused
  [FALLBACK] Iniciando fallback automatizado para IPv4 em 127.0.0.1:9996...
  [SUCESSO] Conectado via IPv4 (Fallback)!
  [RESPOSTA RECEBIDA] 'Confirmado IPv4: Recebido 'Ola, testando conexao dual-stack!''
  Conexão fechada.

--- Enviando sinal de finalização para o servidor ---

[CLIENTE] Tentando conectar via IPv6 a [::1]:9996...
  [FALHA] Erro de conexão IPv6: [Errno 111] Connection refused
  [FALLBACK] Iniciando fallback automatizado para IPv4 em 127.0.0.1:9996...
  [SUCESSO] Conectado via IPv4 (Fallback)!
  [RESPOSTA RECEBIDA] 'Confirmado IPv4: Recebido 'SHUTDOWN''
  Conexão fechada.
```

---

## 3. Justificativa Técnica

### Estado real do suporte IPv6 no ambiente
No ambiente da VM Linux (Ubuntu), a pilha de rede suporta dual-stack nativa de forma padrão. A interface de loopback mapeia o host `localhost` tanto para `127.0.0.1` (IPv4) quanto para `::1` (IPv6). No entanto, em ambientes reais de produção (datacenters legados, redes corporativas com firewalls restritivos ou certos provedores de nuvem), o suporte a IPv6 pode ser parcial, inoperante ou totalmente desabilitado.

### O que o fallback demonstra sobre a robustez da aplicação?
O fallback programático implementado no cliente (tentar conectar via `AF_INET6` e, se falhar por timeout ou rejeição, instanciar um novo socket `AF_INET`) demonstra o princípio de **resiliência e design defensivo** em sistemas distribuídos:
1. **Evita indisponibilidade (Downtime)**: Garante que a aplicação continuará operando mesmo que a infraestrutura subjacente de rede mude ou apresente falhas pontuais de roteamento de pacotes IPv6.
2. **Autonomia Operacional**: A aplicação se adapta dinamicamente às capacidades da rede sem exigir intervenção humana (alteração de configurações manuais) ou reinicializações do serviço.
3. **Compatibilidade Ampla**: Habilita a aplicação a ser implantada de forma transparente em servidores puramente IPv4, puramente IPv6 ou redes dual-stack híbridas, preservando o contrato básico de comunicação.
