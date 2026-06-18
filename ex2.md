# UDP: Servidor Echo e Cliente (Datagramas)

Demonstração prática de troca de datagramas utilizando sockets UDP, exibindo limites operacionais de payload e detalhes de transporte sem conexão sob o Linux.

## 1. Execução do Servidor e Cliente UDP no Linux

O servidor [ex2_server.py](file:///c:/Users/sirll/OneDrive/Área de Trabalho/Estrutura/TP3/ex2_server.py) foi iniciado em segundo plano no Linux e o cliente [ex2_client.py](file:///c:/Users/sirll/OneDrive/Área de Trabalho/Estrutura/TP3/ex2_client.py) foi executado em seguida para enviar as 10 mensagens.

### Logs do Servidor UDP (Linux VM)
```text
Servidor UDP escutando em 127.0.0.1:9999
[RECEBIDO] Origem: 127.0.0.1:54666 | Tamanho: 27 bytes
[RECEBIDO] Origem: 127.0.0.1:54666 | Tamanho: 50 bytes
[RECEBIDO] Origem: 127.0.0.1:54666 | Tamanho: 1024 bytes
[RECEBIDO] Origem: 127.0.0.1:54666 | Tamanho: 8192 bytes
[RECEBIDO] Origem: 127.0.0.1:54666 | Tamanho: 32768 bytes
[RECEBIDO] Origem: 127.0.0.1:54666 | Tamanho: 60000 bytes
[RECEBIDO] Origem: 127.0.0.1:54666 | Tamanho: 65507 bytes
[RECEBIDO] Origem: 127.0.0.1:54666 | Tamanho: 31 bytes
[RECEBIDO] Origem: 127.0.0.1:54666 | Tamanho: 41 bytes
Comando SHUTDOWN recebido. Desligando servidor...
Servidor UDP finalizado.
```

### Logs do Cliente UDP (Linux VM)
```text
=== CLIENTE UDP INICIANDO TRANSMISSÃO ===

[ENVIO] ID 1: Enviando 27 bytes...
[RETORNO] ID 1 recebido com sucesso de 127.0.0.1:9999

[ENVIO] ID 2: Enviando 50 bytes...
[RETORNO] ID 2 recebido com sucesso de 127.0.0.1:9999

[ENVIO] ID 3: Enviando 1024 bytes...
[RETORNO] ID 3 recebido com sucesso de 127.0.0.1:9999

[ENVIO] ID 4: Enviando 8192 bytes...
[RETORNO] ID 4 recebido com sucesso de 127.0.0.1:9999

[ENVIO] ID 5: Enviando 32768 bytes...
[RETORNO] ID 5 recebido com sucesso de 127.0.0.1:9999

[ENVIO] ID 6: Enviando 60000 bytes...
[RETORNO] ID 6 recebido com sucesso de 127.0.0.1:9999

[ENVIO] ID 7: Enviando 65507 bytes...
[RETORNO] ID 7 recebido com sucesso de 127.0.0.1:9999

[ENVIO] ID 8: Enviando 70000 bytes...
[ERRO NO ENVIO] ID 8 falhou ao enviar: [Errno 90] Message too long

[ENVIO] ID 9: Enviando 31 bytes...
[RETORNO] ID 9 recebido com sucesso de 127.0.0.1:9999

[ENVIO] ID 10: Enviando 41 bytes...
[RETORNO] ID 10 recebido com sucesso de 127.0.0.1:9999

=== RELATÓRIO DE ENTREGAS UDP ===
IDs enviados com sucesso no transporte: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
IDs ecoados e recebidos: [1, 2, 3, 4, 5, 6, 7, 9, 10]
IDs perdidos (excluindo erro de buffer excedido): []
```

---

## 2. Justificativa Técnica

### Confiabilidade e Ordem no UDP
1. **Confiabilidade**: O UDP não possui mecanismos nativos para garantir a entrega de pacotes. Se um roteador intermediário descartar um pacote por congestionamento, o destinatário nunca o receberá, e o remetente não será notificado.
2. **Ordem**: Não há numeração de sequência nativa para reorganização de pacotes. Se um pacote $B$ pegar uma rota de rede mais rápida que o pacote $A$ (enviado antes), o pacote $B$ será entregue antes na pilha de aplicação, causando reordenação.
3. **Limitação de Tamanho**: O teste de envio do ID 8 com 70.000 bytes falhou imediatamente no sistema operacional Linux com o erro `[Errno 90] Message too long`. Isso ocorre porque o limite máximo de um pacote IPv4 UDP é de 65.507 bytes (65.535 bytes de payload total do IP - 20 bytes do cabeçalho IP - 8 bytes do cabeçalho UDP). Qualquer payload maior do que isso é sumariamente rejeitado pelo kernel do Linux.

### Relevância em Sistemas Distribuídos Reais
A escolha do UDP é crucial em sistemas de tempo real sensíveis à latência, como streaming de vídeo/áudio, jogos online multijogador e consultas DNS rápidas. Nesses contextos, retransmitir um pacote perdido é inútil porque a informação já estaria desatualizada (por exemplo, a posição de um jogador no mapa 1 segundo atrás). A ausência de overhead de handshake e controle de fluxo torna o UDP muito mais rápido e leve. A confiabilidade e a integridade de dados necessárias são transferidas para protocolos de camada de aplicação específicos (como RTP, SRTP ou QUIC) se e quando exigido.
