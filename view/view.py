from PySide6.QtWidgets import (QMainWindow,
                                QFrame, QLabel, QTableView,
                                QVBoxLayout, QHBoxLayout,
                                QHeaderView, QLineEdit,
                                QPushButton, QGridLayout,
                                QAbstractItemView, QDialog,
                                QMessageBox, QComboBox,)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from view.table_model.table_model import TableClass, TableEditableClass
from view.style import style
from view.validators_view.validators_view import NumDelegateOnly, StrDelegateOnly, IntValidation, DecimalValidation, StrOnlyValidator
from decimal import Decimal

class TelaPrincipal(QMainWindow):
    def __init__(self, estoque_controller, produto_controller, categoria_controller, movimentacao_controller, relatorio_controller):
        self.produto_controller = produto_controller
        self.estoque_controller = estoque_controller
        self.categoria_controller = categoria_controller
        self.movimentacao_controller = movimentacao_controller
        self.relatorio_controller = relatorio_controller

        self.dados_tabela_generica = self.estoque_controller.buscar_todos()
        self.dados_id = {}
        super().__init__()
        
        self.setWindowIcon(QIcon())
        self.setWindowTitle('Estoque — Buscar Todos')

        self.barra_estoque = self.barra_menu('Estoque')
        self.submenu = self.gerar_submenu(self.barra_estoque, ['Adicionar Produto', 'Atualizar Produto', 'Remover Produto'])

        self.barra_produto = self.barra_menu('Produto')
        self.submenu = self.gerar_submenu(self.barra_produto, ['Criar Produto', 'Atualizar Produto', 'Remover Produto', 'Buscar Todos'])

        self.barra_categoria = self.barra_menu('Categoria')
        self.submenu = self.gerar_submenu(self.barra_categoria, ['Criar Categoria', 'Atualizar Categoria', 'Remover Categoria', 'Buscar Todos'])

        self.barra_movimentacao = self.barra_menu('Movimentacao')
        self.submenu = self.gerar_submenu(self.barra_movimentacao, ['Buscar Todos'])

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
        self.tabela_model = TableClass(self.dados_tabela_generica)

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
        dado_recebido['nome'] = self.entrada_nome.text().strip()
        dado_recebido['marca'] = self.entrada_marca.text().strip()
        dado_recebido['categoria'] = self.entrada_categoria.text().strip()
        dado_recebido['sku'] = self.entrada_sku.text().strip()
        dado_recebido['valor_unitario'] = self.entrada_valor_unitario.text().strip()
        dado_recebido['quantidade'] = self.entrada_quantidade.text().strip()
        dado_recebido['estoque_minimo'] = self.entrada_estoque_minimo.text().strip()

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
        if nome_campo:
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
                self.tela_adicionar_produto_estoque = SubMenuEstoqueAdicionarProduto(self)
            if destino == 'Atualizar Produto':
                self.tela_atualizar_produto_estoque = SubMenuEstoqueAtualizarProduto(self)
            if destino == 'Remover Produto':
                self.tela_remover_produto_estoque = SubMenuEstoqueRemoverProduto(self)
        if setor == 'Produto':
            if destino == 'Criar Produto':
                self.tela_criar_produto = SubMenuProdutoCriarProduto(self)
                self.tela_criar_produto.show()
            if destino == 'Atualizar Produto':
                self.tela_atualizar_produto = SubMenuProdutoAtualizarProduto(self)
            if destino == 'Buscar Todos':
                self.tela_buscar_todos_produtos = SubMenuProdutoBuscarTodos(self)
            if destino == 'Remover Produto':
                self.tela_remover_produto = SubMenuProdutoRemoverProduto (self)
        if setor == 'Categoria':
            if destino == 'Criar Categoria':
                self.tela_criar_categoria = SubMenuCategoriaCriarCategoria(self)
                self.tela_criar_categoria.show()
            if destino == 'Atualizar Categoria':
                self.tela_atualizar_categoria = SubMenuCategoriaAtualizarCategoria(self)
            if destino == 'Buscar Todos':
                self.tela_buscar_todos_categoria = SubMenuCategoriaBuscarTodos(self)
            if destino == 'Remover Categoria':
                self.tela_remover_categoria = SubMenuCategoriaRemoverCategoria(self)
        if setor == 'Movimentacao':
            if destino == 'Buscar Todos':
                self.tela_filtrar_movimentacao = SubMenuMovimentacaoBuscarTodos(self)

    def definir_botao(self, texto, funcao=None):
        botao_pesquisar = QPushButton(texto)
        botao_pesquisar.setStyleSheet(style.estilo_botao)
        botao_pesquisar.setCursor(Qt.PointingHandCursor)
        botao_pesquisar.setMinimumHeight(40)
        botao_pesquisar.setMinimumWidth(200)
        if funcao != None:
            botao_pesquisar.clicked.connect(funcao)
        return botao_pesquisar

    def tela_pegar_id(self, title, dado, coluna=False, nome_botao=None, funcao=None):
        self.tela = QFrame()
        self.tela.setWindowTitle(title)

        self.model = TableClass(dado)

        self.tabela_view = self.criar_tabela(self.model)
        if coluna == False:
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

        if nome_botao and funcao:
            self.frame_superior = QFrame()

            self.frame_superior.setMaximumHeight(50)
            self.frame_superior.setStyleSheet(style.cor_fundo)
            self.botao_adicionar = self.definir_botao(nome_botao, funcao)
            self.layout_botoes = QHBoxLayout(self.frame_superior)
            self.layout_botoes.addWidget(self.botao_adicionar)
            self.tela_layout.addWidget(self.frame_superior)

        self.tela_layout.addWidget(self.frame_tabela)
        self.tela_layout.setContentsMargins(0, 0, 0, 0)
        self.tela_layout.setSpacing(0)
        self.tela_layout.setStretch(0, 1)
        self.tela_layout.setStretch(1, 1)

        self.tela.setMinimumSize(1080, 720)
        self.tela.setContentsMargins(0, 0, 0, 0)
        self.tela.setStyleSheet(style.cor_fundo)

        return self.tela

    def pegar_dados_linha(self, index):
        linha = index.row()
        self.data = self.model.retornar_data()
        dados_linha = self.data[0][linha]
        self.dados_id['id'] = dados_linha[0]

    def criar_tabela(self, model, pegar_dado=True, esconder_coluna=False):
        tabela_view = QTableView()
        tabela_view.setModel(model)
        tabela_view.setContentsMargins(0, 0, 0, 0)
        tabela_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tabela_view.setStyleSheet(style.estilo_tabela)
        tabela_view.setProperty('show-decoration-selected', True)
        tabela_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        tabela_view.setSelectionMode(QAbstractItemView.SingleSelection)
        if esconder_coluna == True:
            tabela_view.hideColumn(0)

        if pegar_dado == True:
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

    def tela_generica(self, controller, nome_tela, texto_botao=None, funcao_tela_atualizar=None, coluna=False, retornar=False):
        self.dados_genericos = controller.buscar_todos()
        self.tela_atualizar = self.tela_pegar_id(nome_tela, self.dados_genericos, coluna, texto_botao, funcao_tela_atualizar)

        self.tela_geral = QFrame()

        self.tela_geral.setWindowTitle(nome_tela)
        self.tela_geral.setMinimumSize(1000, 600)
        self.tela_geral.setContentsMargins(10, 10, 10, 10)
        self.tela_geral.setStyleSheet(style.cor_fundo)

        self._layout = QVBoxLayout(self.tela_geral)
        self._layout.addWidget(self.tela_atualizar)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        if retornar == True:
            return self.tela_geral
        else:
            self.tela_geral.show()

    def tela_tabela_generica(self, controller, nome_tela, funcao_atualizar, colunas=None, delegates=None):
        if self.dados_id:
            self.id = self.dados_id['id']
            self.dados_tabela_generica = controller.buscar_por_id(self.id)

            self.tela_ajustar = QDialog()
            self.tela_ajustar.setWindowTitle(nome_tela)
            self.tela_ajustar.setFixedSize(1000, 500)

            self.frame_cima = QFrame()
            self.frame_cima.setStyleSheet(style.cor_fundo)
            self.frame_cima.setContentsMargins(0, 0, 0, 0)
            self.frame_cima.setFixedHeight(100)

            self.frame_baixo = QFrame()
            self.frame_baixo.setStyleSheet(style.cor_secundaria)
            self.frame_baixo.setContentsMargins(0, 0, 0, 0)

            self.tabela_model_generica = TableEditableClass(self.dados_tabela_generica, colunas)

            self.botao_ok = self.definir_botao('OK', funcao_atualizar)
            self.botao_cancel = self.definir_botao('CANCEL', self.tela_ajustar.close)

            self.tabela_view_generica = self.criar_tabela(self.tabela_model_generica)
            self.tabela_view_generica.hideColumn(0)

            if delegates:
                for coluna, delegate in delegates.items():
                    self.tabela_view_generica.setItemDelegateForColumn(coluna, delegate)

            self.layout_frame_cima = QHBoxLayout(self.frame_cima)
            self.layout_frame_cima.addWidget(self.botao_ok)
            self.layout_frame_cima.addWidget(self.botao_cancel)

            self.layout_frame_baixo = QVBoxLayout(self.frame_baixo)
            self.layout_frame_baixo.addWidget(self.tabela_view_generica)
            self.layout_frame_baixo.setContentsMargins(10, 10, 10, 10)

            self.layout_principal = QVBoxLayout(self.tela_ajustar)
            self.layout_principal.addWidget(self.frame_cima)
            self.layout_principal.addWidget(self.frame_baixo)
            self.layout_principal.setSpacing(0)

            self.grid = QGridLayout(self.tabela_view_generica)
            self.grid.setContentsMargins(0, 0, 0, 0)

            self.tela_ajustar.exec()

    def atualizar_generico(self, controller, nome_tipo_dado):
        try:
            dados_model = self.tabela_model_generica.retornar_data()
            if dados_model:
                controller.atualizar(id=self.id, **dados_model)
                dados_novos = controller.buscar_todos()
                self.model.atualizar_dados_model(dados_novos)
                self.tabela_model_generica.atualizar_dados_model(dados_novos)
                self.msg('Success', f'{nome_tipo_dado.capitalize()} atualizado com sucesso!', 'information')
                self.tela_ajustar.close()
                dados_model.clear()
        except Exception as e:
            self.msg('Error', e, 'warning')

    def remover_generico(self, controller):
        try:
            if not self.tela_confirmacao():
                return
            print(self.dados_id)
            self.id = self.dados_id['id']
            self.info = controller.delete(self.id)
            novos_dados = controller.buscar_todos()
            self.model.atualizar_dados_model(novos_dados)
            self.msg('Success', self.info, 'information')
            self.dados_id.clear()
        except Exception as e:
            self.msg('Error', e, 'warning')

class SubMenuEstoqueAdicionarProduto(QFrame):
    def __init__(self, tela_principal):
        self.tela_principal = tela_principal
        super().__init__()
        self.tela_adicionar = self.tela_principal.tela_generica(self.tela_principal.produto_controller, 'Estoque — Adicionar Produto', 'ADICIONAR AO ESTOQUE', self.adicionar_produto)

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
                    dados = self.tela_principal.dados_id
                    dados['id_produto'] = dados['id']
                    dados.pop('id')
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
        self.delegate_num = NumDelegateOnly()
        self.tela_principal.tela_generica(self.tela_principal.estoque_controller, 'Estoque — Atualizar Produto no Estoque', 'ATUALIZAR ESTOQUE',
                                          lambda: self.tela_principal.tela_tabela_generica(self.tela_principal.estoque_controller, 'Estoque — Ajustar Estoque', self.ajustar_estoque, colunas=[6, 7], delegates={6: self.delegate_num , 7: self.delegate_num}))

    def ajustar_estoque(self):
        try:
            dado_model = self.tela_principal.tabela_model_generica.retornar_data()
            if dado_model:
                self.tela_principal.estoque_controller.ajustar_produto(self.tela_principal.id, **dado_model)
                dados_novos = self.tela_principal.estoque_controller.buscar_todos()
                self.tela_principal.model.atualizar_dados_model(dados_novos)
                self.tela_principal.tabela_model.atualizar_dados_model(dados_novos)
                self.tela_principal.tabela_model_generica.atualizar_dados_model(dados_novos)
                self.tela_principal.msg('Success', 'Estoque ajustado com sucesso!', 'information')
                dado_model.clear()
                self.tela_principal.tela_ajustar.close()
        except Exception as e:
            self.tela_principal.msg('Error', e, 'warning')

class SubMenuEstoqueRemoverProduto(QFrame):
    def __init__(self,tela_principal):
        self.tela_principal = tela_principal
        super().__init__()
        self.tela_principal.tela_generica(self.tela_principal.estoque_controller ,'Estoque — Remover Produto do Estoque', 'REMOVER PRODUTO', self.remover_produto)

    def remover_produto(self):
        try:
            if not self.tela_principal.tela_confirmacao():
                return
            self.id = self.tela_principal.dados_id['id']
            self.info = self.tela_principal.estoque_controller.delete(self.id)
            novos_dados = self.tela_principal.estoque_controller.buscar_todos()
            self.tela_principal.tabela_model.atualizar_dados_model(novos_dados)
            self.tela_principal.model.atualizar_dados_model(novos_dados)
            self.tela_principal.msg('Success', self.info, 'information')
            self.tela_principal.dados_id.clear()
        except Exception as e:
            self.tela_principal.msg('Error', e, 'warning')


class SubMenuProdutoCriarProduto(QFrame):
    def __init__(self, tela_principal):
        self.tela_principal = tela_principal
        super().__init__()
        self.dados_produto = self.tela_principal.produto_controller.buscar_todos()
        self.dados_categoria = self.tela_principal.categoria_controller.buscar_todos()

        self.campo_nome = self.tela_principal.criar_campos('Digite o nome do produto...')
        self.campo_marca = self.tela_principal.criar_campos('Digite a marca do produto...')
        self.campo_valor_unitario = self.tela_principal.criar_campos('Digite o valor unitário do produto...')
        self.campo_valor_unitario.setValidator(DecimalValidation.validate())
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
        self.grid.addWidget(self.menu_suspenso_categoria_borda, 3, 1)
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
            if not self.campo_nome.text() and not self.campo_marca.text() and not self.campo_valor_unitario.text() and not self.menu_suspenso_categoria.currentText():
                raise NameError('Os campos não podem estar vazios.')
            print(self.menu_suspenso_categoria.currentText())
            self.dado = {'nome': self.campo_nome.text(), 'marca': self.campo_marca.text(), 'valor_unitario': Decimal(self.campo_valor_unitario.text()), 'categoria': self.menu_suspenso_categoria.currentText().lower()}
            self.tela_principal.produto_controller.criar(**self.dado)
            self.tela_principal.msg('Success', f'Produto {self.campo_nome.text().upper()} criado com sucesso!', 'information')

        except Exception as e:
            self.tela_principal.msg('Error', e, 'warning')

        finally:
            self.campo_nome.clear()
            self.campo_marca.clear()
            self.campo_valor_unitario.clear()
            self.menu_suspenso_categoria.setCurrentIndex(-1)

    def criar_menu_suspenso(self):
        self.menu = QComboBox()
        self.menu.setStyleSheet(style.estilo_menu_suspenso)
        self.menu.setMaximumHeight(32)
        self.menu.setContentsMargins(0, 0, 0, 0)
        self.menu.addItems(i[1].capitalize() for i in self.dados_categoria[0])
        self.menu.setCurrentIndex(-1)
        return self.menu

class SubMenuProdutoAtualizarProduto(QFrame):
    def __init__(self, tela_principal):
        self.tela_principal = tela_principal
        super().__init__()

        delegate_str = StrDelegateOnly()
        self.tela_principal.tela_generica(self.tela_principal.produto_controller, 'Produtos — Atualizar Produto', 'ATUALIZAR PRODUTO',
                                        lambda: self.tela_principal.tela_tabela_generica(self.tela_principal.produto_controller, 'Produtos — Atualizar Produto', self.atualizar_produto, colunas=[1, 2, 3, 5], delegates={1: delegate_str, 2: delegate_str, 3: delegate_str}))

    def atualizar_produto(self):
        self.tela_principal.atualizar_generico(self.tela_principal.produto_controller, 'produto')

class SubMenuProdutoBuscarTodos(QFrame):
    def __init__(self, tela_principal):
        self.tela_principal = tela_principal
        self.dados_produto = self.tela_principal.produto_controller.buscar_todos()
        super().__init__()

        self.setMinimumSize(1080, 720)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle('Produtos — Buscar Todos')

        frame_busca = QFrame()
        frame_busca.setContentsMargins(0, 0, 0, 0)
        frame_busca.setStyleSheet(style.cor_fundo)

        self.nome = self.tela_principal.criar_campos('Digite o nome do produto: ')
        self.categoria = self.tela_principal.criar_campos('Digite a categoria do produto: ')
        self.marca = self.tela_principal.criar_campos('Digite a marca produto: ')
        self.sku = self.tela_principal.criar_campos('Digite o sku do produto: ')
        self.valor_unitario = self.tela_principal.criar_campos('Digite o valor unitário: ')

        botao_filtrar = self.tela_principal.definir_botao('PESQUISAR', self.filtrar)

        nome_borda = self.tela_principal.adicionar_bordas(self.nome)
        categoria_borda = self.tela_principal.adicionar_bordas(self.categoria)
        marca_borda = self.tela_principal.adicionar_bordas(self.marca)
        sku_borda = self.tela_principal.adicionar_bordas(self.sku)
        valor_unitario_borda = self.tela_principal.adicionar_bordas(self.valor_unitario)

        grid_busca = QGridLayout(frame_busca)
        grid_busca.addWidget(botao_filtrar, 4, 1, 3, 1)
        grid_busca.setContentsMargins(10, 20, 10, 20)

        self.tela_principal.posicionar_campo(grid_busca, 'nome', nome_borda,  0, 0, 1, 0)
        self.tela_principal.posicionar_campo(grid_busca, 'marca', marca_borda,  0, 1, 1, 1)
        self.tela_principal.posicionar_campo(grid_busca, 'categoria', categoria_borda,  2, 0, 3, 0)
        self.tela_principal.posicionar_campo(grid_busca, 'sku', sku_borda,  2, 1, 3, 1)
        self.tela_principal.posicionar_campo(grid_busca, 'valor unitário', valor_unitario_borda,  4, 0, 5, 0)

        # relacionado a parte de tabela
        frame_moldura_tabela = QFrame()
        frame_moldura_tabela.setContentsMargins(0, 0, 0, 0)
        frame_moldura_tabela.setStyleSheet(style.cor_fundo)

        frame_moldura_tabela_borda = QFrame()
        frame_moldura_tabela_borda.setContentsMargins(10, 10, 10, 10)
        frame_moldura_tabela_borda.setStyleSheet(style.cor_secundaria)

        frame_interno_moldura_tabela = QFrame()
        frame_interno_moldura_tabela.setContentsMargins(0, 0, 0, 0)
        frame_interno_moldura_tabela.setStyleSheet(style.cor_fundo) 

        self.tabela_model = TableClass(self.dados_produto)
        tabela = self.tela_principal.criar_tabela(self.tabela_model, pegar_dado=False, esconder_coluna=True)
        grid_tabela_layout = QGridLayout(tabela)
        grid_tabela_layout.setContentsMargins(0, 0, 0, 0)

        frame_moldura_tabela_layout = QVBoxLayout(frame_moldura_tabela)
        frame_moldura_tabela_layout.addWidget(frame_moldura_tabela_borda)

        frame_moldura_tabela_borda_layout = QVBoxLayout(frame_moldura_tabela_borda)
        frame_moldura_tabela_borda_layout.addWidget(frame_interno_moldura_tabela)
        frame_moldura_tabela_borda_layout.setContentsMargins(0, 0, 0, 0)

        frame_interno_moldura_tabela_layout = QVBoxLayout(frame_interno_moldura_tabela)
        frame_interno_moldura_tabela_layout.addWidget(tabela)
        frame_interno_moldura_tabela_layout.setContentsMargins(0, 0, 0, 0)

        self_layout = QVBoxLayout(self)
        self_layout.setSpacing(0)
        self_layout.setContentsMargins(0, 0, 0, 0)
        self_layout.addWidget(frame_busca)
        self_layout.addWidget(frame_moldura_tabela)
        self_layout.setStretch(0,1)
        self_layout.setStretch(1,1)
    
        self.show()

    def filtrar(self):
        nome = self.nome.text().strip()
        marca = self.marca.text().strip()
        categoria = self.categoria.text().strip()
        sku = self.sku.text().strip()
        valor_unitario = self.valor_unitario.text().strip()

        parametro = {'nome': nome, 'categoria': categoria, 'marca': marca, 'sku': sku, 'valor_unitario': valor_unitario}

        parametro_temp = parametro.copy()

        for i in parametro_temp:
            if not parametro[i]:
                parametro.pop(i)

        try:
            dados = self.tela_principal.produto_controller.filtrar(**parametro)
            self.tabela_model.atualizar_dados_model(dados)
        except Exception as e:
            self.tela_principal.msg('Error', e, 'warning')
        finally:
            nome = self.nome.clear()
            marca = self.marca.clear()
            categoria = self.categoria.clear()
            sku = self.sku.clear()
            valor_unitario = self.valor_unitario.clear()
            parametro.clear()

class SubMenuProdutoRemoverProduto(QFrame):
    def __init__(self, tela_principal):
        self.tela_principal = tela_principal
        super().__init__()

        self.tela_principal.tela_generica(self.tela_principal.produto_controller, 'Produtos — Remover Produto', 'REMOVER PRODUTO', self.remover_produto)

    def remover_produto(self):
        self.tela_principal.remover_generico(self.tela_principal.produto_controller)


class SubMenuCategoriaCriarCategoria(QFrame):
    def __init__(self, tela_principal):
        self.tela_principal = tela_principal
        super().__init__()

        self.campo_nome = self.tela_principal.criar_campos('Digite o nome da categoria...')
        self.campo_nome.setValidator(StrOnlyValidator.validate())

        self.campo_nome_borda = self.tela_principal.adicionar_bordas(self.campo_nome)

        self.botao_enviar = self.tela_principal.definir_botao('CRIAR CATEGORIA', self.criar_categoria)

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
        self.grid.addWidget(self.botao_enviar, 2,0)

        self.layout_frame_fora = QVBoxLayout(self.frame_fora)
        self.layout_frame_fora.addWidget(self.frame_dentro, alignment=Qt.AlignCenter)

        self._layout = QVBoxLayout(self)
        self._layout.addWidget(self.frame_fora, alignment=Qt.AlignCenter)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self.setWindowTitle('Categorias — Criar Categoria')
        self.setFixedSize(680, 460)
        self.setContentsMargins(10, 10, 10, 10)
        self.setStyleSheet(style.cor_fundo)

    def criar_categoria(self):
        try:
            self.dados_categoria = self.campo_nome.text()
            if self.dados_categoria:
                self.tela_principal.categoria_controller.criar(nome=self.dados_categoria)
                self.tela_principal.msg('Success', 'Categoria criada com sucesso!', 'information')
                self.campo_nome.clear()
        except Exception as e:
            self.tela_principal.msg('Error', e, 'warning')

class SubMenuCategoriaAtualizarCategoria(QFrame):
    def __init__(self, tela_principal):
        self.tela_principal = tela_principal
        super().__init__()

        self.tela_principal.tela_generica(self.tela_principal.categoria_controller, 'Categorias — Atualizar Categoria', 'ATUALIZAR CATEGORIA',
                                          lambda: self.tela_principal.tela_tabela_generica(self.tela_principal.categoria_controller, 'Categorias — Atualizar Categoria', self.atualizar_categoria))

    def atualizar_categoria(self):
        self.tela_principal.atualizar_generico(self.tela_principal.categoria_controller, 'categoria')

class SubMenuCategoriaBuscarTodos(QFrame):
    def __init__(self, tela_principal):
        self.tela_principal = tela_principal
        self.dados_categoria = self.tela_principal.categoria_controller.buscar_todos()
        super().__init__()

        self.setMinimumSize(1080, 720)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle('Categoria — Buscar Todos')

        frame_busca = QFrame()
        frame_busca.setContentsMargins(0, 0, 0, 0)
        frame_busca.setStyleSheet(style.cor_fundo)

        self.nome = self.tela_principal.criar_campos('Digite o nome do produto: ')
        nome_borda = self.tela_principal.adicionar_bordas(self.nome)

        botao_filtrar = self.tela_principal.definir_botao('PESQUISAR', self.buscar_por_nome)
    
        grid_busca = QGridLayout(frame_busca)
        grid_busca.addWidget(botao_filtrar, 1, 1)
        grid_busca.setContentsMargins(10, 50, 10, 0)

        self.tela_principal.posicionar_campo(grid_busca, '', nome_borda,  0, 0, 1, 0)

        # relacionado a parte de tabela
        frame_moldura_tabela = QFrame()
        frame_moldura_tabela.setContentsMargins(0, 0, 0, 0)
        frame_moldura_tabela.setStyleSheet(style.cor_fundo)

        frame_moldura_tabela_borda = QFrame()
        frame_moldura_tabela_borda.setContentsMargins(10, 10, 10, 10)
        frame_moldura_tabela_borda.setStyleSheet(style.cor_secundaria)

        frame_interno_moldura_tabela = QFrame()
        frame_interno_moldura_tabela.setContentsMargins(0, 0, 0, 0)
        frame_interno_moldura_tabela.setStyleSheet(style.cor_fundo) 

        self.tabela_model = TableClass(self.dados_categoria)
        tabela = self.tela_principal.criar_tabela(self.tabela_model, pegar_dado=False, esconder_coluna=True)
        grid_tabela_layout = QGridLayout(tabela)
        grid_tabela_layout.setContentsMargins(0, 0, 0, 0)

        frame_moldura_tabela_layout = QVBoxLayout(frame_moldura_tabela)
        frame_moldura_tabela_layout.addWidget(frame_moldura_tabela_borda)

        frame_moldura_tabela_borda_layout = QVBoxLayout(frame_moldura_tabela_borda)
        frame_moldura_tabela_borda_layout.addWidget(frame_interno_moldura_tabela)
        frame_moldura_tabela_borda_layout.setContentsMargins(0, 0, 0, 0)

        frame_interno_moldura_tabela_layout = QVBoxLayout(frame_interno_moldura_tabela)
        frame_interno_moldura_tabela_layout.addWidget(tabela)
        frame_interno_moldura_tabela_layout.setContentsMargins(0, 0, 0, 0)

        self_layout = QVBoxLayout(self)
        self_layout.setSpacing(0)
        self_layout.setContentsMargins(0, 0, 0, 0)
        self_layout.addWidget(frame_busca)
        self_layout.addWidget(frame_moldura_tabela)
        self_layout.setStretch(0,1)
        self_layout.setStretch(1,8)
    
        self.show()

    def buscar_por_nome(self):
        try:
            entrada = self.nome.text()
            if entrada:
                dados = self.tela_principal.categoria_controller.buscar_por_nome(entrada)
                self.tabela_model.atualizar_dados_model(dados)
                self.nome.clear()
            else:
                dados = self.tela_principal.categoria_controller.buscar_todos()
                self.tabela_model.atualizar_dados_model(dados)
        except Exception as e:
            self.tela_principal.msg('Error',e, 'warning')

class SubMenuCategoriaRemoverCategoria(QFrame):
    def __init__(self, tela_principal):
        self.tela_principal = tela_principal
        super().__init__()

        self.tela_principal.tela_generica(self.tela_principal.categoria_controller, 'Categorias — Remover Categoria', 'REMOVER CATEGORIA', self.remover_categoria)

    def remover_categoria(self):
            self.tela_principal.remover_generico(self.tela_principal.categoria_controller)


class SubMenuMovimentacaoBuscarTodos(QFrame):
    def __init__(self, tela_principal):
        self.tela_principal = tela_principal
        self.dados_movimentacao = self.tela_principal.movimentacao_controller.buscar_todos()
        self.chamada_filtrar = False
        super().__init__()

        self.setMinimumSize(1600, 900)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle('Movimentação — Buscar Todos')

        frame_busca = QFrame()
        frame_busca.setContentsMargins(0, 0, 0, 0)
        frame_busca.setStyleSheet(style.cor_fundo)

        self.nome = self.tela_principal.criar_campos('Digite o nome do produto: ')
        self.categoria = self.tela_principal.criar_campos('Digite a categoria do produto: ')
        self.marca = self.tela_principal.criar_campos('Digite a marca produto: ')
        self.sku = self.tela_principal.criar_campos('Digite o sku do produto: ')
        self.quantidade = self.tela_principal.criar_campos('Digite a quantidade do produto: ')
        self.valor_unitario = self.tela_principal.criar_campos('Digite o valor unitário: ')
        self.tipo_movimentacao = self.tela_principal.criar_campos('Digite o tipo de movimentação: ')
        self.origem = self.tela_principal.criar_campos('Digite a origem da movimentação: ')

        self.ano_inicial = self.tela_principal.criar_campos('Digite o ano inicial: ')
        self.ano_final = self.tela_principal.criar_campos('Digite o ano final: ')

        self.mes_inicial = self.tela_principal.criar_campos('Digite o mês inicial: ')
        self.mes_final = self.tela_principal.criar_campos('Digite o mês final: ')

        self.dia_inicial = self.tela_principal.criar_campos('Digite o dia inicial: ')
        self.dia_final = self.tela_principal.criar_campos('Digite o dia final: ')

        self.ano = self.tela_principal.criar_campos('Digite o ano: ')
        self.mes = self.tela_principal.criar_campos('Digite o mês: ')
        self.dia = self.tela_principal.criar_campos('Digite o dia: ')

        botao_filtrar = self.tela_principal.definir_botao('PESQUISAR', self.filtrar)
        botao_relatorio = self.tela_principal.definir_botao('GERAR RELATÓRIO', self.gerar_relatorio)

        nome_borda = self.tela_principal.adicionar_bordas(self.nome)
        categoria_borda = self.tela_principal.adicionar_bordas(self.categoria)
        marca_borda = self.tela_principal.adicionar_bordas(self.marca)
        sku_borda = self.tela_principal.adicionar_bordas(self.sku)
        quantidade_borda = self.tela_principal.adicionar_bordas(self.quantidade)
        valor_unitario_borda = self.tela_principal.adicionar_bordas(self.valor_unitario)
        tipo_movimentacao_borda = self.tela_principal.adicionar_bordas(self.tipo_movimentacao)
        origem_borda = self.tela_principal.adicionar_bordas(self.origem)

        ano_inicial_borda = self.tela_principal.adicionar_bordas(self.ano_inicial)
        ano_final_borda = self.tela_principal.adicionar_bordas(self.ano_final)

        mes_inicial_borda = self.tela_principal.adicionar_bordas(self.mes_inicial)
        mes_final_borda = self.tela_principal.adicionar_bordas(self.mes_final)

        dia_inicial_borda = self.tela_principal.adicionar_bordas(self.dia_inicial)
        dia_final_borda = self.tela_principal.adicionar_bordas(self.dia_final)

        ano_borda = self.tela_principal.adicionar_bordas(self.ano)
        mes_borda = self.tela_principal.adicionar_bordas(self.mes)
        dia_borda = self.tela_principal.adicionar_bordas(self.dia)

        grid_busca = QGridLayout(frame_busca)
        grid_busca.addWidget(botao_filtrar, 8, 1, 3, 2)
        grid_busca.addWidget(botao_relatorio, 8, 3, 3, 3)
        grid_busca.setContentsMargins(10, 50, 10, 20)

        self.tela_principal.posicionar_campo(grid_busca, 'nome', nome_borda,  0, 0, 1, 0)
        self.tela_principal.posicionar_campo(grid_busca, 'marca', marca_borda,  2, 0, 3, 0)
        self.tela_principal.posicionar_campo(grid_busca, 'categoria', categoria_borda,  4, 0, 5, 0)
        self.tela_principal.posicionar_campo(grid_busca, 'sku', sku_borda,  6, 0, 7, 0)

        self.tela_principal.posicionar_campo(grid_busca, 'quantidade', quantidade_borda,  0, 1, 1, 1)
        self.tela_principal.posicionar_campo(grid_busca, 'valor unitário', valor_unitario_borda,  2, 1, 3, 1)
        self.tela_principal.posicionar_campo(grid_busca, 'tipo de movimentação', tipo_movimentacao_borda,  4, 1, 5, 1)
        self.tela_principal.posicionar_campo(grid_busca, 'origem', origem_borda,  6, 1, 7, 1)

        self.tela_principal.posicionar_campo(grid_busca, 'ano inicial', ano_inicial_borda,  0, 2, 1, 2)
        self.tela_principal.posicionar_campo(grid_busca, 'ano final', ano_final_borda,  0, 3, 1, 3)

        self.tela_principal.posicionar_campo(grid_busca, 'mês inicial', mes_inicial_borda,  2, 2, 3, 2)
        self.tela_principal.posicionar_campo(grid_busca, 'mês final', mes_final_borda,  2, 3, 3, 3)

        self.tela_principal.posicionar_campo(grid_busca, 'dia inicial', dia_inicial_borda,  4, 2, 5, 2)
        self.tela_principal.posicionar_campo(grid_busca, 'dia final', dia_final_borda,  4, 3, 5, 3)

        self.tela_principal.posicionar_campo(grid_busca, 'ano', ano_borda,  6, 2, 7, 2)
        self.tela_principal.posicionar_campo(grid_busca, 'mês', mes_borda,  6, 3, 7, 3)
        self.tela_principal.posicionar_campo(grid_busca, 'dia', dia_borda,  8, 0, 9, 0)

        # relacionado a parte de tabela
        frame_moldura_tabela = QFrame()
        frame_moldura_tabela.setContentsMargins(0, 0, 0, 0)
        frame_moldura_tabela.setStyleSheet(style.cor_fundo)

        frame_moldura_tabela_borda = QFrame()
        frame_moldura_tabela_borda.setContentsMargins(10, 10, 10, 10)
        frame_moldura_tabela_borda.setStyleSheet(style.cor_secundaria)

        frame_interno_moldura_tabela = QFrame()
        frame_interno_moldura_tabela.setContentsMargins(0, 0, 0, 0)
        frame_interno_moldura_tabela.setStyleSheet(style.cor_fundo) 

        self.tabela_model = TableClass(self.dados_movimentacao[0])
        tabela = self.tela_principal.criar_tabela(self.tabela_model, pegar_dado=False)
        grid_tabela_layout = QGridLayout(tabela)
        grid_tabela_layout.setContentsMargins(0, 0, 0, 0)

        frame_moldura_tabela_layout = QVBoxLayout(frame_moldura_tabela)
        frame_moldura_tabela_layout.addWidget(frame_moldura_tabela_borda)

        frame_moldura_tabela_borda_layout = QVBoxLayout(frame_moldura_tabela_borda)
        frame_moldura_tabela_borda_layout.addWidget(frame_interno_moldura_tabela)
        frame_moldura_tabela_borda_layout.setContentsMargins(0, 0, 0, 0)

        frame_interno_moldura_tabela_layout = QVBoxLayout(frame_interno_moldura_tabela)
        frame_interno_moldura_tabela_layout.addWidget(tabela)
        frame_interno_moldura_tabela_layout.setContentsMargins(0, 0, 0, 0)

        self_layout = QVBoxLayout(self)
        self_layout.setSpacing(0)
        self_layout.setContentsMargins(0, 0, 0, 0)
        self_layout.addWidget(frame_busca)
        self_layout.addWidget(frame_moldura_tabela)
        self_layout.setStretch(0,1)
        self_layout.setStretch(1,1)
    
        self.show()

    def filtrar(self):
        nome = self.nome.text().strip()
        categoria = self.categoria.text().strip() 
        marca = self.marca.text().strip()
        sku = self.sku.text().strip()
        quantidade = self.quantidade.text().strip()
        valor_unitario = self.valor_unitario.text().strip()
        tipo_movimentacao = self.tipo_movimentacao.text().upper().strip()
        origem = self.origem.text().upper().strip()
        ano_inicial = self.ano_inicial.text().strip()
        ano_final = self.ano_final.text().strip()
        mes_inicial = self.mes_inicial.text().strip()
        mes_final = self.mes_final.text().strip()
        dia_inicial = self.dia_inicial.text().strip()
        dia_final = self.dia_final.text().strip()
        ano = self.ano.text().strip()
        mes = self.mes.text().strip()
        dia = self.dia.text().strip()

        if quantidade:
            quantidade = int(quantidade)

        if valor_unitario:
            valor_unitario = Decimal(valor_unitario)

        self.parametros = {'nome': nome, 'categoria': categoria, 'marca': marca,
                    'sku': sku, 'valor_unitario': valor_unitario, 'quantidade': quantidade,
                    'tipo_movimentacao': tipo_movimentacao, 'origem': origem,
                    'ano_inicial': ano_inicial, 'ano_final': ano_final,
                    'mes_inicial': mes_inicial, 'mes_final': mes_final,
                    'dia_inicial': dia_inicial, 'dia_final': dia_final,
                    'ano': ano, 'mes': mes, 'dia': dia}
        
        self.parametros_temp = self.parametros.copy()
        
        for i in self.parametros_temp:
            if not self.parametros_temp[i]:
                self.parametros.pop(i)
        try:
            self.dados = self.tela_principal.movimentacao_controller.filtrar(**self.parametros)
            self.tabela_model.atualizar_dados_model(self.dados[0])
        except Exception as e:
            self.tela_principal.msg('Error', e, 'warning')
        finally:
            nome = self.nome.clear()
            categoria = self.categoria.clear() 
            marca = self.marca.clear() 
            sku = self.sku.clear()
            quantidade = self.quantidade.clear()
            valor_unitario = self.valor_unitario.clear()
            tipo_movimentacao = self.tipo_movimentacao.clear()
            origem = self.origem.clear()
            ano_inicial = self.ano_inicial.clear()
            ano_final = self.ano_final.clear()
            mes_inicial = self.mes_inicial.clear()
            mes_final = self.mes_final.clear()
            dia_inicial = self.dia_inicial.clear()
            dia_final = self.dia_final.clear()
            ano = self.ano.clear()
            mes = self.mes.clear()
            dia = self.dia.clear()
            self.parametros.clear()
            self.chamada_filtrar = True

    def gerar_relatorio(self):
        try:
            if self.chamada_filtrar:
                self.tela_principal.relatorio_controller.gerar_relatorio_pdf(self.dados[1])
            else:
                self.tela_principal.relatorio_controller.gerar_relatorio_pdf(self.dados_movimentacao[1])
            self.tela_principal.msg('Sucess', 'Relatório criado com sucesso!', 'information')
        except Exception as e:
            self.tela_principal.msg('Error', e, 'warning')
