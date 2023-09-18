import pandas as pd
import os

regras_df = pd.read_excel("data/regras.xlsx")

def criar_grupo_modified(self):
    print("\nRegras disponíveis:")
    print(regras_df[['ID', 'Perfil', 'Regra']])
    regras = input("Digite os IDs das regras que deseja agrupar (separados por vírgula): ").split(',')
    regras = [int(r.strip()) for r in regras]
    novo_id = len(self.grupos) + 1
    regras_selecionadas = regras_df[regras_df['ID'].isin(regras)]
    recursos = regras_selecionadas['Recursos'].unique()
    facil_acesso = any(regras_selecionadas['Facil_acesso'] == "FA")
    valor_regra = regras_selecionadas['Regra'].min()
    perfil_grupo = ', '.join(regras_selecionadas['Perfil'])
    self.grupos.append({
        "ID do Grupo": novo_id,
        "Perfil": perfil_grupo,
        "Recursos": ', '.join([str(r) for r in recursos if pd.notna(r)]),
        "Facil Acesso": "FA" if facil_acesso else "NaN",
        "Regra": valor_regra
    })
    pd.DataFrame(self.grupos).to_excel("data/grupos.xlsx", index=False)
    print(f"Grupo {novo_id} criado com sucesso!")
    self.carregar_grupos()

def editar_grupo_modified(self):
    self.visualizar_grupos()
    try:
        grupo_id = int(input("\nDigite o ID do grupo que deseja editar: "))
        if not any(g['ID do Grupo'] == grupo_id for g in self.grupos):
            raise ValueError
        print("\nRegras disponíveis:")
        print(self.regras_df[['ID', 'Perfil', 'Regra']])
        regras = input("Digite os novos IDs das regras para esse grupo (separados por vírgula): ").split(',')
        regras = [int(r.strip()) for r in regras]
        regras_selecionadas = self.regras_df[self.regras_df['ID'].isin(regras)]
        recursos = regras_selecionadas['Recursos'].unique()
        facil_acesso = any(regras_selecionadas['Facil_acesso'] == "FA")
        valor_regra = regras_selecionadas['Regra'].min()
        perfil_grupo = ', '.join(regras_selecionadas['Perfil'])
        for grupo in self.grupos:
            if grupo['ID do Grupo'] == grupo_id:
                grupo['Perfil'] = perfil_grupo
                grupo['Recursos'] = ', '.join([str(r) for r in recursos if pd.notna(r)])
                grupo['Facil Acesso'] = 'FA' if facil_acesso else 'Não'
                grupo['Regra'] = valor_regra
        pd.DataFrame(self.grupos).to_excel("data/grupos.xlsx", index=False)
        print(f"Grupo {grupo_id} editado com sucesso!")
        self.carregar_grupos()
    except ValueError:
        print(f"Grupo {grupo_id} não encontrado.")
        return

def excluir_grupo_modified(self):
    self.visualizar_grupos()
    try:
        grupo_id = int(input("\nDigite o ID do grupo que deseja excluir: "))
        if not any(g['ID do Grupo'] == grupo_id for g in self.grupos):
            raise ValueError
        self.grupos = [g for g in self.grupos if g["ID do Grupo"] != grupo_id]
        pd.DataFrame(self.grupos).to_excel("data/grupos.xlsx", index=False)
        print(f"Grupo {grupo_id} excluído com sucesso!")
        self.carregar_grupos()
    except ValueError:
        print(f"Grupo {grupo_id} não encontrado.")
        return

class GruposRegrasCLI:
    def __init__(self):
        self.regras_df = regras_df
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
        criar_grupo_modified(self)
    
    def editar_grupo(self):
        editar_grupo_modified(self)
    
    def excluir_grupo(self):
        excluir_grupo_modified(self)
    
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

