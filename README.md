# Servidor Asterisk - Torra Torra Veículos

Configurações e scripts do servidor **Asterisk PBX 22.7.0** da Torra Torra Veículos.

## Visão Geral

Este repositório contém todas as configurações personalizadas, scripts AGI e arquivos de áudio customizados do servidor Asterisk que opera a central telefônica da empresa.

| Item | Descrição |
|---|---|
| **Versão** | Asterisk 22.7.0 |
| **Servidor** | Torratorra2025 (Ubuntu) |
| **Domínio** | torratorraveiculos.com.br |
| **Integração** | Evolution API (WhatsApp) + Sistema de Promissórias |

## Estrutura do Repositório

```
asterisk-torratorra/
├── etc/asterisk/              # Configurações principais
│   ├── extensions.conf        # Dialplan (URA, filas, ramais)
│   ├── pjsip.conf             # Troncos SIP e endpoints
│   ├── queues.conf            # Filas de atendimento
│   ├── manager.conf           # AMI (Asterisk Manager Interface)
│   ├── features.conf          # Features (transferência, gravação)
│   ├── musiconhold.conf       # Música de espera
│   └── ...                    # Demais configurações
├── lib/
│   ├── agi-bin/               # Scripts AGI
│   │   ├── enviar_whatsapp.py # Integração WhatsApp via Evolution API
│   │   └── tts_google.py      # Text-to-Speech Google
│   ├── moh/                   # Áudios de música de espera
│   ├── moh1/                  # Áudios de música de espera (alt)
│   ├── sounds/pt-br/          # Áudios customizados em português
│   ├── scripts/               # Scripts auxiliares
│   └── images/                # Imagens
├── spool/                     # Spool (outgoing calls, etc)
├── backups/                   # Backups de configurações anteriores
└── docs/                      # Documentação
```

## Integrações

### Evolution API (WhatsApp)
O script `enviar_whatsapp.py` é chamado via AGI durante as chamadas para enviar mensagens WhatsApp aos atendentes da fila. O Asterisk coleta **CPF** e **data de nascimento** do cliente via URA e envia esses dados automaticamente para o atendente responsável.

### Sistema de Promissórias
O servidor Asterisk se integra com o sistema de gestão de promissórias disponível em `promissorias.torratorraveiculos.com.br`, permitindo consulta de dados de clientes durante o atendimento.

### Google TTS
O script `tts_google.py` gera áudios dinâmicos usando a API do Google Text-to-Speech para reproduzir informações personalizadas durante as chamadas.

## Arquivos Principais

| Arquivo | Função |
|---|---|
| `extensions.conf` | Dialplan completo: URA, filas, horário de funcionamento, ramais |
| `pjsip.conf` | Configuração SIP: troncos, endpoints, transports |
| `queues.conf` | Filas de atendimento com estratégias e membros |
| `manager.conf` | AMI para integração com sistemas externos |
| `features.conf` | Transferência, captura, gravação de chamadas |
| `musiconhold.conf` | Configuração de música de espera |
| `enviar_whatsapp.py` | Script AGI - envia dados da URA via WhatsApp |
| `tts_google.py` | Script AGI - gera áudio TTS durante chamada |

## Backup e Restauração

### Criar backup completo
```bash
tar czf /opt/backups/asterisk_$(date +%Y%m%d_%H%M%S).tar.gz \
  /etc/asterisk/ /var/lib/asterisk/agi-bin/ \
  /var/lib/asterisk/moh/ /var/lib/asterisk/moh1/ \
  /var/lib/asterisk/sounds/ /var/lib/asterisk/scripts/
```

### Restaurar configurações
```bash
# Parar Asterisk
systemctl stop asterisk

# Restaurar arquivos
tar xzf /opt/backups/asterisk_XXXXXXXX_XXXXXX.tar.gz -C /

# Verificar permissões
chown -R asterisk:asterisk /etc/asterisk/ /var/lib/asterisk/

# Reiniciar Asterisk
systemctl start asterisk
```

### Recarregar sem reiniciar
```bash
asterisk -rx "dialplan reload"
asterisk -rx "pjsip reload"
asterisk -rx "queue reload all"
asterisk -rx "manager reload"
```

## Comandos Úteis

```bash
# Ver status
asterisk -rx "core show version"
asterisk -rx "pjsip show endpoints"
asterisk -rx "queue show"
asterisk -rx "core show channels"

# Logs em tempo real
asterisk -rvvvv

# Testar dialplan
asterisk -rx "dialplan show default"
```

## Autor

**Luciano** - Torra Torra Veículos

---
*Repositório privado - Uso interno*
