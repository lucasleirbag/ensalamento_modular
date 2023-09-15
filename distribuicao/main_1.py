import pandas as pd

# Ler os arquivos
df_regras = pd.read_excel("data/regras.xlsx")
df_candidatos = pd.read_excel("data_dist/candidatos.xlsx")
df_mapa_de_sala = pd.read_excel("data_dist/mapa_de_sala.xlsx")

# Ordenar as regras de forma crescente, considerando as regras mais restritivas primeiro
df_regras = df_regras.sort_values(by=['Facil_acesso', 'Regra'], ascending=[False, True])

# Iniciar o ensalamento
ensalamento = []
salas_usadas = set()

# Filtrar salas de fácil acesso (térreo ou 1º andar)
salas_facil_acesso = df_mapa_de_sala[df_mapa_de_sala['Andar'].isin(['Térreo', '1º Andar'])]

for _, regra in df_regras.iterrows():
    perfil = regra['Perfil']
    max_per_sala = regra['Regra']
    facil_acesso = regra['Facil_acesso']
    
    candidatos_perfil = df_candidatos[df_candidatos['Candidato'] == perfil]
    
    for _, candidato in candidatos_perfil.iterrows():
        # Verificar se o candidato precisa de sala de fácil acesso
        if facil_acesso == 'FA':
            salas = salas_facil_acesso
        else:
            salas = df_mapa_de_sala
        
        # Alocar o candidato em uma sala
        alocado = False
        for _, sala in salas.iterrows():
            if sala['Sala'] not in salas_usadas:
                # Se a sala não foi usada, inicia o uso
                salas_usadas.add(sala['Sala'])
                ensalamento.append({
                    'Sala': sala['Sala'],
                    'Perfil': perfil,
                    'Quantidade': 1,
                    'Capacidade': sala['Capacidade']
                })
                alocado = True
                break
            else:
                # Se a sala já foi usada, verificar se ainda há espaço para o candidato
                sala_usada = next((e for e in ensalamento if e['Sala'] == sala['Sala'] and e['Perfil'] == perfil), None)
                if sala_usada and (sala_usada['Quantidade'] < min(max_per_sala, sala['Capacidade'])):
                    sala_usada['Quantidade'] += 1
                    alocado = True
                    break
        
        # Se o candidato não foi alocado, adiciona uma nova sala
        if not alocado:
            next_sala = salas.iloc[0]
            salas_usadas.add(next_sala['Sala'])
            ensalamento.append({
                'Sala': next_sala['Sala'],
                'Perfil': perfil,
                'Quantidade': 1,
                'Capacidade': next_sala['Capacidade']
            })

# Criar o resumo do ensalamento
escola_info = df_mapa_de_sala.iloc[0]
id_escola = escola_info['IdLocalProva']
nome_escola = escola_info['LocalProva']
endereco_escola = f"{escola_info['UF']}, {escola_info['Cidade']}, {escola_info['Bairro']}"

capacidade_total = df_mapa_de_sala['Capacidade'].sum()
pessoas_ensaladas = sum([e['Quantidade'] for e in ensalamento])

resumo_ensalamento = f"ID da Escola: {id_escola}\nNome da Escola: {nome_escola}\nEndereço da Escola: {endereco_escola}\nCapacidade Total da Escola: {capacidade_total}\nNúmero de Pessoas Ensaladas na Escola: {pessoas_ensaladas}\n" + "-"*60 + "\n"

for ensala in ensalamento:
    resumo_ensalamento += f"Sala: {ensala['Sala']}\nPerfis Ensalados: {ensala['Perfil']}: {ensala['Quantidade']}\nPessoas Ensaladas: {ensala['Quantidade']}\nCapacidade da Sala: {ensala['Capacidade']}\n" + "-"*60 + "\n"

print(resumo_ensalamento)

