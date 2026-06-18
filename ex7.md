# Cliente TLS: Inspeção de Certificado e Cifradores

Demonstração prática de um cliente TLS seguro que se conecta a um host público via HTTPS, realiza o handshake criptográfico, inspeciona os parâmetros da sessão de segurança e extrai o certificado digital do servidor em formato PEM sob ambiente Linux.

## 1. Execução do Cliente TLS no Linux

O script [ex7.py](file:///c:/Users/sirll/OneDrive/Área de Trabalho/Estrutura/TP3/ex7.py) foi copiado e executado dentro da VM Linux para estabelecer uma sessão segura com o domínio `www.google.com` na porta 443 (HTTPS).

Comando executado:
```bash
python3 ex7.py
```

### Logs de Saída (Evidência Objetiva no Linux)
```text
=== CLIENTE TLS: CONECTANDO A HTTPS://www.google.com:443 ===

[Handshake TLS Completado com Sucesso]
  Versão TLS: TLSv1.3
  Cipher Negociado: TLS_AES_256_GCM_SHA384 (TLSv1.3 - 256 bits)

[Detalhes do Certificado do Servidor]
  Emissor (Issuer):
    countryName: US
    organizationName: Google Trust Services
    commonName: WR2
  Período de Validade:
    Válido a partir de (Not Before): May 25 08:39:11 2026 GMT
    Válido até (Not After): Aug 17 08:39:10 2026 GMT

Certificado PEM obtido e salvo em 'google_cert.pem' com sucesso.

Trecho inicial do Certificado PEM (Evidência):
  -----BEGIN CERTIFICATE-----
  MIIEVzCCAz+gAwIBAgIRAKvnS02GY4K9ErwdxOq7VKEwDQYJKoZIhvcNAQELBQAw
  OzELMAkGA1UEBhMCVVMxHjAcBgNVBAoTFUdvb2dsZSBUcnVzdCBTZXJ2aWNlczEM
  MAoGA1UEAxMDV1IyMB4XDTI2MDUyNTA4MzkxMVoXDTI2MDgxNzA4MzkxMFowGTEX
  MBUGA1UEAxMOd3d3Lmdvb2dsZS5jb20wWTATBgcqhkjOPQIBBggqhkjOPQMBBwNC
  ...
  Bevo6z9dSLvpX9M=
  -----END CERTIFICATE-----
```

---

## 2. Justificativa Técnica

### O que as evidências comprovam sobre comunicação segura?
As informações capturadas comprovam os três pilares fundamentais da segurança da informação (CIA) aplicados ao canal de comunicação:
1. **Confidencialidade (Criptografia Simétrica)**: O cipher negociado `TLS_AES_256_GCM_SHA384` sob `TLSv1.3` garante que todos os dados transmitidos serão encriptados com AES de 256 bits, tornando impossível a interceptação legível por terceiros na rede (*eavesdropping*).
2. **Integridade (Hashing)**: O algoritmo de autenticação de mensagem `GCM` com hash `SHA384` assegura que nenhum bit do payload possa ser alterado em trânsito sem ser imediatamente detectado pelo destinatário.
3. **Autenticidade e Confiança (Criptografia Assimétrica)**: A estrutura do certificado comprova a identidade do servidor. O emissor (`Google Trust Services`) é uma Autoridade Certificadora (CA) cujas chaves públicas raiz estão embutidas e pré-aprovadas na pilha de confiança local do sistema operacional. O certificado digital assinado pela CA atesta que a chave pública de criptografia pertence legitimamente ao domínio `www.google.com`, mitigando ataques de personificação (*Man-in-the-Middle*).

### Por que TLS é indispensável em ambientes distribuídos?
Em sistemas distribuídos modernos, os dados trafegam por infraestruturas de rede públicas ou não confiáveis (como a internet ou datacenters compartilhados). Sem o TLS:
- Dados altamente confidenciais (credenciais de acesso, dados bancários, APIs de microsserviços) seriam expostos em texto claro.
- Um atacante poderia interceptar a requisição e injetar dados maliciosos no fluxo (ataques de replay ou injeção de payload).
- Não haveria garantia de que o microsserviço cliente está se comunicando com o microsserviço servidor correto, facilitando o roubo de dados.
Portanto, o TLS é a camada de segurança que viabiliza transações financeiras, APIs seguras (gRPC, REST) e a própria computação em nuvem em escala global.
