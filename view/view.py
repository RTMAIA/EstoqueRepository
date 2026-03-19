from PySide6.QtWidgets import (QApplication, QMainWindow, 
                                QFrame, QLabel, QTableView,
                                QVBoxLayout, QHBoxLayout,
                                QHeaderView, QLineEdit,
                                QPushButton, QGridLayout,
                                QAbstractItemView, QDialog,
                                QMessageBox, QComboBox)
from PySide6.QtCore import Qt
from view.table_model.table_model import TableClass, TableEditableClass
from view.instancias import instances
from view.style import style
from view.validators_view.validators_view import NumDelegateOnly, IntValidation
from decimal import Decimal
import sys

app = QApplication(sys.argv)
app.setStyle('Fusion')

class TelaPrincipal(QMainWindow):
    def __init__(self, estoque_controller, produto_controller, categoria_controller):
        self.produto_controller = produto_controller
        self.estoque_controller = estoque_controller
        self.categoria_controller = categoria_controller
        self.dados = self.estoque_controller.buscar_todos()
        self.dados_id = {}
        super().__init__()

        self.setWindowTitle('Estoque — Buscar Todos')

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
        self.frame_cima_fora.setStyleSheet(style.cor_fundo)
        self.frame_cima_fora.setContentsMargins(0, 0, 0, 0)

        self.entrada_nome = self.criar_campos('Pesquisar por Nome do Produto...')
        self.entrada_marca = self.criar_campos('Pesquisar por Marca do Produto...')
        self.entrada_categoria = self.criar_campos('Pesquisar por Categoria do Produto...')
        self.entrada_sku = self.criar_campos('Pesquisa por SKU do Produto...')
        self.entrada_valor_unitario = self.criar_campos('Pesquisar por Valor Unitário do Produto...')
        self.entrada_quantidade = self.criar_campos('Pesquisar por Quantidade do Produto...')
        self.entrada_estoque_minimo = self.criar_campos('Pesquisar por Estoque Mínimo do Produto...')

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
        
        self.posicionar_campo(self.grid, 'nome', self.campo_nome, 0, 0, 1, 0)
        self.posicionar_campo(self.grid, 'marca', self.campo_marca, 0, 1, 1, 1)
        self.posicionar_campo(self.grid, 'categoria', self.campo_categoria, 0, 2, 1, 2)

        self.posicionar_campo(self.grid, 'SKU', self.campo_sku, 2, 0, 3, 0)
        self.posicionar_campo(self.grid, 'valor unitário', self.campo_valor_unitario, 2, 1, 3, 1)
        self.posicionar_campo(self.grid, 'quantidade', self.campo_quantidae, 2, 2, 3, 2)

        self.posicionar_campo(self.grid, 'estoque mínimo', self.campo_estoque_minimo, 4, 0, 5, 0)

        self.frame_cima_fora.setMinimumSize(1080, 720)

        #definicoes da tabela
        self.tabela_model = TableClass(self.dados)
    
        self.tabela_view = QTableView()
        self.tabela_view.setModel(self.tabela_model)
        self.tabela_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela_view.setStyleSheet(style.estilo_tabela)
        self.tabela_view.setMinimumHeight(300)
        self.tabela_view.horizontalHeader().setStretchLastSection(True)
        self.tabela_view.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.tabela_view.hideColumn(0)

        self.frame_tabela = QFrame()
        self.frame_tabela.setStyleSheet(style.cor_secundaria)

        self.layout_tabela = QVBoxLayout(self.frame_tabela)
        self.layout_tabela.addWidget(self.tabela_view)
        self.layout_tabela.setContentsMargins(10, 10, 10, 10)

        #definicoes do frame central
        self.frame_central = QFrame()
        self.frame_central.setStyleSheet(style.cor_fundo)
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

        dados = self.estoque_controller.filtrar(**dado_recebido_copy)
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
        frame_borda.setStyleSheet(style.cor_secundaria)
        frame_borda.setMaximumHeight(35)
        
        layout_borda = QVBoxLayout(frame_borda)
        layout_borda.addWidget(entrada)
        layout_borda.setContentsMargins(5, 5, 5, 5)
        return frame_borda
    
    def criar_campos(self, placeholder):
        self.entrada = QLineEdit()
        self.entrada.setPlaceholderText(placeholder)
        self.entrada.setStyleSheet(style.estilo_qline_edit)
        self.entrada.setMaximumHeight(30)
        return self.entrada

    def posicionar_campo(self, layout, nome_campo, campo, row_nome_campo, column_nome_campo, row_campo, column_campo):
        texto = QLabel(f'{nome_campo}:'.capitalize())
        texto.setStyleSheet(style.cor_texto_campos)
        texto.setAlignment(Qt.AlignCenter)
        layout.addWidget(texto, row_nome_campo, column_nome_campo)
        layout.addWidget(campo, row_campo, column_campo)

    def barra_menu(self, nome_menu):
        barra_menu = self.menuBar()
        novo_menu = barra_menu.addMenu(nome_menu)
        barra_menu.setCursor(Qt.PointingHandCursor)
        barra_menu.setStyleSheet(style.estilo_menu)
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
                self.tela_adicionar_produto_estoque = SubMenuEstoqueAdicionarProduto(self, self.produto_controller)
                self.tela_adicionar_produto_estoque.show()
            if destino == 'Atualizar Produto':
                self.tela_atualizar_produto_estoque = SubMenuEstoqueAtualizarProduto(self)
                self.tela_atualizar_produto_estoque.show()
            if destino == 'Remover Produto':
                self.tela_remover_produto_estoque = SubMenuEstoqueRemoverProduto(self)
                self.tela_remover_produto_estoque.show()
        if setor == 'Produto':
            if destino == 'Criar Produto':
                self.tela_criar_produto = SubMenuProdutoCriarProduto(self, self.categoria_controller)
                self.tela_criar_produto.show()

    def definir_botao(self, texto, funcao=None):
        botao_pesquisar = QPushButton(texto)
        botao_pesquisar.setStyleSheet(style.estilo_botao)
        botao_pesquisar.setCursor(Qt.PointingHandCursor)
        botao_pesquisar.setMinimumHeight(40)
        botao_pesquisar.setMinimumWidth(200)
        if funcao != None:
            botao_pesquisar.clicked.connect(funcao)
        return botao_pesquisar

    def tela_pegar_id(self, title, nome_botao, dado, funcao):
        self.tela = QFrame()
        self.tela.setWindowTitle(title)

        self.model = TableClass(dado)

        self.frame_botoes = QFrame()
        
        self.frame_botoes.setMaximumHeight(50)
        self.frame_botoes.setStyleSheet(style.cor_fundo)

        self.botao_adicionar = self.definir_botao(nome_botao, funcao)

        self.layout_botoes = QHBoxLayout(self.frame_botoes)
        self.layout_botoes.addWidget(self.botao_adicionar)

        self.tabela_view = self.criar_tabela(self.model)
        self.tabela_view.hideColumn(0)

        self.frame_tabela = QFrame()
        self.frame_tabela .setStyleSheet(style.cor_secundaria)
        self.frame_tabela.setContentsMargins(0, 0, 0, 0)

        self.layout_tabela = QVBoxLayout(self.frame_tabela)
        self.layout_tabela.setContentsMargins(10, 10, 10, 10)
        self.layout_tabela.addWidget(self.tabela_view)

        self.grid = QGridLayout(self.tabela_view)
        self.grid.setSpacing(0)
        self.grid.setContentsMargins(0, 0, 0, 0)
        
        self.tela_layout = QVBoxLayout(self.tela)
        self.tela_layout.addWidget(self.frame_botoes)
        self.tela_layout.addWidget(self.frame_tabela)
        self.tela_layout.setContentsMargins(0, 0, 0, 0)
        self.tela_layout.setSpacing(0)
        self.tela_layout.setStretch(0, 1)
        self.tela_layout.setStretch(1, 1)
        
        self.tela.setMinimumSize(1000, 600)
        self.tela.setContentsMargins(0, 0, 0, 0)
        self.tela.setStyleSheet(style.cor_fundo)
        return self.tela

    def pegar_dados_linha(self, index):
        linha = index.row()
        self.data = self.model.retornar_data()
        dados_linha = self.data[0][linha]
        self.dados_id['id_produto'] = dados_linha[0]

    def criar_tabela(self, model):
        tabela_view = QTableView()
        tabela_view.setModel(model)
        tabela_view.setContentsMargins(0, 0, 0, 0)
        tabela_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tabela_view.setStyleSheet(style.estilo_tabela)
        tabela_view.setProperty('show-decoration-selected', True)
        tabela_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        tabela_view.setSelectionMode(QAbstractItemView.SingleSelection)
        tabela_view.clicked.connect(self.pegar_dados_linha)

        return tabela_view

    def msg(self, titulo, texto, icon):
            icone = {'warning': QMessageBox.Icon.Warning, 'information': QMessageBox.Icon.Information}
            msg = QMessageBox()
            msg.setIcon(icone[icon])
            msg.setWindowTitle(titulo)
            msg.setText(str(texto))
            if icon == 'warning':
                msg.setStyleSheet(style.estilo_messagebox_warning)
            else:
                msg.setStyleSheet(style.estilo_messagebox_information)
            msg.exec()

    def tela_confirmacao(self):
        if self.dados_id:
            self.confirmacao = QMessageBox()
            self.confirmacao.setWindowTitle('Confirmação')
            self.confirmacao.setText('Você realmente deseja remover esse item?')
            self.confirmacao.setIcon(QMessageBox.Icon.Question)

            self.botao_sim = self.confirmacao.addButton('Sim', QMessageBox.YesRole)
            self.botao_nao = self.confirmacao.addButton('Não', QMessageBox.NoRole)

            self.confirmacao.setMinimumSize(500, 600)
            self.confirmacao.setStyleSheet(style.estilo_messagebox_information)

            self.confirmacao.exec()

            if self.confirmacao.clickedButton() == self.botao_sim:
                return True
            return

class SubMenuEstoqueAdicionarProduto(QFrame):
    def __init__(self, tela_principal, produto_controller):
        self.tela_principal = tela_principal
        self.produto_controller = produto_controller
        super().__init__()
        self.dados_produtos = self.produto_controller.buscar_todos()
        self.tela_adicionar = self.tela_principal.tela_pegar_id('Estoque — Adicionar Produto', 'ADICIONAR AO ESTOQUE', self.dados_produtos, self.adicionar_produto)
        
        self._layout = QVBoxLayout(self)
        self._layout.addWidget(self.tela_adicionar)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self.setWindowTitle('Estoque — Adicionar ao Estoque')
        self.setMinimumSize(900, 600)
        self.setContentsMargins(10, 10, 10, 10)
        self.setStyleSheet(style.cor_fundo)

    def tela_concluir_produto_estoque(self):
        self.tela_dados = QDialog()
        self.tela_dados.setWindowTitle('Estoque — Adicionar Produto')
        self.tela_dados.setStyleSheet(style.cor_fundo)

        frame = QFrame()
        frame.setContentsMargins(0, 0, 0, 0)

        frame_botao = QFrame()

        self.botao_ok = self.tela_principal.definir_botao('OK', self.pegar_dado_tela)

        self.botao_cancel = self.tela_principal.definir_botao('CANCEL', self.limpar_e_fechar)

        layout_frame_botao =  QHBoxLayout(frame_botao)
        layout_frame_botao.addWidget(self.botao_ok)
        layout_frame_botao.addWidget(self.botao_cancel)

        grid = QGridLayout(frame)

        self.entrada_quantidade = self.tela_principal.criar_campos('Digite a quantidade: ')
        self.entrada_estoque_minimo = self.tela_principal.criar_campos('Digite o estoque minimo: ')
        self.entrada_quantidade.setValidator(IntValidation.validate())
        self.entrada_estoque_minimo.setValidator(IntValidation.validate())

        campo_quantidade = self.tela_principal.adicionar_bordas(self.entrada_quantidade)
        campo_estoque_minimo = self.tela_principal.adicionar_bordas(self.entrada_estoque_minimo)

        self.tela_principal.posicionar_campo(grid, 'Quantidade', campo_quantidade, 0, 0, 1, 0)
        self.tela_principal.posicionar_campo(grid, 'Estoque Minimo', campo_estoque_minimo, 0, 1, 1, 1)

        grid.addWidget(campo_quantidade)
        grid.addWidget(campo_estoque_minimo)

        layout_frame = QVBoxLayout(self.tela_dados)
        layout_frame.addWidget(frame)
        layout_frame.addWidget(frame_botao)

        self.tela_dados.setFixedSize(450, 200)
        self.tela_dados.exec()

    def limpar_e_fechar(self):
        self.entrada_quantidade.clear()
        self.entrada_estoque_minimo.clear()
        self.tela_principal.dados_id.clear()
        self.tela_dados.close()
        return

    def pegar_dado_tela(self):
        try:
                if not self.entrada_quantidade.text().strip() or not self.entrada_estoque_minimo.text().strip():
                    self.tela_principal.msg('Aviso', 'Os campos não podem estar vazios.', 'warning')
                    return
                if not self.entrada_quantidade.text().isdigit() and not self.entrada_estoque_minimo.text().isdigit():
                    raise ValueError('O campo não pode conter letras.')
                self.tela_principal.dados_id['quantidade'] = int(self.entrada_quantidade.text())
                self.tela_principal.dados_id['estoque_minimo'] = int(self.entrada_estoque_minimo.text())
                self.tela_dados.accept()
        except Exception as e:
            self.tela_principal.msg('Error', e, 'warning')

    def adicionar_produto(self):
        try:
            if self.tela_principal.dados_id:
                self.tela_concluir_produto_estoque()
                if len(self.tela_principal.dados_id) == 3:
                    self.tela_principal.estoque_controller.adicionar_produto_estoque(**self.tela_principal.dados_id)
                    dados_novos = self.tela_principal.estoque_controller.buscar_todos()
                    self.tela_principal.tabela_model.atualizar_dados_model(dados_novos)
                    self.tela_principal.msg('Sucesso!', 'Produto Adicionado ao Estoque!', 'information')
                    self.tela_principal.dados_id.clear()
                    return
                return
        except Exception as e:
            self.tela_principal.dados_id.clear()
            self.tela_principal.msg('Error', e, 'warning')
            return

class SubMenuEstoqueAtualizarProduto(QFrame):
    def __init__(self, tela_principal):
        self.tela_principal = tela_principal
        super().__init__()
        self.dados_estoque = tela_principal.estoque_controller.buscar_todos()
        self.tela_atualizar = self.tela_principal.tela_pegar_id('Estoque — Atualizar Produto no Estoque', 'ATUALIZAR ESTOQUE', self.dados_estoque, self.tela_ajustar_estoque)

        self._layout = QVBoxLayout(self)
        self._layout.addWidget(self.tela_atualizar)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self.setWindowTitle('Estoque — Atualizar Produto no Estoque')
        self.setMinimumSize(1000, 600)
        self.setContentsMargins(10, 10, 10, 10)
        self.setStyleSheet(style.cor_fundo)

    def tela_ajustar_estoque(self):
        if self.tela_principal.dados_id:
            self.id = self.tela_principal.dados_id['id_produto']
            self.dados = self.tela_principal.estoque_controller.buscar_por_id(self.id)

            self.tela_ajustar = QDialog()
            self.tela_ajustar.setWindowTitle('Estoque — Ajustar Estoque')
            self.tela_ajustar.setFixedSize(1000, 500)
            
            self.frame_cima = QFrame()
            self.frame_cima.setStyleSheet(style.cor_fundo)
            self.frame_cima.setContentsMargins(0, 0, 0, 0)
            self.frame_cima.setFixedHeight(100)

            self.frame_baixo = QFrame()
            self.frame_baixo.setStyleSheet(style.cor_secundaria)
            self.frame_baixo.setContentsMargins(0, 0, 0, 0)

            self.tabela_model = TableEditableClass(self.dados)

            self.botao_ok = self.tela_principal.definir_botao('OK', self.ajustar_estoque)
            self.botao_cancel = self.tela_principal.definir_botao('CANCEL', self.tela_ajustar.close)

            self.delegate_num = NumDelegateOnly()

            self.tabela_view = self.tela_principal.criar_tabela(self.tabela_model)
            self.tabela_view.setItemDelegateForColumn(5, self.delegate_num)
            self.tabela_view.setItemDelegateForColumn(6, self.delegate_num)
            self.tabela_view.hideColumn(0)

            self.layout_frame_cima = QHBoxLayout(self.frame_cima)
            self.layout_frame_cima.addWidget(self.botao_ok)
            self.layout_frame_cima.addWidget(self.botao_cancel)

            self.layout_frame_baixo = QVBoxLayout(self.frame_baixo)
            self.layout_frame_baixo.addWidget(self.tabela_view)
            self.layout_frame_baixo.setContentsMargins(10, 10, 10, 10)

            self.layout_principal = QVBoxLayout(self.tela_ajustar)
            self.layout_principal.addWidget(self.frame_cima)
            self.layout_principal.addWidget(self.frame_baixo)
            self.layout_principal.setSpacing(0)

            self.grid = QGridLayout(self.tabela_view)
            self.grid.setContentsMargins(0, 0, 0, 0)

            self.tela_ajustar.exec()

    def ajustar_estoque(self):
        try:
            dado_model = self.tabela_model.retornar_data()
            if dado_model:
                self.tela_principal.estoque_controller.ajustar_produto(self.id, **dado_model)
                dados_novos = self.tela_principal.estoque_controller.buscar_todos()
                self.tela_principal.tabela_model.atualizar_dados_model(dados_novos)
                self.tela_principal.msg('Success', 'Estoque ajustado com sucesso!', 'information')
                self.tela_ajustar.close()
        except Exception as e:
            self.tela_principal.msg('Error', e, 'warning')

class SubMenuEstoqueRemoverProduto(QFrame):
    def __init__(self,tela_principal):
        self.tela_principal = tela_principal
        super().__init__()
        self.dados_estoque = self.tela_principal.estoque_controller.buscar_todos()
        self.tela_deletar = self.tela_principal.tela_pegar_id('Estoque — Remover Produto do Estoque', 'REMOVER PRODUTO', self.dados_estoque, self.remover_produto)

        self._layout = QVBoxLayout(self)
        self._layout.addWidget(self.tela_deletar)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self.setWindowTitle('Estoque — Remover Produto do Estoque')
        self.setMinimumSize(1000, 600)
        self.setContentsMargins(10, 10, 10, 10)
        self.setStyleSheet(style.cor_fundo)

    def remover_produto(self):
        try:
            if not self.tela_principal.tela_confirmacao():
                return
            self.id = self.tela_principal.dados_id['id_produto']
            self.info = self.tela_principal.estoque_controller.delete(self.id)
            novos_dados = self.tela_principal.estoque_controller.buscar_todos()
            self.tela_principal.tabela_model.atualizar_dados_model(novos_dados)
            self.tela_principal.msg('Sucess', self.info, 'information')
            self.tela_principal.dados_id.clear()
        except Exception as e:
            self.tela_principal.msg('Error', e, 'warning')

class SubMenuProdutoCriarProduto(QFrame):
    def __init__(self, tela_principal, categoria_controller):
        self.tela_principal = tela_principal
        self.categoria_controller = categoria_controller
        super().__init__()
        self.dados_produto = self.tela_principal.produto_controller.buscar_todos()

        self.campo_nome = self.tela_principal.criar_campos('Digite o nome do produto...')
        self.campo_marca = self.tela_principal.criar_campos('Digite a marca do produto...')
        self.campo_valor_unitario = self.tela_principal.criar_campos('Digite o valor unitário do produto...')
        self.campo_valor_unitario.setValidator(IntValidation.validate())
        self.menu_suspenso_categoria = self.criar_menu_suspenso()

        self.campo_nome_borda = self.tela_principal.adicionar_bordas(self.campo_nome)
        self.campo_marca_borda = self.tela_principal.adicionar_bordas(self.campo_marca)
        self.campo_valor_unitario_borda = self.tela_principal.adicionar_bordas(self.campo_valor_unitario)
        self.menu_suspenso_categoria_borda = self.tela_principal.adicionar_bordas(self.menu_suspenso_categoria)

        self.botao_enviar = self.tela_principal.definir_botao('CRIAR PRODUTO', self.criar_produto)

        self.frame_fora = QFrame()
        self.frame_fora.setStyleSheet(style.cor_secundaria)
        self.frame_fora.setMinimumSize(630, 410)

        self.frame_dentro = QFrame()
        self.frame_dentro.setStyleSheet(style.cor_fundo)
        self.frame_dentro.setContentsMargins(10, 10, 10, 10)
        self.frame_dentro.setMinimumSize(640, 420)

        self.grid = QGridLayout(self.frame_dentro)
        self.grid.setContentsMargins(0, 100, 0 ,150)

        tela_principal.posicionar_campo(self.grid, 'nome', self.campo_nome_borda, 0, 0, 1, 0)
        tela_principal.posicionar_campo(self.grid, 'marca', self.campo_marca_borda, 0, 1, 1, 1)
        tela_principal.posicionar_campo(self.grid, 'valor Unitário', self.campo_valor_unitario_borda, 2, 0, 3, 0)
        self.grid.addWidget(self.menu_suspenso_categoria, 3, 1)
        self.grid.addWidget(self.botao_enviar, 4, 0, 5, 0)

        self.layout_frame_fora = QVBoxLayout(self.frame_fora)
        self.layout_frame_fora.addWidget(self.frame_dentro, alignment=Qt.AlignCenter)

        self._layout = QVBoxLayout(self)
        self._layout.addWidget(self.frame_fora, alignment=Qt.AlignCenter)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self.setWindowTitle('Produtos — Criar Produto')
        self.setFixedSize(680, 460)
        self.setContentsMargins(10, 10, 10, 10)
        self.setStyleSheet(style.cor_fundo)

    def criar_produto(self):
        try:
            self.dado = {'nome': self.campo_nome.text(), 'marca': self.campo_marca.text(), 'valor_unitario': Decimal(self.campo_valor_unitario.text()), 'categoria': self.menu_suspenso_categoria.currentText().lower()}
            self.tela_principal.produto_controller.criar(**self.dado)
            self.tela_principal.msg('Sucess', f'Produto {self.campo_nome.text().upper()} criado com sucesso!', 'information')
        except Exception as e:
            self.tela_principal.msg('Error', e, 'warning')    

    def criar_menu_suspenso(self):
        self.menu = QComboBox()
        self.menu.setStyleSheet(style.estilo_menu_suspenso)
        self.menu.setMaximumHeight(32)
        self.menu.setContentsMargins(0, 0, 0, 0)
        self.dados_categoria = self.categoria_controller.buscar_todos()
        self.menu.addItems(list(map(str.capitalize, self.dados_categoria[0])))
        self.menu.setCurrentIndex(-1)
        return self.menu

a = TelaPrincipal(instances.estoque_controller, instances.produto_controller, instances.categoria_controller)

a.show()
sys.exit(app.exec())