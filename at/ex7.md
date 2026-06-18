# Exercicio 7 - Cliente TLS: Inspeçao de Certificado e Cifradores

Aqui a gente fez um cliente que se conecta de forma segura em um site publico (o Google) e le as informaçoes do certificado de segurança dele, salvando o certificado no formato PEM.

## Saida no VirtualBox

```
host: www.google.com
tls version: TLSv1.3
cipher: TLS_AES_256_GCM_SHA384
issuer cn: WR2
validade de: May 25 08:39:11 2026 GMT ate: Aug 17 08:39:10 2026 GMT
certificado salvo pem
```

## Justificativa Simples

A conexao com TLS garante que os dados sejam transmitidos de forma embaralhada (criptografada) de ponta a ponta. Isso significa que se alguem tentar bisbilhotar a rede, nao vai conseguir ler nada do que estamos conversando. O TLS eh fundamental em sistemas distribuidos porque garante que o servidor eh realmente quem ele diz ser (evita clones) e que ninguem alterou as mensagens no meio do caminho.
