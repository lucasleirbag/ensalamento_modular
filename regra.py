import pandas as pd
import time
import os

# Carregar os dados das planilhas
planilha_2 = pd.read_excel("data/perfis.xlsx")
planilha_3 = pd.read_excel("data/recursos.xlsx")
planilha_regras = pd.read_excel("data/regras.xlsx")

def get_fa_and_qtd_max(perfil, recursos):
    perfil_fa = planilha_2.loc[planilha_2["Participante"] == perfil, "Facil_acesso"].values[0]
    perfil_qtd_max = planilha_2.loc[planilha_2["Participante"] == perfil, "Regra"].values[0]
    recursos_fa = planilha_3.loc[planilha_3["Recurso"].isin(recursos), "Facil_acesso"].values
    recursos_qtd_max = planilha_3.loc[planilha_3["Recurso"].isin(recursos), "Regra"].values
    fa = "FA" if perfil_fa == "FA" or "FA" in recursos_fa else ""
    qtd_max = min([perfil_qtd_max] + list(recursos_qtd_max))
    return fa, qtd_max

def display_rules():
    if planilha_regras.empty:
        print("--- Nenhuma regra cadastrada ---")
        time.sleep(3)
        os.system('cls' if os.name == 'nt' else 'clear')
    else:
        print("Regras cadastradas:")
        time.sleep(3)
        os.system('cls' if os.name == 'ns' else 'clear')
        print(planilha_regras)

def save_to_excel():
    planilha_regras.to_excel("data/regras.xlsx", index=False)

def create_rule():
    global planilha_regras

    # Verifique se a coluna "ID" existe e crie-a se não existir
    if 'ID' not in planilha_regras.columns:
        planilha_regras['ID'] = [None for _ in range(len(planilha_regras))]
    
    # Determinar o último ID utilizado
    last_id = planilha_regras['ID'].max() if not planilha_regras['ID'].isnull().all() else 0

    print("\nSelecione o perfil:")
    for idx, perfil in enumerate(planilha_2["Participante"], 1):
        print(f"{idx}. {perfil}")
    perfil_choice = int(input("Escolha o número do perfil: ")) - 1
    selected_perfil = planilha_2.loc[perfil_choice, "Participante"]

    # Modificação para tornar a seleção de recursos opcional
    print("\nSelecione os recursos (ou pressione Enter para pular):")
    for idx, recurso in enumerate(planilha_3["Recurso"], 1):
        print(f"{idx}. {recurso}")
    recursos_choice = input("Escolha os números dos recursos, separados por vírgula (ou pressione Enter para pular): ")
    selected_recursos = []
    if recursos_choice:
        recursos_choice = recursos_choice.split(',')
        selected_recursos = [planilha_3.loc[int(choice) - 1, "Recurso"] for choice in recursos_choice]

    # Getting the 'Facil_acesso' and 'Regra' based on the selection
    fa, qtd_max = get_fa_and_qtd_max(selected_perfil, selected_recursos)

    selected_juncao = []
    if qtd_max > 1:
        # Selecionando a junção (com quais perfis pode ser ensalado)
        print("\nSelecione com quais perfis pode ser ensalado (ou pressione Enter para pular):")
        for idx, perfil in enumerate(planilha_2["Participante"], 1):
            print(f"{idx}. {perfil}")
        juncao_choice = input("Escolha os números dos perfis, separados por vírgula (ou pressione Enter para pular): ")
        if juncao_choice:
            juncao_choice = juncao_choice.split(',')
            selected_juncao = [planilha_2.loc[int(choice) - 1, "Participante"] for choice in juncao_choice]

    # Incrementando o ID e adicionando à regra
    last_id += 1
    new_rule = {
        "ID": last_id,
        "Perfil": selected_perfil,
        "Recursos": ", ".join(selected_recursos),
        "Facil_acesso": fa,
        "Regra": qtd_max,
        "Juncao": ", ".join(selected_juncao)
    }

    os.system('cls' if os.name == 'nt' else 'clear')

    # Mostrando o resumo da regra
    print("\nResumo da regra:")
    print(f"\nID: {new_rule['ID']}")
    print(f"Perfil: {new_rule['Perfil']}")
    print(f"Recursos: {new_rule['Recursos']}")
    print(f"Facil_acesso: {new_rule['Facil_acesso']}")
    print(f"Regra: {new_rule['Regra']}")
    print(f"Juncao: {new_rule['Juncao']}")

    confirmation = input("\nDeseja salvar esta regra? (s/n): ").strip().lower()
    if confirmation == 's':
        # Adicionando a nova regra ao DataFrame
        planilha_regras.loc[len(planilha_regras)] = new_rule
        # Reordenando as colunas para que o ID seja a primeira coluna
        planilha_regras = planilha_regras[['ID'] + [col for col in planilha_regras if col != 'ID']]
        save_to_excel()
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n--- Regra criada e salva com sucesso! ---")
        time.sleep(3)
        os.system('cls' if os.name == 'nt' else 'clear')
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\nCriação de regra cancelada.")
        time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')

def edit_rule():

    if planilha_regras.empty:
        print("\n--- Nenhuma regra cadastrada ---")
        time.sleep(3)
        os.system('cls' if os.name == 'nt' else 'clear')

        return
    display_rules()
    rule_to_edit = int(input("\nDigite o número da regra que deseja editar: "))
    print("Editando a regra:")
    print(planilha_regras.loc[rule_to_edit])

    # Reusing create_rule function to edit the selected rule
    create_rule()
    os.system('cls' if os.name == 'nt' else 'clear')

    # Removing the old rule
    planilha_regras.drop(index=rule_to_edit, inplace=True)
    save_to_excel()
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n--- Regra editada com sucesso! ---")
    time.sleep(3)
    os.system('cls' if os.name == 'nt' else 'clear')

def delete_rule():
    
    if planilha_regras.empty:
        print("\n--- Nenhuma regra cadastrada ---")
        time.sleep(3)
        os.system('cls' if os.name == 'nt' else 'clear')
        return
    
    display_rules()
    rule_to_delete = int(input("\nDigite o número da regra que deseja excluir: "))
    planilha_regras.drop(index=rule_to_delete, inplace=True)
    planilha_regras.reset_index(drop=True, inplace=True)
    save_to_excel()
    print("\nRegra excluída com sucesso!")

def main_menu():
    while True:
        print("\nMenu Principal:")
        print("1. Mostrar regras")
        print("2. Criar nova regra")
        print("3. Editar regra")
        print("4. Excluir regra")
        print("5. Sair")
        choice = input("Escolha uma opção: ")

        if choice == '1':
            os.system('cls' if os.name == 'nt' else 'clear')
            display_rules()
        elif choice == '2':
            os.system('cls' if os.name == 'nt' else 'clear')
            create_rule()
        elif choice == '3':
            os.system('cls' if os.name == 'nt' else 'clear')
            edit_rule()
        elif choice == '4':
            os.system('cls' if os.name == 'nt' else 'clear')
            delete_rule()
        elif choice == '5':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\nSAINDO...")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main_menu()
