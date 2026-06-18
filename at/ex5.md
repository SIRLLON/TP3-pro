# Exercicio 5 - Servidor HTTP/1.1 Minimo com Socket Puro

Aqui a gente criou um servidor web bem simples do zero usando sockets puros, que responde requisiçoes HTTP comuns e mostra respostas diferentes dependendo do caminho digitado.

## Saida do Servidor no VirtualBox

```
http rodando
req: / status: 200 OK
req: /health status: 200 OK
req: /outra status: 404 Not Found
```

## Resposta para a rota / (Curl)

```
HTTP/1.1 200 OK
Content-Type: text/plain
Content-Length: 4
Connection: close

home
```

## Resposta para a rota /health (Curl)

```
HTTP/1.1 200 OK
Content-Type: text/plain
Content-Length: 2
Connection: close

ok
```

## Resposta para rotas invalidas (Curl)

```
HTTP/1.1 404 Not Found
Content-Type: text/plain
Content-Length: 4
Connection: close

erro
```

## Justificativa Simples

O header `Content-Length` serve para avisar ao navegador ou ao `curl` qual o tamanho exato da resposta em bytes. Se nao colocar isso, quem fez a requisiçao nao sabe quando o texto terminou e o programa fica esperando ate travar por timeout. Fechar a conexao certinha com `Connection: close` garante que a porta do servidor seja liberada logo apos o envio, evitando que o servidor fique cheio de conexoes abertas sem uso.
