import pandas as pd

# Carregar bases de dados
regras_df = pd.read_excel("data/regras.xlsx")
grupos_df = pd.read_excel("data/grupos.xlsx")
candidatos_df = pd.read_excel("data_dist/candidatos.xlsx")
mapa_de_sala_df = pd.read_excel("data_dist/mapa_de_sala.xlsx")

def ensalamento_completo(df_regras, df_candidatos, df_mapa_de_sala, df_grupos):
    # 1. Identificar os candidatos que devem ser ensalados em grupo
    candidatos_ensalados_grupo = set()
    ensalamento_grupo = []
    for _, grupo in df_grupos.iterrows():
        perfis_grupo = [p.split('-')[1].strip() for p in grupo['Perfil'].split(',')]
        candidatos_grupo = df_candidatos[df_candidatos['Candidato'].isin(perfis_grupo)]
        total_candidatos_grupo = candidatos_grupo.shape[0]
        
        if grupo['Facil_acesso'] == 'FA':
            salas_disponiveis = df_mapa_de_sala[df_mapa_de_sala['Andar'].isin(['Térreo', '1º Andar'])].copy()
        else:
            salas_disponiveis = df_mapa_de_sala.copy()
        
        salas_capacidade_suficiente = salas_disponiveis[salas_disponiveis['Capacidade'] >= total_candidatos_grupo]
        
        if not salas_capacidade_suficiente.empty:
            sala_selecionada = salas_capacidade_suficiente.iloc[0]
            ensalamento_grupo.append({
                'Sala': sala_selecionada['Sala'],
                'Perfil': ', '.join(perfis_grupo),
                'Quantidade': total_candidatos_grupo,
                'Capacidade da Sala': sala_selecionada['Capacidade'],
                'Grupo': f"Grupo {grupo['ID do Grupo']}"
            })
            candidatos_ensalados_grupo.update(candidatos_grupo.index.tolist())
            df_mapa_de_sala = df_mapa_de_sala[df_mapa_de_sala['Sala'] != sala_selecionada['Sala']]
    
    # 2. Ensalamento dos candidatos individuais
    candidatos_individual = df_candidatos.drop(index=candidatos_ensalados_grupo)
    ensalamento_individual = []
    for _, regra in df_regras.iterrows():
        perfil = regra['Perfil']
        candidatos_perfil = candidatos_individual[candidatos_individual['Candidato'] == perfil]
        total_candidatos_perfil = candidatos_perfil.shape[0]
        
        while total_candidatos_perfil > 0 and not df_mapa_de_sala.empty:
            if regra['Facil_acesso'] == 'FA':
                salas_disponiveis = df_mapa_de_sala[df_mapa_de_sala['Andar'].isin(['Térreo', '1º Andar'])].copy()
            else:
                salas_disponiveis = df_mapa_de_sala.copy()
            
            sala_selecionada = salas_disponiveis.iloc[0]
            qtd_ensalada = min(total_candidatos_perfil, sala_selecionada['Capacidade'])
            ensalamento_individual.append({
                'Sala': sala_selecionada['Sala'],
                'Perfil': perfil,
                'Quantidade': qtd_ensalada,
                'Capacidade da Sala': sala_selecionada['Capacidade'],
                'Grupo': 'Individual'
            })
            
            total_candidatos_perfil -= qtd_ensalada
            df_mapa_de_sala = df_mapa_de_sala[df_mapa_de_sala['Sala'] != sala_selecionada['Sala']]
    
    # Consolidando o ensalamento
    ensalamento_final = ensalamento_grupo + ensalamento_individual
    return pd.DataFrame(ensalamento_final)

# Executando o ensalamento completo
ensalamento_final_df = ensalamento_completo(regras_df, candidatos_df, mapa_de_sala_df, grupos_df)
print(ensalamento_final_df)




