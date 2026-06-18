# Exercicio 6 - Servidor HTTP Concorrente

Aqui a gente melhorou o servidor HTTP do exercicio anterior para que ele consiga responder varias requisiçoes de uma vez so, usando Threads.

## Saida do Servidor no VirtualBox

```
http concorrente rodando
concorrente req: /health status: 200 OK
concorrente req: /health status: 200 OK
concorrente req: /health status: 200 OK
```

## Resposta obtida (Curl)

```
HTTP/1.1 200 OK
Content-Type: text/plain
Content-Length: 2
Connection: close

ok
```

## Justificativa Simples

A gente usou threads para nao deixar o servidor bloqueado. Sem isso, se um cliente fizesse uma requisiçao demorada, nenhum outro cliente conseguiria acessar o site nesse tempo. A limitaçao dessa soluçao eh que se tivermos acessos em massa, criar uma thread para cada pessoa vai esgotar a memoria do servidor rapidinho e ele vai travar. Servidores de verdade usam um limite maximo de threads para evitar isso.
