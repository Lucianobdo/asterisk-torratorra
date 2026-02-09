#!/usr/bin/env python3
import sys
import requests
import json

# Configurações da Evolution API
EVO_URL = "https://pbx3.torratorraveiculos.com.br/message/sendText/torra_torra"
EVO_KEY = "944E37257396-45F7-BCAE-30CFA1F1E556"

def enviar_whatsapp( ):
    # Verifica se recebeu os 5 argumentos: CPF, NASC, CNH, CLIENTE, VENDEDOR
    if len(sys.argv) < 6:
        return

    cpf = sys.argv[1]
    nascimento = sys.argv[2]
    cnh = "Sim" if sys.argv[3] == "1" else "Não"
    cliente_fone = sys.argv[4]
    vendedor_fone = sys.argv[5]

    # Garante o DDI 55 no número do vendedor
    if not vendedor_fone.startswith('55'):
        vendedor_fone = '55' + vendedor_fone

    mensagem = (
        f"🚗 *NOVO LEAD - TORRA TORRA*\n\n"
        f"👤 *Cliente:* {cliente_fone}\n"
        f"📄 *CPF:* {cpf}\n"
        f"📅 *Nascimento:* {nascimento}\n"
        f"🪪 *Possui CNH:* {cnh}\n\n"
        f"⚡ _Espero que vc consiga aprovar essa simulação:)!_"
    )

    payload = {
        "number": vendedor_fone,
        "text": mensagem,
        "delay": 1000,
        "linkPreview": False
    }

    headers = {
        "Content-Type": "application/json",
        "apikey": EVO_KEY
    }

    try:
        requests.post(EVO_URL, json=payload, headers=headers)
    except:
        pass

if __name__ == "__main__":
    enviar_whatsapp()

