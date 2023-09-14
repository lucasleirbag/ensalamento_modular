import pandas as pd

# Carregar os dados das planilhas
planilha_2 = pd.read_excel("data/planilha_2.xlsx")
planilha_3 = pd.read_excel("1data/planilha_3.xlsx")

def get_fa_and_qtd_max(perfil, recursos):
    perfil_fa = planilha_2.loc[planilha_2["Participante"] == perfil, "Facil_acesso"].values[0]
    perfil_qtd_max = planilha_2.loc[planilha_2["Participante"] == perfil, "Regra"].values[0]
    
    recursos_fa = planilha_3.loc[planilha_3["Recurso"].isin(recursos), "Facil_acesso"].values
    recursos_qtd_max = planilha_3.loc[planilha_3["Recurso"].isin(recursos), "Regra"].values
    
    fa = "FA" if perfil_fa == "FA" or "FA" in recursos_fa else ""
    qtd_max = min([perfil_qtd_max] + list(recursos_qtd_max))
    return fa, qtd_max

def create_rule():
    print("\nSelecione o perfil:")
    for idx, perfil in enumerate(planilha_2["Participante"], 1):
        print(f"{idx}. {perfil}")
    perfil_choice = int(input("Digite o número correspondente ao perfil: "))
    perfil = planilha_2["Participante"].iloc[perfil_choice - 1]

    print("\nSelecione o(s) recurso(s) (separados por vírgula):")
    for idx, recurso in enumerate(planilha_3["Recurso"], 1):
        print(f"{idx}. {recurso}")
    recursos_choices = input("Digite os números correspondentes aos recursos, separados por vírgula: ")
    recursos = [planilha_3["Recurso"].iloc[int(choice) - 1] for choice in recursos_choices.split(",")]

    print("\nSelecione a junção de perfil (separados por vírgula):")
    for idx, juncao_perfil in enumerate(planilha_2["Participante"], 1):
        print(f"{idx}. {juncao_perfil}")
    juncao_choices = input("Digite os números correspondentes à junção de perfil, separados por vírgula: ")
    juncoes = [planilha_2["Participante"].iloc[int(choice) - 1] for choice in juncao_choices.split(",")]

    fa, qtd_max = get_fa_and_qtd_max(perfil, recursos)

    print(f"\nRegra criada:\nPerfil: {perfil}\nRecurso(s): {', '.join(recursos)}\nJunção de Perfil: {', '.join(juncoes)}\nFA: {fa}\nQtd Máxima: {qtd_max}\n")

if __name__ == "__main__":
    while True:
        print("1. Criar nova regra")
        print("2. Sair")
        choice = input("Escolha uma opção: ")

        if choice == "1":
            create_rule()
        elif choice == "2":
            print("Encerrando programa...")
            break
