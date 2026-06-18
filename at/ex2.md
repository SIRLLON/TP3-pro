# Exercicio 2 - Servidor Echo UDP e Cliente

Aqui a gente fez um servidor e um cliente usando UDP. O cliente envia mensagens de varios tamanhos para ver como o servidor responde de volta.

## Saida do Servidor no VirtualBox

```
servidor rodando
ip: 127.0.0.1 porta: 53995 size: 5
ip: 127.0.0.1 porta: 53995 size: 5
ip: 127.0.0.1 porta: 53995 size: 5
ip: 127.0.0.1 porta: 53995 size: 5
ip: 127.0.0.1 porta: 53995 size: 5
ip: 127.0.0.1 porta: 53995 size: 5
ip: 127.0.0.1 porta: 53995 size: 5
ip: 127.0.0.1 porta: 53995 size: 5
ip: 127.0.0.1 porta: 53995 size: 5
ip: 127.0.0.1 porta: 53995 size: 6
ip: 127.0.0.1 porta: 53995 size: 100
ip: 127.0.0.1 porta: 53995 size: 1000
ip: 127.0.0.1 porta: 53995 size: 5000
ip: 127.0.0.1 porta: 53995 size: 10000
ip: 127.0.0.1 porta: 53995 size: 50000
ip: 127.0.0.1 porta: 53995 size: 4
```

## Saida do Cliente no VirtualBox

```
recebido id: 1 payload: msg 1
recebido id: 2 payload: msg 2
recebido id: 3 payload: msg 3
recebido id: 4 payload: msg 4
recebido id: 5 payload: msg 5
recebido id: 6 payload: msg 6
recebido id: 7 payload: msg 7
recebido id: 8 payload: msg 8
recebido id: 9 payload: msg 9
recebido id: 10 payload: msg 10
enviei: 100 recebi: 100
enviei: 1000 recebi: 1000
enviei: 5000 recebi: 5000
enviei: 10000 recebi: 10000
enviei: 50000 recebi: 50000
```

## Justificativa Simples

Como o UDP nao garante entrega e nem a ordem das mensagens, se a rede estiver ruim algumas mensagens podem simplesmente sumir no caminho. A gente testou com tamanhos diferentes e tudo chegou porque rodamos no proprio computador (localhost). Em sistemas reais, isso eh muito util para coisas rapidas como jogos online ou ligacoes de voz, onde eh melhor perder um pedaço do que travar tudo esperando.
