import pandas as pd

# Função para ensalar os candidatos nas salas
def ensalar_candidatos_otimizado(df_regras, df_candidatos, df_mapa_de_sala):
    ensalamento = []
    salas_usadas = set()
    
    # Filtrar salas de fácil acesso (térreo ou 1º andar)
    salas_facil_acesso = df_mapa_de_sala[df_mapa_de_sala['Andar'].isin(['Térreo', '1º Andar'])]
    
    for _, regra in df_regras.iterrows():
        perfil = regra['Perfil']
        max_per_sala = regra['Regra']
        facil_acesso = regra['Facil_acesso']
        
        if facil_acesso == 'FA':
            salas_disponiveis = salas_facil_acesso.copy()
        else:
            salas_disponiveis = df_mapa_de_sala.copy()
        
        # Ordenando as salas de acordo com a regra
        if max_per_sala <= 5:
            salas_disponiveis = salas_disponiveis.sort_values(by='Capacidade', ascending=True)
        else:
            salas_disponiveis = salas_disponiveis.sort_values(by='Capacidade', ascending=False)
        
        candidatos_perfil = df_candidatos[df_candidatos['Candidato'] == perfil]
        
        for _, candidato in candidatos_perfil.iterrows():
            alocado = False
            for _, sala in salas_disponiveis.iterrows():
                if sala['Sala'] not in salas_usadas:
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
                    sala_usada = next((e for e in ensalamento if e['Sala'] == sala['Sala'] and e['Perfil'] == perfil), None)
                    if sala_usada and (sala_usada['Quantidade'] < min(max_per_sala, sala['Capacidade'])):
                        sala_usada['Quantidade'] += 1
                        alocado = True
                        break
            
            if not alocado:
                break

    # Ordenar ensalamento pela numeração das salas
    ensalamento = sorted(ensalamento, key=lambda x: x['Sala'])
    return ensalamento, salas_usadas

# Função para gerar o relatório de ensalamento
def gerar_relatorio(ensalamento, salas_usadas, df_mapa_de_sala, df_candidatos):
    salas_nao_usadas = set(df_mapa_de_sala['Sala']) - salas_usadas
    capacidade_nao_usada = df_mapa_de_sala[df_mapa_de_sala['Sala'].isin(salas_nao_usadas)]['Capacidade'].sum()

    candidatos_ensalados = sum([e['Quantidade'] for e in ensalamento])
    candidatos_nao_ensalados = len(df_candidatos) - candidatos_ensalados
    perfis_nao_ensalados = set(df_candidatos['Candidato']) - set([e['Perfil'] for e in ensalamento])

    escola_info = df_mapa_de_sala.iloc[0]
    id_escola = escola_info['IdLocalProva']
    nome_escola = escola_info['LocalProva']
    endereco_escola = f"{escola_info['UF']}, {escola_info['Cidade']}, {escola_info['Bairro']}"

    capacidade_total = df_mapa_de_sala['Capacidade'].sum()
    pessoas_ensaladas = sum([e['Quantidade'] for e in ensalamento])

    resumo_ensalamento = f"ID da Escola: {id_escola}\nNome da Escola: {nome_escola}\nEndereço da Escola: {endereco_escola}\nCapacidade Total da Escola: {capacidade_total}\nNúmero de Pessoas Ensaladas na Escola: {pessoas_ensaladas}\n" + "-"*60 + "\n"

    for ensala in ensalamento:
        resumo_ensalamento += f"Sala: {ensala['Sala']}\nPerfis Ensalados: {ensala['Perfil']}: {ensala['Quantidade']}\nPessoas Ensaladas: {ensala['Quantidade']}\nCapacidade da Sala: {ensala['Capacidade']}\n" + "-"*60 + "\n"

    if salas_nao_usadas:
        resumo_ensalamento += f"\nSalas não utilizadas: {', '.join(map(str, salas_nao_usadas))}\nCapacidade não utilizada: {capacidade_nao_usada}\n"

    if candidatos_nao_ensalados:
        resumo_ensalamento += f"\nCandidatos não ensalados: {candidatos_nao_ensalados}\nPerfis não ensalados: {', '.join(perfis_nao_ensalados)}\n"

    return resumo_ensalamento

# Carregar os arquivos
df_regras = pd.read_excel("data/regras.xlsx")
df_candidatos = pd.read_excel("data_dist/candidatos.xlsx")
df_mapa_de_sala = pd.read_excel("data_dist/mapa_de_sala.xlsx")

# Executar ensalamento otimizado e gerar relatório
ensalamento_otimizado, salas_usadas_otimizado = ensalar_candidatos_otimizado(df_regras, df_candidatos, df_mapa_de_sala)
resumo = gerar_relatorio(ensalamento_otimizado, salas_usadas_otimizado, df_mapa_de_sala, df_candidatos)
print(resumo)


