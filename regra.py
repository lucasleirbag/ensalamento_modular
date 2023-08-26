import pandas as pd

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
        print("Nenhuma regra cadastrada.")
    else:
        print("Regras cadastradas:")
        print(planilha_regras)

def save_to_excel():
    planilha_regras.to_excel("data/regras.xlsx", index=False)

def create_rule():
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

    # Creating a new rule
    new_rule = {
        "Perfil": selected_perfil,
        "Recurso(s)": ", ".join(selected_recursos),
        "Facil_acesso": fa,
        "Regra": qtd_max,
        "Juncao": ", ".join(selected_juncao)
    }

    # Mostrando o resumo da regra
    print("\nResumo da regra:")
    print(f"Perfil: {new_rule['Perfil']}")
    print(f"Recurso(s): {new_rule['Recurso(s)']}")
    print(f"Facil_acesso: {new_rule['Facil_acesso']}")
    print(f"Regra: {new_rule['Regra']}")
    print(f"Juncao: {new_rule['Juncao']}")

    confirmation = input("Deseja salvar esta regra? (s/n): ").strip().lower()
    if confirmation == 's':
        # Adicionando a nova regra ao DataFrame
        planilha_regras.loc[len(planilha_regras)] = new_rule
        save_to_excel()
        print("\nRegra criada e salva com sucesso!")
    else:
        print("\nCriação de regra cancelada.")

def edit_rule():
    display_rules()
    rule_to_edit = int(input("Digite o número da regra que deseja editar: ")) - 1
    print("Editando a regra:")
    print(planilha_regras.loc[rule_to_edit])

    # Reusing create_rule function to edit the selected rule
    create_rule()

    # Removing the old rule
    planilha_regras.drop(index=rule_to_edit, inplace=True)
    save_to_excel()
    print("Regra editada com sucesso!")

def delete_rule():
    display_rules()
    rule_to_delete = int(input("Digite o número da regra que deseja excluir: "))
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
            display_rules()
        elif choice == '2':
            create_rule()
        elif choice == '3':
            edit_rule()
        elif choice == '4':
            delete_rule()
        elif choice == '5':
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main_menu()