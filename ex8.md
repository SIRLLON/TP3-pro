# Servidor TLS Mínimo

Demonstração prática de um servidor TLS local que realiza cifragem de canal ponta a ponta utilizando um certificado autoassinado (self-signed) gerado programaticamente e validado de forma estrita por um cliente Python confiável sob o Linux.

## 1. Geração do Certificado Autoassinado no Linux

Para fins de desenvolvimento e testes locais, foi criado e executado o script Python [generate_cert.py](file:///c:/Users/sirll/OneDrive/Área de Trabalho/Estrutura/TP3/generate_cert.py) utilizando a biblioteca `cryptography` dentro do Linux.

### Comando executado
```bash
python3 generate_cert.py
```

### Saída obtida e arquivos criados
```text
Gerando chave privada RSA de 2048 bits...
Configurando metadados do certificado...
Salvando chave privada em 'server.key'...
Salvando certificado em 'server.crt'...
Certificado e chave privada gerados com sucesso!
```

---

## 2. Execução do Servidor e Cliente TLS Locais no Linux

O servidor [ex8_server.py](file:///c:/Users/sirll/OneDrive/Área de Trabalho/Estrutura/TP3/ex8_server.py) foi iniciado em segundo plano na porta segura 8443 e o cliente [ex8_client.py](file:///c:/Users/sirll/OneDrive/Área de Trabalho/Estrutura/TP3/ex8_client.py) foi executado em seguida na VM Linux.

### Logs do Servidor TLS (Linux VM)
```text
Certificado TLS carregado com sucesso.
Servidor TLS escutando em segura https://127.0.0.1:8443

[CONEXÃO TLS ESTABELECIDA] Origem: 127.0.0.1:39690
  Mensagem descriptografada recebida: 'Conexao segura via socket TLS puro!'

[CONEXÃO TLS ESTABELECIDA] Origem: 127.0.0.1:39702
  Mensagem descriptografada recebida: 'SHUTDOWN'
Comando SHUTDOWN recebido. Encerrando servidor TLS...
Servidor TLS finalizado.
```

### Logs do Cliente TLS (Linux VM)
```text
=== CLIENTE TLS SEGURO INICIANDO ===

[CLIENTE] Conectado via TLSv1.3 usando TLS_AES_256_GCM_SHA384
[CLIENTE] Enviando: 'Conexao segura via socket TLS puro!'
[CLIENTE] Recebido do Servidor: 'Confirmado TLS: Recebido 'Conexao segura via socket TLS puro!''

--- Enviando comando de finalização para o servidor ---

[CLIENTE] Conectado via TLSv1.3 usando TLS_AES_256_GCM_SHA384
[CLIENTE] Enviando: 'SHUTDOWN'
[CLIENTE] Recebido do Servidor: 'Confirmado TLS: Recebido 'SHUTDOWN''
```

---

## 3. Justificativa Técnica

### Limitações e Riscos de Certificados Autoassinados (Self-Signed)
Embora os certificados autoassinados sejam extremamente úteis para testes em ambientes de desenvolvimento (pois garantem que o canal trafegue criptografado), eles possuem graves limitações de segurança se expostos em ambientes externos:
1. **Ausência de Cadeia de Confiança**: O certificado é assinado por sua própria chave privada, e não por uma Autoridade Certificadora (CA) pública confiável (como DigiCert ou Let's Encrypt). Navegadores web e clientes HTTPS padrão lançarão avisos de erro de segurança críticos e bloquearão a conexão por padrão.
2. **Ataque Man-in-the-Middle (MITM)**: Para fazer os sistemas funcionarem com certificados autoassinados, desenvolvedores frequentemente configuram seus clientes para desabilitar a verificação de certificados (ex: `ssl.CERT_NONE` em Python ou `--insecure` no curl). Ao desativar a validação, qualquer atacante pode interceptar a conexão, apresentar outro certificado falso (também autoassinado) e ler/modificar todo o tráfego sem disparar alertas, anulando a segurança do TLS.
3. **Gerenciamento e Revogação Inexistentes**: Certificados autoassinados não possuem suporte a verificação de revogação (via CRL ou OCSP), tornando impossível invalidar uma chave comprometida de forma automática.

### Alternativa Adequada para Ambientes de Produção
Para ambientes de produção, deve-se adotar certificados emitidos e assinados digitalmente por uma **Autoridade Certificadora (CA) confiável e auditada publicamente**.
- **Let's Encrypt**: É a alternativa padrão da indústria moderna de TI para emissão automatizada e gratuita de certificados TLS confiáveis utilizando o protocolo ACME.
- **Autoridades Comerciais (CAs corporativas)**: Para necessidades corporativas específicas ou certificados Wildcard/EV (Extended Validation).
- **PKI Privada Interna (Private CA)**: Em redes internas corporativas complexas ou clusters de microsserviços do Kubernetes, pode-se estabelecer uma CA raiz interna confiável controlada pela empresa. Os certificados emitidos por ela são injetados nas máquinas clientes como confiáveis, permitindo criptografia e identificação segura entre máquinas internas sem expor chaves na internet pública.
