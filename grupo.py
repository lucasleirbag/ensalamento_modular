import pandas as pd
import os
import time

regras_df = pd.read_excel("data/regras.xlsx")

def criar_grupo_modified(self):
    print("\nRegras disponíveis:")
    print(self.regras_df[['ID', 'Perfil', 'Recursos', 'Regra']].to_string(index=False))
    regras = input("\nDigite os IDs das regras que deseja agrupar (separados por vírgula): ").split(',')
    regras = [int(r.strip()) for r in regras]
    novo_id = len(self.grupos) + 1
    regras_selecionadas = self.regras_df[self.regras_df['ID'].isin(regras)]
    recursos = regras_selecionadas['Recursos'].unique()
    facil_acesso = any(regras_selecionadas['Facil_acesso'] == "FA")
    valor_regra = regras_selecionadas['Regra'].min()
    perfil_grupo = ', '.join([f"{r['ID']}-{r['Perfil']}" for _, r in regras_selecionadas.iterrows()])
    
    self.grupos.append({
        "ID do Grupo": novo_id,
        "Perfil": perfil_grupo,
        "Recursos": ', '.join([str(r) for r in recursos if pd.notna(r)]),
        "Facil Acesso": "FA" if facil_acesso else "NaN",
        "Regra": valor_regra
    })
    pd.DataFrame(self.grupos).to_excel("data/grupos.xlsx", index=False)
    
    # Atualizar a coluna "Grupo" na base de regras
    for index, row in self.regras_df.iterrows():
        if row['ID'] in regras:
            if pd.isna(row['Grupo']):
                self.regras_df.at[index, 'Grupo'] = str(novo_id)
            else:
                existing_groups = row['Grupo'].split(", ")
                if str(novo_id) not in existing_groups:
                    existing_groups.append(str(novo_id))
                    self.regras_df.at[index, 'Grupo'] = ", ".join(existing_groups)
    self.regras_df.to_excel("data/regras.xlsx", index=False)
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\n--- Grupo {novo_id} criado com sucesso ---")
    time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')
    self.carregar_grupos()

def editar_grupo_modified(self):
    self.visualizar_grupos()
    try:
        grupo_id = int(input("\nDigite o ID do grupo que deseja editar: "))
        if not any(g['ID do Grupo'] == grupo_id for g in self.grupos):
            raise ValueError
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n--- Editando o grupo {grupo_id} ---")
        print("\nRegras disponíveis:")
        print(self.regras_df[['ID', 'Perfil', 'Regra']].to_string(index=False))
        regras = input("Digite os novos IDs das regras para esse grupo (separados por vírgula): ").split(',')
        regras = [int(r.strip()) for r in regras]
        regras_selecionadas = self.regras_df[self.regras_df['ID'].isin(regras)]
        recursos = regras_selecionadas['Recursos'].unique()
        facil_acesso = any(regras_selecionadas['Facil_acesso'] == "FA")
        valor_regra = regras_selecionadas['Regra'].min()
        perfil_grupo = ', '.join([f"{r['ID']}-{r['Perfil']}" for _, r in regras_selecionadas.iterrows()])
        
        # Removendo o ID do grupo das regras anteriormente associadas
        for index, row in self.regras_df.iterrows():
            existing_groups = str(row['Grupo']).split(", ")
            if str(grupo_id) in existing_groups:
                existing_groups.remove(str(grupo_id))
                self.regras_df.at[index, 'Grupo'] = ", ".join(existing_groups)
        
        # Adicionando o ID do grupo às novas regras selecionadas
        for index, row in self.regras_df.iterrows():
            if row['ID'] in regras:
                if pd.isna(row['Grupo']) or row['Grupo'] == "":
                    self.regras_df.at[index, 'Grupo'] = str(grupo_id)
                else:
                    existing_groups = row['Grupo'].split(", ")
                    if str(grupo_id) not in existing_groups:
                        existing_groups.append(str(grupo_id))
                        self.regras_df.at[index, 'Grupo'] = ", ".join(existing_groups)
        
        # Atualizando o grupo
        for grupo in self.grupos:
            if grupo['ID do Grupo'] == grupo_id:
                grupo['Perfil'] = perfil_grupo
                grupo['Recursos'] = ', '.join([str(r) for r in recursos if pd.notna(r)])
                grupo['Facil Acesso'] = 'FA' if facil_acesso else ''
                grupo['Regra'] = valor_regra
        
        pd.DataFrame(self.grupos).to_excel("data/grupos.xlsx", index=False)
        self.regras_df.to_excel("data/regras.xlsx", index=False)
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n--- Grupo {grupo_id} editado com sucesso ---")
        time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
        self.carregar_grupos()
    except ValueError:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Grupo {grupo_id} não encontrado.")
        time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
        return

def excluir_grupo_modified(self):
    self.visualizar_grupos()
    try:
        grupo_id = int(input("\nDigite o ID do grupo que deseja excluir: "))
        if not any(g['ID do Grupo'] == grupo_id for g in self.grupos):
            raise ValueError
        
        # Removendo o ID do grupo das regras associadas
        for index, row in self.regras_df.iterrows():
            existing_groups = str(row['Grupo']).split(", ")
            if str(grupo_id) in existing_groups:
                existing_groups.remove(str(grupo_id))
                self.regras_df.at[index, 'Grupo'] = ", ".join(existing_groups)
        
        # Excluindo o grupo
        self.grupos = [g for g in self.grupos if g["ID do Grupo"] != grupo_id]
        
        pd.DataFrame(self.grupos).to_excel("data/grupos.xlsx", index=False)
        self.regras_df.to_excel("data/regras.xlsx", index=False)
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n*** Grupo {grupo_id} excluído com sucesso! ***")
        time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
        self.carregar_grupos()
    except ValueError:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Grupo {grupo_id} não encontrado.")
        time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
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
            os.system('cls' if os.name == 'nt' else 'clear')
            print("### Nenhum grupo foi criado ainda ###")
            time.sleep(2)
            os.system('cls' if os.name == 'nt' else 'clear')
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
                os.system('cls' if os.name == 'nt' else 'clear')
                self.visualizar_grupos()
            elif escolha == '2':
                os.system('cls' if os.name == 'nt' else 'clear')
                self.criar_grupo()
            elif escolha == '3':
                os.system('cls' if os.name == 'nt' else 'clear')
                self.editar_grupo()
            elif escolha == '4':
                os.system('cls' if os.name == 'nt' else 'clear')
                self.excluir_grupo()
            elif escolha == '5':
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Saindo...")
                time.sleep(2)    
                break
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("\n--- Opção inválida! Tente novamente ---")

if __name__ == "__main__":
    cli = GruposRegrasCLI()
    cli.menu()
