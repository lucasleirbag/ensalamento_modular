import pandas as pd

# Funções definidas para o ensalamento

def identificar_ensalamento(df_regras, df_candidatos, df_mapa_de_sala, df_grupos):
    candidatos_ensalados_grupo = set()
    candidatos_ensalados_individual = set()
    
    # Identificar candidatos ensalados em grupo
    for _, grupo in df_grupos.iterrows():
        perfis_grupo = [p.split('-')[1].strip() for p in grupo['Perfil'].split(',')]
        total_candidatos_grupo = df_candidatos[df_candidatos['Candidato'].isin(perfis_grupo)].shape[0]
        
        if grupo['Facil Acesso'] == 'FA':
            salas_disponiveis = df_mapa_de_sala[df_mapa_de_sala['Andar'].isin(['Térreo', '1º Andar'])].copy()
        else:
            salas_disponiveis = df_mapa_de_sala.copy()
        
        # Verificar se há salas que podem acomodar todos os candidatos do grupo
        salas_capacidade_suficiente = salas_disponiveis[salas_disponiveis['Capacidade'] >= total_candidatos_grupo]
        
        if not salas_capacidade_suficiente.empty:
            candidatos_ensalados_grupo.update(df_candidatos[df_candidatos['Candidato'].isin(perfis_grupo)].index.tolist())

    # Identificar candidatos ensalados individualmente
    candidatos_ensalados_individual = set(df_candidatos.index) - candidatos_ensalados_grupo

    return list(candidatos_ensalados_grupo), list(candidatos_ensalados_individual)

def ensalar_individualmente(df_regras, candidatos_individual, df_mapa_de_sala, salas_usadas_grupo):
    ensalamento_individual = []
    salas_usadas_individual = set()

    for _, regra in df_regras.iterrows():
        perfil_regra = regra['Perfil']
        qtd_candidatos = candidatos_individual.count(perfil_regra)

        if qtd_candidatos == 0:
            continue

        if regra['Facil Acesso'] == 'FA':
            salas_disponiveis = df_mapa_de_sala[df_mapa_de_sala['Andar'].isin(['Térreo', '1º Andar'])].copy()
        else:
            salas_disponiveis = df_mapa_de_sala.copy()

        # Removendo salas já utilizadas pelo ensalamento em grupo
        salas_disponiveis = salas_disponiveis[~salas_disponiveis['Sala'].isin(salas_usadas_grupo)]

        # Ordenando salas por capacidade
        salas_disponiveis = salas_disponiveis.sort_values(by='Capacidade', ascending=True)

        alocado = False
        for _, sala in salas_disponiveis.iterrows():
            if sala['Sala'] not in salas_usadas_individual and sala['Capacidade'] >= qtd_candidatos:
                salas_usadas_individual.add(sala['Sala'])
                ensalamento_individual.append({
                    'Sala': sala['Sala'],
                    'Perfil': perfil_regra,
                    'Quantidade': qtd_candidatos,
                    'Capacidade': sala['Capacidade']
                })
                alocado = True
                break

        if not alocado:
            print(f"Não foi possível alocar os candidatos de perfil {perfil_regra} em nenhuma sala.")

    return ensalamento_individual



def ensalar_grupo_consolidado(df_mapa_de_sala, df_grupos, df_candidatos):
    ensalamento_grupo = []
    salas_usadas_grupo = set()
    
    # Agrupando candidatos por grupo
    candidatos_agrupados_por_grupo = {}
    for _, row in df_candidatos.iterrows():
        perfil_candidato = row['Candidato']
        grupos_pertencentes = df_grupos[df_grupos['Perfil'].str.contains(perfil_candidato)]
        for _, grupo in grupos_pertencentes.iterrows():
            grupo_id = "Grupo " + str(int(grupo['ID do Grupo']))
            if grupo_id not in candidatos_agrupados_por_grupo:
                candidatos_agrupados_por_grupo[grupo_id] = []
            candidatos_agrupados_por_grupo[grupo_id].append(perfil_candidato)
    for grupo_id, candidatos_grupo in candidatos_agrupados_por_grupo.items():
        qtd_candidatos = len(candidatos_grupo)
        grupo_data = df_grupos[df_grupos['ID do Grupo'] == int(grupo_id.split()[1])].iloc[0]
        
        if grupo_data['Facil Acesso'] == 'FA':
            salas_disponiveis = df_mapa_de_sala[df_mapa_de_sala['Andar'].isin(['Térreo', '1º Andar'])].copy()
        else:
            salas_disponiveis = df_mapa_de_sala.copy()
        
        # Ordenando salas por capacidade
        salas_disponiveis = salas_disponiveis.sort_values(by='Capacidade', ascending=True)
        
        alocado = False
        for _, sala in salas_disponiveis.iterrows():
            if sala['Sala'] not in salas_usadas_grupo and sala['Capacidade'] >= qtd_candidatos:
                salas_usadas_grupo.add(sala['Sala'])
                ensalamento_grupo.append({
                    'Sala': sala['Sala'],
                    'Perfil': ", ".join(candidatos_grupo),
                    'Quantidade': qtd_candidatos,
                    'Capacidade': sala['Capacidade'],
                    'Grupo': grupo_id
                })
                alocado = True
                break
        
        if not alocado:
            print(f"Não foi possível alocar os candidatos do {grupo_id} em nenhuma sala.")
        else:
            # Removendo a sala usada das salas disponíveis
            df_mapa_de_sala = df_mapa_de_sala[df_mapa_de_sala['Sala'] != sala['Sala']]
                
    return ensalamento_grupo


def gerar_relatorio_ensalamento(ensalamento_individual, ensalamento_grupo):
    relatorio = []

    # Adicionando ensalamento individual ao relatório
    for item in ensalamento_individual:
        relatorio.append({
            'Sala': item['Sala'],
            'Perfil': item['Perfil'],
            'Quantidade': item['Quantidade'],
            'Capacidade da Sala': item['Capacidade'],
            'Grupo': 'Individual'
        })

    # Adicionando ensalamento em grupo ao relatório
    for item in ensalamento_grupo:
        relatorio.append({
            'Sala': item['Sala'],
            'Perfil': item['Perfil'],
            'Quantidade': item['Quantidade'],
            'Capacidade da Sala': item['Capacidade'],
            'Grupo': item['Grupo']
        })

    return pd.DataFrame(relatorio)
# Carregando os dados
regras_df = pd.read_excel('data/regras.xlsx')
grupos_df = pd.read_excel('data/grupos.xlsx')
mapa_de_sala_df = pd.read_excel('data_dist/mapa_de_sala.xlsx')
candidatos_df = pd.read_excel('data_dist/candidatos.xlsx')

# Identificando os candidatos para ensalamento
candidatos_grupo_nomes, candidatos_individual_nomes = identificar_ensalamento(regras_df, candidatos_df, mapa_de_sala_df, grupos_df)

# Realizando o ensalamento em grupo
ensalamento_grupo = ensalar_grupo_consolidado(mapa_de_sala_df, grupos_df, candidatos_df)

# Recuperando as salas já usadas pelo ensalamento em grupo
salas_usadas_grupo = [item['Sala'] for item in ensalamento_grupo]

# Realizando o ensalamento individual
ensalamento_individual = ensalar_individualmente(regras_df, candidatos_individual_nomes, mapa_de_sala_df, salas_usadas_grupo)

# Gerando o relatório final
relatorio_final = gerar_relatorio_ensalamento(ensalamento_individual, ensalamento_grupo)
print(relatorio_final)