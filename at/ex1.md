# Exercicio 1 - Inventario de Sockets

Aqui a gente cria quatro tipos de sockets para ver o que vem configurado neles por padrao. Nao conectamos em nada, so criamos e fechamos.

## Saida no VirtualBox

```
IPv4 TCP fam: 2 tipo: 1 timeout: None
IPv4 UDP fam: 2 tipo: 2 timeout: None
IPv6 TCP fam: 10 tipo: 1 timeout: None
IPv6 UDP fam: 10 tipo: 2 timeout: None
```

## Justificativa Simples

O TCP e o UDP sao diferentes porque o TCP precisa criar uma conexao certinha antes de mandar dados, garantindo que tudo chegue na ordem. O UDP so joga os dados na rede e nao avisa se deu certo. Isso muda como a gente escreve o codigo: no TCP usamos `accept` e `connect`, e no UDP usamos `recvfrom` e `sendto`. Isso vai afetar os proximos exercicios porque cada um usa uma logica diferente de envio.
