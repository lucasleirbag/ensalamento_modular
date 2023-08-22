from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QComboBox, QLineEdit, QCompleter)
from PyQt5.QtCore import Qt
import pandas as pd

# Carregar os dados das planilhas
planilha_2 = pd.read_excel("data/planilha_2.xlsx")
planilha_3 = pd.read_excel("data/planilha_3.xlsx")

class EnsalamentoApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # Layout principal
        self.layout = QVBoxLayout()
        
        # Adicionar os campos de entrada inicialmente
        self.add_rule_fields()
        
        # Botão para adicionar mais campos
        self.add_btn = QPushButton("+", self)
        self.add_btn.clicked.connect(self.add_rule_fields)
        
        # Botão para remover campos
        self.remove_btn = QPushButton("-", self)
        self.remove_btn.clicked.connect(self.remove_rule_fields)
        
        # Adicionando os botões ao layout principal
        self.layout.addWidget(self.add_btn)
        self.layout.addWidget(self.remove_btn)
        
        self.setLayout(self.layout)
        
    def add_rule_fields(self):
        # Criando um layout horizontal para cada conjunto de campos de regra
        h_layout = QHBoxLayout()
        
        # Perfil
        perfil_combo = QComboBox(self)
        perfil_combo.addItems(planilha_2["Participante"].tolist())
        h_layout.addWidget(perfil_combo)
        
        # Recurso
        recurso_combo = QComboBox(self)
        recurso_combo.addItems(planilha_3["Recurso"].tolist())
        h_layout.addWidget(recurso_combo)
        
        # Junção Perfil
        juncao_edit = QLineEdit(self)
        juncao_completer = QCompleter(planilha_2["Participante"].tolist(), self)
        juncao_edit.setCompleter(juncao_completer)
        h_layout.addWidget(juncao_edit)
        
        # FA
        fa_combo = QComboBox(self)
        fa_combo.addItems(["", "FA"])
        h_layout.addWidget(fa_combo)
        
        # Qtd Max
        qtd_max_edit = QLineEdit(self)
        h_layout.addWidget(qtd_max_edit)
        
        self.layout.insertLayout(self.layout.count() - 2, h_layout)
        
    def remove_rule_fields(self):
        if self.layout.count() > 2:  # Deve haver pelo menos um conjunto de campos
            item = self.layout.takeAt(self.layout.count() - 3)
            while item.count():
                sub_item = item.takeAt(0)
                widget = sub_item.widget()
                if widget is not None:
                    widget.deleteLater()
            del item

app = QApplication([])
window = EnsalamentoApp()
window.show()
app.exec_()
