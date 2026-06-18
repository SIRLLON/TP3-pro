# Exercicio 8 - Servidor TLS Minimo

Aqui a gente gerou um certificado de testes autoassinado e criou um servidor e um cliente TLS locais para conversar de forma criptografada.

## Comando de Geraçao do Certificado (Via Python Subprocess)

```bash
openssl req -newkey rsa:2048 -nodes -keyout server.key -x509 -days 365 -out server.crt -subj "/CN=localhost"
```

## Arquivos Criados
- `server.key`: Chave privada do servidor.
- `server.crt`: Certificado de segurança do servidor.

## Saida do Servidor no VirtualBox

```
servidor tls rodando
recv: sair
```

## Saida do Cliente no VirtualBox

```
res: ok
```

## Justificativa Simples

Os certificados autoassinados sao otimos para a gente programar e testar no computador local, mas sao perigosos em ambientes reais (produçao) porque qualquer um pode criar um. O navegador nao confia neles e mostra aquele aviso vermelho de "site nao seguro". Em servidores de verdade na internet, a gente deve usar um certificado emitido por uma autoridade oficial confiada por todos (tipo o Let's Encrypt, que eh de graça e seguro).
