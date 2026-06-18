# Exercicio 3 - Servidor TCP Concorrente e Múltiplos Clientes

Aqui a gente fez um servidor TCP que consegue atender varios clientes de uma vez usando Threads. Criamos 5 clientes para testar tudo junto.

## Saida do Servidor no VirtualBox

```
servidor ouvindo
con: 127.0.0.1 33266 msg: cliente_1
con: 127.0.0.1 33274 msg: cliente_2
con: 127.0.0.1 56880 msg: cliente_3
con: 127.0.0.1 56896 msg: cliente_4
con: 127.0.0.1 56902 msg: cliente_5
```

## Saida dos Clientes no VirtualBox

```
cli: cliente_1 res: OK
cli: cliente_2 res: OK
cli: cliente_3 res: OK
cli: cliente_4 res: OK
cli: cliente_5 res: OK
```

## Justificativa Simples

A gente usou threads para que o servidor atenda cada cliente em uma "via" separada. Desse jeito, se um cliente demorar ou travar, os outros continuam funcionando normalmente. O lado ruim (trade-off) eh que criar muitas threads gasta muita memoria e processamento da maquina. Se entrar muita gente ao mesmo tempo, o servidor pode ficar lento ou cair por falta de recursos.
