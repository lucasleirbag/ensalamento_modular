import pandas as pd
import os

# Carregando a planilha de regras
regras_df = pd.read_excel("data/regras.xlsx")

class GruposRegrasCLI:
    def __init__(self):
        self.carregar_grupos()

    def carregar_grupos(self):
        self.grupos = []
        if os.path.exists("data/grupos.xlsx"):
            self.grupos = pd.read_excel("data/grupos.xlsx").to_dict(orient="records")

    def visualizar_grupos(self):
        if not self.grupos:
            print("Nenhum grupo foi criado ainda.")
            return
        print(pd.DataFrame(self.grupos))

    def criar_grupo(self):
        print("\nRegras disponíveis:")
        print(regras_df[['Perfil', 'Regra']])
        regras = input("Digite os IDs das regras que deseja agrupar (separados por vírgula): ").split(',')
        regras = [int(r.strip()) for r in regras]
        novo_id = len(self.grupos) + 1
        qtd_regras = len(regras)
        regras_selecionadas = regras_df[regras_df['Regra'].isin(regras)]
        recursos = []
        for recurso in regras_selecionadas['Recurso(s)']:
            if pd.notna(recurso):
                recursos.extend(recurso.split(", "))
        qtd_recursos = len(set(recursos))
        self.grupos.append({
            "Nome do Grupo": f"Grupo {novo_id}",
            "ID do Grupo": novo_id,
            "QTD de Regras": qtd_regras,
            "QTD de Recursos": qtd_recursos
        })
        pd.DataFrame(self.grupos).to_excel("data/grupos.xlsx", index=False)
        print(f"Grupo {novo_id} criado com sucesso!")
        self.carregar_grupos()

    def editar_grupo(self):
        self.visualizar_grupos()
        grupo_id = int(input("\nDigite o ID do grupo que deseja editar: "))
        print("\nRegras disponíveis:")
        print(regras_df[['Perfil', 'Regra']])
        regras = input("Digite os novos IDs das regras para esse grupo (separados por vírgula): ").split(',')
        regras = [int(r.strip()) for r in regras]
        
        for grupo in self.grupos:
            if grupo["ID do Grupo"] == grupo_id:
                grupo["QTD de Regras"] = len(regras)
                regras_selecionadas = regras_df[regras_df['Regra'].isin(regras)]
                recursos = []
                for recurso in regras_selecionadas['Recurso(s)']:
                    if pd.notna(recurso):
                        recursos.extend(recurso.split(", "))
                grupo["QTD de Recursos"] = len(set(recursos))
                break
        else:
            print(f"Grupo {grupo_id} não encontrado.")
            return
        
        pd.DataFrame(self.grupos).to_excel("data/grupos.xlsx", index=False)
        print(f"Grupo {grupo_id} editado com sucesso!")
        self.carregar_grupos()

    def excluir_grupo(self):
        self.visualizar_grupos()
        grupo_id = int(input("\nDigite o ID do grupo que deseja excluir: "))
        self.grupos = [g for g in self.grupos if g["ID do Grupo"] != grupo_id]
        pd.DataFrame(self.grupos).to_excel("data/grupos.xlsx", index=False)
        print(f"Grupo {grupo_id} excluído com sucesso!")
        self.carregar_grupos()

    def menu(self):
        while True:
            print("\nMenu:")
            print("1. Visualizar Grupos")
            print("2. Criar Grupo")
            print("3. Editar Grupo")
            print("4. Excluir Grupo")
            print("5. Sair")
            escolha = input("Digite a opção desejada: ")

            if escolha == '1':
                self.visualizar_grupos()
            elif escolha == '2':
                self.criar_grupo()
            elif escolha == '3':
                self.editar_grupo()
            elif escolha == '4':
                self.excluir_grupo()
            elif escolha == '5':
                break
            else:
                print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    cli = GruposRegrasCLI()
    cli.menu()


