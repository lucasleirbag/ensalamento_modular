import pandas as pd
import tabulate

def ensalamento_completo_corrigido(df_regras, df_candidatos, df_mapa_de_sala, df_grupos):
    candidatos_ensalados_grupo = set()
    ensalamento_grupo = []
    
    for _, grupo in df_grupos.iterrows():
        perfis_grupo = [p.split('-')[1].strip() if '-' in p else p.strip() for p in grupo['Perfil'].split(',')]
        candidatos_grupo = df_candidatos[df_candidatos['Candidato'].isin(perfis_grupo)]
        
        # Checando os recursos necessários para o grupo
        recursos_necessarios = str(grupo["Recursos"]).split(', ')
        
        # Filtrando candidatos que não possuem pelo menos um dos recursos do grupo
        candidatos_grupo = candidatos_grupo[candidatos_grupo["Recursos"].apply(lambda x: any([rec in str(x) for rec in recursos_necessarios]))]
        
        total_candidatos_grupo = candidatos_grupo.shape[0]
        
        # Se houver apenas um candidato no grupo, continue e trate-o como individual
        if total_candidatos_grupo == 1:
            continue
        
        if grupo['Facil_acesso'] == 'FA':
            salas_disponiveis = df_mapa_de_sala[df_mapa_de_sala['Andar'].isin(['Térreo', '1º Andar'])].copy()
        else:
            salas_disponiveis = df_mapa_de_sala.copy()
        
        salas_capacidade_suficiente = salas_disponiveis[salas_disponiveis['Capacidade'] >= total_candidatos_grupo]
        
        if not salas_capacidade_suficiente.empty:
            sala_selecionada = salas_capacidade_suficiente.iloc[0]
            ensalamento_grupo.append({
                'Sala': sala_selecionada['Sala'],
                'Perfil': ', '.join(candidatos_grupo['Candidato']),
                'Quantidade': total_candidatos_grupo,
                'Capacidade da Sala': sala_selecionada['Capacidade'],
                'Grupo': f"Grupo {grupo['ID do Grupo']}",
                'Recursos': ', '.join(recursos_necessarios) if recursos_necessarios[0] != 'nan' else '',
                'Facil Acesso': 'FA' if grupo['Facil_acesso'] == 'FA' else ''
            })
            candidatos_ensalados_grupo.update(candidatos_grupo.index.tolist())
            df_mapa_de_sala = df_mapa_de_sala[df_mapa_de_sala['Sala'] != sala_selecionada['Sala']]
    
    # Ensalamento dos candidatos individuais
    candidatos_individual = df_candidatos.drop(index=candidatos_ensalados_grupo)
    ensalamento_individual = []
    
    for _, regra in df_regras.iterrows():
        perfil = regra['Perfil']
        recursos_regra = str(regra["Recursos"]).split(', ')
        maximo_por_sala = regra['Regra']
        
        # Filtrando candidatos que atendem ao perfil e aos recursos da regra
        candidatos_perfil = candidatos_individual[(candidatos_individual['Candidato'] == perfil) & 
                                                  (candidatos_individual["Recursos"].apply(lambda x: any([rec in str(x) for rec in recursos_regra])))]
        
        # Se não há candidatos que atendem ao perfil e aos recursos da regra, continue
        if candidatos_perfil.empty:
            continue
        
        total_candidatos_perfil = candidatos_perfil.shape[0]
        
        while total_candidatos_perfil > 0 and not df_mapa_de_sala.empty:
            if regra['Facil_acesso'] == 'FA':
                salas_disponiveis = df_mapa_de_sala[df_mapa_de_sala['Andar'].isin(['Térreo', '1º Andar'])].copy()
            else:
                salas_disponiveis = df_mapa_de_sala.copy()
            
            sala_selecionada = salas_disponiveis.iloc[0]
            qtd_ensalada = min(total_candidatos_perfil, sala_selecionada['Capacidade'], maximo_por_sala)
            ensalamento_individual.append({
                'Sala': sala_selecionada['Sala'],
                'Perfil': perfil,
                'Quantidade': qtd_ensalada,
                'Capacidade da Sala': sala_selecionada['Capacidade'],
                'Grupo': 'Individual',
                'Recursos': regra['Recursos'] if pd.notna(regra['Recursos']) else '',
                'Facil Acesso': 'FA' if regra['Facil_acesso'] == 'FA' else ''
            })
            
            total_candidatos_perfil -= qtd_ensalada
            df_mapa_de_sala = df_mapa_de_sala[df_mapa_de_sala['Sala'] != sala_selecionada['Sala']]
            
            # Removendo candidatos ensalados, mas verificando se o índice realmente existe
            indices_a_remover = candidatos_perfil.index[:qtd_ensalada].tolist()
            indices_existentes = candidatos_individual.index.intersection(indices_a_remover)
            candidatos_individual = candidatos_individual.drop(index=indices_existentes)
    
    # Consolidando o ensalamento
    ensalamento_final = ensalamento_grupo + ensalamento_individual
    return pd.DataFrame(ensalamento_final), df_mapa_de_sala, candidatos_individual

def gerar_relatorio_atualizado_v3(ensalamento, escola_info, capacidade_total, capacidade_utilizada, salas_restantes, candidatos_sem_regra):
    # Informações iniciais sobre a escola
    relatorio = []
    relatorio.append("Informações da Escola:")
    relatorio.append(f"ID da Escola: {escola_info['IdLocalProva']}")
    relatorio.append(f"UF: {escola_info['UF']}")
    relatorio.append(f"Cidade: {escola_info['Cidade']}")
    relatorio.append(f"Bairro: {escola_info['Bairro']}")
    relatorio.append(f"Nome da Escola: {escola_info['LocalProva']}")
    relatorio.append(f"Capacidade Total: {capacidade_total} candidatos")
    relatorio.append(f"Capacidade Utilizada: {capacidade_utilizada} candidatos")
    
    # Informações sobre salas não utilizadas
    relatorio.append("\nSalas Não Utilizadas:")
    if salas_restantes.empty:
        relatorio.append("Todas as salas foram utilizadas.")
    else:
        relatorio.append(f"Total de Salas Não Utilizadas: {len(salas_restantes)}")
        for _, sala in salas_restantes.iterrows():
            relatorio.append(f"Sala {sala['Sala']} - Capacidade: {sala['Capacidade']} candidatos")
    
    # Informações sobre candidatos sem regra definida
    relatorio.append("\nCandidatos Sem Regra Definida:")
    if not candidatos_sem_regra:
        relatorio.append("Todos os candidatos têm regras definidas.")
    else:
        for candidato in candidatos_sem_regra:
            relatorio.append(candidato)

    # Quantidade de colaboradores ensalados e capacidade da sala
    relatorio.append("\nResumo do Ensalamento:")
    total_ensalados = ensalamento['Quantidade'].sum()
    capacidade_sala_total = ensalamento['Capacidade da Sala'].sum()
    relatorio.append(f"Total de Colaboradores Ensalados: {total_ensalados}")
    relatorio.append(f"Capacidade Total das Salas Usadas: {capacidade_sala_total} candidatos")
    relatorio.append("\nDetalhes do Ensalamento:")

    # Construindo a tabela principal de ensalamento
    headers_ensalamento = ensalamento.columns.tolist()
    ensalamento_table = tabulate.tabulate(ensalamento.values, headers=headers_ensalamento, tablefmt="grid")

    # Combinando todas as partes para formar o relatório completo
    relatorio_final = "\n".join(relatorio) + "\n\n" + ensalamento_table
    return relatorio_final

# Carregando os arquivos
df_regras = pd.read_excel("data/regras.xlsx")
df_candidatos = pd.read_excel("data_dist/candidatos.xlsx")
df_mapa_de_sala = pd.read_excel("data_dist/mapa_de_sala.xlsx")
df_grupos = pd.read_excel("data/grupos.xlsx")

# Informações sobre a escola utilizada
escola_info = df_mapa_de_sala.iloc[0][['IdLocalProva', 'UF', 'Cidade', 'Bairro', 'LocalProva']]
capacidade_total = df_mapa_de_sala['Capacidade'].sum()

# Executando o ensalamento
ensalamento_resultado, salas_restantes, candidatos_nao_ensalados = ensalamento_completo_corrigido(df_regras, df_candidatos, df_mapa_de_sala, df_grupos)
capacidade_utilizada = ensalamento_resultado['Quantidade'].sum()

# Identificar candidatos sem regra definida
candidatos_unicos = set(df_candidatos['Candidato'])
regras_unicas = set(df_regras['Perfil'])
candidatos_sem_regra = candidatos_unicos - regras_unicas

# Gerando o relatório atualizado
relatorio_atualizado_v3 = gerar_relatorio_atualizado_v3(ensalamento_resultado, escola_info, capacidade_total, capacidade_utilizada, salas_restantes, candidatos_sem_regra)
print(relatorio_atualizado_v3)
