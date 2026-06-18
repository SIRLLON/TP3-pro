# Exercicio 9 - IPv6 no Socket e Fallback Controlado

Aqui a gente fez um servidor e um cliente se comunicarem usando IPv6 no loopback (`::1`). Configuramos tambem uma segurança de "fallback" (voltar atras) para usar IPv4 caso o IPv6 falhasse.

## Saida do Servidor no VirtualBox

```
ipv6 rodando
recv: sair
```

## Saida do Cliente no VirtualBox

```
ipv6 ok
res: ok
```

## Justificativa Simples

No nosso teste na VM Linux, a conexao IPv6 funcionou direto de primeira, o que mostra que o sistema operacional ja da suporte total ao IPv6. Mas em computadores antigos ou redes mal configuradas o IPv6 pode nao funcionar. Ter um sistema de fallback eh importante porque garante que o programa nao vai dar erro e fechar sozinho se o IPv6 falhar: ele simplesmente tenta se conectar por IPv4 e continua funcionando normal.
