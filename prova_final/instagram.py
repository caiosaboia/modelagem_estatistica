import re
import pandas as pd

def converter_tempo(tempo):
    if isinstance(tempo, str):
        tempo = tempo.replace(' ', '').lower()
        if 'h' in tempo:
            partes = tempo.split('h')
            # Horas
            horas = int(re.findall(r'\d+', partes[0])[0]) if re.findall(r'\d+', partes[0]) else 0
            # Minutos
            minutos_str = partes[1] if len(partes) > 1 else ''
            minutos = int(re.findall(r'\d+', minutos_str)[0]) if re.findall(r'\d+', minutos_str) else 0
            return horas * 60 + minutos
        elif 'm' in tempo:
            return int(re.findall(r'\d+', tempo)[0]) if re.findall(r'\d+', tempo) else 0
        else:
            try:
                return float(tempo) * 60
            except:
                return 0  # Valor padrão para entradas inválidas
    else:
        return tempo

df = pd.read_csv("data/instagram.csv")

# Aplicar conversão de tempo (com tratamento de erros)
dias = ['Segunda', 'Terca', 'Quarta', 'Quinta', 'Sexta', 'Sabado', 'Domingo']
for dia in dias:
    df[dia] = df[dia].apply(converter_tempo)

# Tratar 'translado' (ignorar strings sem números)
df['translado'] = df['translado'].apply(
    lambda x: converter_tempo(x) if isinstance(x, str) and re.search(r'\d', x) else 0
)

df['genero'] = (
    df['genero']
    .str.strip()  # Remove espaços em branco extras
    .str.lower()
    .replace({
        'hétero': 'masculino',
        'm': 'masculino',
        'masculino': 'masculino',
        'feminino': 'feminino'
    })
    .str.capitalize()
)

# Restante do código...
df.to_csv("instagram_tratado.csv", index=False)
