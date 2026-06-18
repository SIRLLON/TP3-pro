# Servidor HTTP/1.1 Mínimo com Socket Puro

Demonstração prática da implementação do protocolo HTTP/1.1 diretamente sobre sockets TCP puros, sem o auxílio de frameworks web, tratando as requisições como fluxos de bytes e validando via curl em ambiente Linux.

## 1. Execução e Validação do Servidor HTTP no Linux

O servidor [ex5_server.py](file:///c:/Users/sirll/OneDrive/Área de Trabalho/Estrutura/TP3/ex5_server.py) foi iniciado em segundo plano na VM Linux. Em seguida, foram efetuadas requisições utilizando a ferramenta `curl` para validar os endpoints `/` e `/health`.

### Teste do Endpoint Inicial (`/`)
Comando executado:
```bash
curl -i http://127.0.0.1:8080/
```

Resposta do servidor:
```text
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 201
Connection: close

<!DOCTYPE html>
<html>
<head><meta charset='utf-8'><title>Servidor HTTP Puro</title></head>
<body>
<h1>Servidor HTTP/1.1 Mínimo Puro</h1>
<p>Página inicial respondida com sucesso!</p>
</body>
</html>
```

### Teste do Endpoint de Saúde (`/health`)
Comando executado:
```bash
curl -i http://127.0.0.1:8080/health
```

Resposta do servidor:
```text
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 54
Connection: close

{"status": "healthy", "service": "http-socket-server"}
```

### Logs do Servidor (Linux VM)
```text
Servidor HTTP puro rodando em http://127.0.0.1:8080
[REQUISIÇÃO] GET / de 127.0.0.1:60750
[REQUISIÇÃO] GET /health de 127.0.0.1:50648
[REQUISIÇÃO] GET /shutdown de 127.0.0.1:50664
Comando de desligamento recebido no endpoint /shutdown. Encerrando...
Servidor HTTP finalizado.
```

---

## 2. Justificativa Técnica

### O uso de Content-Length
No protocolo HTTP/1.1, a conexão TCP pode ser mantida aberta para múltiplas requisições (*Keep-Alive*). Para que o cliente saiba exatamente onde termina uma resposta e onde começa a próxima sem precisar fechar a conexão, é obrigatório indicar o tamanho em bytes do corpo da mensagem através do cabeçalho `Content-Length`.
Se o `Content-Length` for omitido ou calculado incorretamente:
- **Tamanho menor**: O cliente lerá apenas a quantidade parcial de bytes indicada, truncando o corpo da resposta (ex: cortando tags HTML ou quebrando o JSON).
- **Tamanho maior**: O cliente ficará travado esperando que mais bytes cheguem pela conexão TCP até estourar um timeout, degradando severamente a performance.
- *Nota técnica*: O tamanho deve ser computado em **bytes** da string codificada (ex: `len(body.encode('utf-8'))`), e não pelo número de caracteres da string, pois caracteres especiais ou acentuados ocupam mais de 1 byte no padrão UTF-8.

### O encerramento correto da conexão após a resposta
Como especificamos `Connection: close` nos cabeçalhos da nossa resposta, estamos sinalizando ao cliente que não daremos suporte a conexões persistentes (*pipelining* ou *keep-alive*).
Após enviar todos os bytes da resposta (cabeçalho + corpo), o servidor executa imediatamente `client_sock.close()`. Este encerramento é essencial porque:
1. Libera imediatamente os recursos de descritores de arquivo e buffers de socket no sistema operacional do servidor, evitando vazamento de recursos (*resource leaks*).
2. Notifica a pilha TCP do cliente (via pacote FIN) que a transmissão de dados foi concluída com sucesso, permitindo ao cliente encerrar seu estado de leitura sem bloqueios desnecessários.
