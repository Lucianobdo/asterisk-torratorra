#!/usr/bin/env python3
import sys
import os
import hashlib
from urllib.parse import quote

# 1. Validações Básicas
if len(sys.argv) < 2:
    sys.exit(1)

texto = sys.argv[1].replace('"', '').replace("'", "").strip()
hash_name = hashlib.md5(texto.encode()).hexdigest()

# 2. Caminhos (Vamos usar WAV padrão, o Playback do Asterisk adora WAV)
file_mp3 = f"/tmp/{hash_name}.mp3"
# O Asterisk prefere o caminho sem extensão na variavel
file_base = f"/tmp/{hash_name}" 
file_wav = f"{file_base}.wav"

CMD_WGET = "/usr/bin/wget --no-check-certificate -q -U 'Mozilla/5.0'"
CMD_FFMPEG = "/usr/bin/ffmpeg"

# 3. Baixa e Converte (se nao existir)
if not os.path.exists(file_wav):
    url = f"http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q={quote(texto)}&tl=pt-BR"
    
    os.system(f"{CMD_WGET} -O {file_mp3} '{url}'")
    
    if os.path.exists(file_mp3) and os.path.getsize(file_mp3) > 100:
        # Converte para WAV padrão (8khz, 16bit, Mono)
        os.system(f"{CMD_FFMPEG} -y -i {file_mp3} -ar 8000 -ac 1 {file_wav} > /dev/null 2>&1")
        os.remove(file_mp3)

# 4. O GRANDE SEGREDO: Devolve o caminho para o Asterisk tocar
# Em vez de tocar, definimos uma variável para o Dialplan usar
if os.path.exists(file_wav):
    print(f"SET VARIABLE TTS_PLAY \"{file_base}\"")
else:
    # Se falhou, define variavel vazia (Asterisk ignora)
    print(f"SET VARIABLE TTS_PLAY \"\"")

sys.stdout.flush()
sys.stdin.readline()
