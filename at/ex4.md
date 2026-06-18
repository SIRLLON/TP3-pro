# Exercicio 4 - Falha e Diagnostico com connect_ex()

Aqui a gente fez um script para testar a conexao de algumas portas do computador usando a funcao `connect_ex()`. Ela diz se a porta esta aberta ou nao sem quebrar o programa.

## Saida no VirtualBox

```
iniciando teste
porta: 22 code: 0 ms: 0.23
porta: 9999 code: 111 ms: 0.11
porta: 80 code: 111 ms: 0.23
```

## Justificativa Simples

A funcao `connect_ex()` devolve um codigo numerico em vez de jogar um erro na tela. Se ela devolver `0`, a porta esta aberta e funcionando. Se devolver outro numero (tipo o `111` que significa conexao recusada), a porta esta fechada. Isso eh bem melhor do que usar `try/except` porque o codigo fica mais limpo, roda mais rapido e a gente consegue saber exatamente qual foi o motivo da falha olhando o numero do codigo.
