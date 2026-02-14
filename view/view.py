from PySide6.QtWidgets import (QApplication, QMainWindow, 
                                QFrame, QLabel, QTableView,
                                QVBoxLayout, QHBoxLayout,
                                QHeaderView, QLineEdit,
                                QPushButton, QGridLayout)
from PySide6.QtCore import Qt
from view.table_model.table_model import TableClass
from view.instancias.instances import *
import sys

app = QApplication(sys.argv)

class TelaPrincipal(QMainWindow):
    def __init__(self):
        self.estoque = estoque_controller
        self.dados = self.estoque.buscar_todos()
        super().__init__()

        self.setWindowTitle('Estoque — Buscar Todos')

        estilo_total = """
    /* 1. Cor das Células (dados) */
    QTableView {
        background-color: #D9D9D9; /* Fundo branco para os dados */
        color: #585858;             /* Letra escura para os dados */
        gridline-color: #BDBDBD;    /* Cor das linhas da grade */
    }

    /* 2. Cor dos Cabeçalhos (Topo e Lateral) */
    QHeaderView::section {
        background-color: #BDBDBD; /* Cor escura para os headers */
        color: #585858;              /* Letra branca para os headers */
        padding: 4px;
        border: 1px solid #BDBDBD;
        font-weight: bold;
    }

    /* 3. Cor do Botão do Canto (Onde os headers se cruzam) */
    QTableView QTableCornerButton::section {
        background-color: #BDBDBD;
        border: 1px solid #BDBDBD;
    }
"""

        self.barra_estoque = self.barra_menu('Estoque')
        self.submenu = self.gerar_submenu(self.barra_estoque, ['Adicionar Produto', 'Atualizar Produto', 'Remover Produto'])

        self.barra_produto = self.barra_menu('Produto')
        self.submenu = self.gerar_submenu(self.barra_produto, ['Criar Produto', 'Atualizar Produto', 'Remover Produto', 'Buscar Todos'])

        self.barra_categoria = self.barra_menu('Categoria')
        self.submenu = self.gerar_submenu(self.barra_categoria, ['Criar Categoria', 'Atualizar Categoria', 'Remover Categoria', 'Buscar Todos'])


        self.barra_movimentacao = self.barra_menu('Movimentacao')
        self.submenu = self.gerar_submenu(self.barra_movimentacao, ['Filtrar'])


        #definicoes do frame da metade de cima
        self.frame_cima_fora = QFrame()
        self.frame_cima_fora.setStyleSheet('background-color: #D9D9D9;')
        self.frame_cima_fora.setContentsMargins(0, 0, 0, 0)


        self.entrada_nome = self.criar_campos('Pesquisar por Nome do Produto:')
        self.entrada_marca = self.criar_campos('Pesquisar por Marca do Produto:')
        self.entrada_categoria = self.criar_campos('Pesquisar por Categoria do Produto:')
        self.entrada_sku = self.criar_campos('Pesquisa por SKU do Produto:')
        self.entrada_valor_unitario = self.criar_campos('Pesquisar por Valor Unitário do Produto:')
        self.entrada_quantidade = self.criar_campos('Pesquisar por Quantidade do Produto:')
        self.entrada_estoque_minimo = self.criar_campos('Pesquisar por Estoque Mínimo do Produto:')

            #borda do campo de pesquisa
        self.campo_nome = self.adicionar_bordas(self.entrada_nome)
        self.campo_marca = self.adicionar_bordas(self.entrada_marca)
        self.campo_categoria = self.adicionar_bordas(self.entrada_categoria)
        self.campo_sku = self.adicionar_bordas(self.entrada_sku)
        self.campo_valor_unitario = self.adicionar_bordas(self.entrada_valor_unitario)
        self.campo_quantidae = self.adicionar_bordas(self.entrada_quantidade)
        self.campo_estoque_minimo = self.adicionar_bordas(self.entrada_estoque_minimo)

        #define botao
        self.botao_estoque = self.definir_botao('PESQUISAR', self.filtrar)

        #adiciona o campo a grid
        self.grid = QGridLayout(self.frame_cima_fora)
        self.grid.setContentsMargins(0, 100, 0, 150)
        self.grid.addWidget(self.botao_estoque, 4, 1, 3, 3)
        
        self.posicionar_campo('nome', self.campo_nome, 0, 0, 1, 0)
        self.posicionar_campo('marca', self.campo_marca, 0, 1, 1, 1)
        self.posicionar_campo('categoria', self.campo_categoria, 0, 2, 1, 2)

        self.posicionar_campo('SKU', self.campo_sku, 2, 0, 3, 0)
        self.posicionar_campo('valor unitário', self.campo_valor_unitario, 2, 1, 3, 1)
        self.posicionar_campo('quantidade', self.campo_quantidae, 2, 2, 3, 2)

        self.posicionar_campo('estoque mínimo', self.campo_estoque_minimo, 4, 0, 5, 0)

        self.frame_cima_fora.setMinimumSize(1080, 720)

        #definicoes da tabela
        self.tabela_model = TableClass(self.dados)
    
        self.tabela_view = QTableView()
        self.tabela_view.setModel(self.tabela_model)
        self.tabela_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela_view.setStyleSheet(estilo_total)
        self.tabela_view.setMinimumHeight(300)
        self.tabela_view.horizontalHeader().setStretchLastSection(True)
        self.tabela_view.verticalHeader().setDefaultAlignment(Qt.AlignCenter)

        self.frame_tabela = QFrame()
        self.frame_tabela.setStyleSheet('background-color: #BDBDBD;')

        self.layout_tabela = QVBoxLayout(self.frame_tabela)
        self.layout_tabela.addWidget(self.tabela_view)
        self.layout_tabela.setContentsMargins(10, 10, 10, 10)

        #definicoes do frame central
        self.frame_central = QFrame()
        self.frame_central.setStyleSheet('background-color: #D9D9D9;')
        self.frame_central.setMinimumSize(1440, 900)
        self.setCentralWidget(self.frame_central)

        self.layout_central = QVBoxLayout(self.frame_central)
        self.layout_central.addWidget(self.frame_cima_fora, alignment=Qt.AlignCenter)
        self.layout_central.addWidget(self.frame_tabela)
        self.layout_central.setContentsMargins(10, 10, 10, 10)
        self.layout_central.setStretch(0, 1)
        self.layout_central.setStretch(1, 1)
        
    def filtrar(self):
        dado_recebido = {}
        dado_recebido['nome'] = self.entrada_nome.text()
        dado_recebido['marca'] = self.entrada_marca.text()
        dado_recebido['categoria'] = self.entrada_categoria.text()
        dado_recebido['sku'] = self.entrada_sku.text()
        dado_recebido['valor_unitario'] = self.entrada_valor_unitario.text()
        dado_recebido['quantidade'] = self.entrada_quantidade.text()
        dado_recebido['estoque_minimo'] = self.entrada_estoque_minimo.text()

        dado_recebido_copy = dado_recebido.copy()

        for i in dado_recebido:
            if not dado_recebido[i]:
                dado_recebido_copy.pop(i)

        dados = self.estoque.filtrar(**dado_recebido_copy)
        self.tabela_model.atualizar_dados_model(dados)

        self.entrada_nome.clear()
        self.entrada_marca.clear()
        self.entrada_categoria.clear()
        self.entrada_sku.clear()
        self.entrada_valor_unitario.clear()
        self.entrada_quantidade.clear()
        self.entrada_estoque_minimo.clear()
        
    def adicionar_bordas(self, entrada):
        frame_borda = QFrame()
        frame_borda.setStyleSheet('background-color: #BDBDBD;')
        frame_borda.setMaximumHeight(35)
        
        layout_borda = QVBoxLayout(frame_borda)
        layout_borda.addWidget(entrada)
        layout_borda.setContentsMargins(5, 5, 5, 5)
        return frame_borda
    
    def criar_campos(self, placeholder):
        self.entrada = QLineEdit()
        self.entrada.setPlaceholderText(placeholder)
        self.entrada.setStyleSheet(''' QLineEdit {
                              background-color: #D9D9D9; color: #585858; font-size: 15px;
                              border-radius: none;
                              }
                              QLineEdit::focus {
                              border-bottom: 1px solid #909090;
                              }''')
        self.entrada.setMaximumHeight(30)
        return self.entrada

    def posicionar_campo(self, nome_campo, campo, row_nome_campo, column_nome_campo, row_campo, column_campo):
        texto = QLabel(f'{nome_campo}:'.capitalize())
        texto.setStyleSheet('color: #686868; font-weight: bold; font-family: Arial, sans-serif; font-size: 13px;')
        texto.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(texto, row_nome_campo, column_nome_campo)
        self.grid.addWidget(campo, row_campo, column_campo)

    def barra_menu(self, nome_menu):
        barra_menu = self.menuBar()
        novo_menu = barra_menu.addMenu(nome_menu)
        barra_menu.setCursor(Qt.PointingHandCursor)
        barra_menu.setStyleSheet('''
                                    QMenuBar {
                                        background-color: #BDBDBD;
                                        color: #585858;
                                        font-size: 14px;
                                 }

                                    QMenuBar::item {
                                        padding: 6px 12px;
                                        margin: 0px;
                                        border-right: 1px solid #585858;
                                        border-bottom: 1px solid #585858;
                                 }    

                                    QMenuBar::item:selected {
                                        background-color: #C9C9C9;
                                 }

                                    QMenu {
                                        background-color: #BDBDBD;
                                    color: #585858;
                                    margin: 0px;
                                    min-width: 100px;
                                 }

                                    QMenu::item {
                                        margin: 0px;
                                        padding: 12px 12px;
                                 }

                                    QMenu::item:selected {
                                        background-color: #D9D9D9;
                                 }
                                ''')
        return novo_menu

    def gerar_submenu(self,menu, itens=list):
        setor = menu.title()

        for i in itens:
            submenu = menu.addAction(i)
            menu.addSeparator()
            a = submenu.triggered.connect(lambda checked=False, setor=setor, nome=i: self.navegar(setor, nome))
          
    def navegar(self, setor, destino):
        if setor == 'Estoque':
            if destino == 'Adicionar Produto':
                from view.view import TelaAdicionarProdutoEstoque, TelaPrincipal
                tela_principal = TelaPrincipal()
                self.tela = TelaAdicionarProdutoEstoque(tela_principal)
                self.tela.show()

    def definir_botao(self, texto, funcao=None):
        botao_pesquisar = QPushButton(texto)
        botao_pesquisar.setStyleSheet('''
                                        QPushButton {
                                            background-color: #BDBDBD; color: #585858; font-size: 15px;
                                      }

                                        QPushButton:pressed {
                                            background-color: #C0C0C0;
                                      }
                                        ''')
        botao_pesquisar.setCursor(Qt.PointingHandCursor)
        botao_pesquisar.setMinimumHeight(40)
        botao_pesquisar.setMinimumWidth(200)
        if funcao != None:
            botao_pesquisar.clicked.connect(funcao)
        return botao_pesquisar

class TelaAdicionarProdutoEstoque(QFrame):
    def __init__(self, tela_principal):
        self.tela_principal = tela_principal
        super().__init__()
        self.setWindowTitle('Adicionar Produto — Estoque')

        dados = produto_controller.buscar_todos()
        model = TableClass(dados)

        self.frame_botoes = QFrame()
        
        self.frame_botoes.setMaximumHeight(50)
        self.frame_botoes.setStyleSheet('background-color: #D9D9D9;')

        self.botao_adicionar = self.tela_principal.definir_botao('ADICIONAR PRODUTO')
        self.botao_atualizar = self.tela_principal.definir_botao('ATUALIZAR PRODUTO')
        self.botao_remover = self.tela_principal.definir_botao('REMOVER PRODUTO')

        self.layout_botoes = QHBoxLayout(self.frame_botoes)
        self.layout_botoes.addWidget(self.botao_adicionar)
        self.layout_botoes.addWidget(self.botao_atualizar)
        self.layout_botoes.addWidget(self.botao_remover)

        self.tabela_view = QTableView()
        self.tabela_view.setModel(model)
        self.tabela_view.setContentsMargins(0, 0, 0, 0)
        self.tabela_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela_view.setStyleSheet("""
                                            QTableView {
                                                background-color: #D9D9D9;
                                                color: #585858;        
                                                gridline-color: #BDBDBD;
                                            }

                                            QHeaderView::section {
                                                background-color: #BDBDBD; 
                                                color: #585858;             
                                                padding: 4px;
                                                border: 1px solid #BDBDBD;
                                                font-weight: bold;
                                            }

                                            QTableView QTableCornerButton::section {
                                                background-color: #BDBDBD;
                                                border: 1px solid #BDBDBD;
                                            }
                                       """)
        
        self.frame_tabela = QFrame()
        self.frame_tabela .setStyleSheet('background-color: #BDBDBD;')
        self.frame_tabela.setContentsMargins(0, 0, 0, 0)

        self.layout_tabela = QVBoxLayout(self.frame_tabela)
        self.layout_tabela.setContentsMargins(10, 10, 10, 10)
        self.layout_tabela.addWidget(self.tabela_view)

        self.grid = QGridLayout(self.tabela_view)
        self.grid.setSpacing(0)
        self.grid.setContentsMargins(0, 0, 0, 0)
        
        self._layout = QVBoxLayout(self)
        self._layout.addWidget(self.frame_botoes)
        self._layout.addWidget(self.frame_tabela)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._layout.setStretch(0, 1)
        self._layout.setStretch(1, 1)
        
        self.setMinimumSize(900, 600)
        self.setContentsMargins(10, 10, 10, 10)
        self.setStyleSheet('background-color: #D9D9D9; ')


a = TelaPrincipal()

a.show()
sys.exit(app.exec())