

class CategoriasControler:
    def __init__(self, categoria_service):
        self.categoria_services = categoria_service

    def _converter_obj(self, obj):
        dados_convertidos = [(i.nome) for i in obj]
        return dados_convertidos

    def criar(self, **kwargs):
        self.categoria_services.criar(**kwargs)

    def update(self, **kwargs):
        self.categoria_services.update(**kwargs)

    def delete(self, id):
        self.categoria_services.delete(id)
    
    def buscar_todos(self):
        obj = self.categoria_services.buscar_todos()
        dados_convertidos = self._converter_obj(obj)
        return dados_convertidos

    def buscar_por_nome(self, nome):
        obj = self.categoria_services.buscar_por_nome(nome)
        dados_convertidos = self._converter_obj(obj)
        return dados_convertidos

class ProdutosController:
    def __init__(self, produto_service):
        self.produto_service = produto_service

    def _converter_obj(self, obj):
        dados_convertidos = [[i.nome, i.marca,
                              i.categoria.nome,
                              i.sku, str(i.valor_unitario)] for i in obj]
        
        return dados_convertidos

    def criar(self, **kwargs):
        self.produto_service.criar(**kwargs)

    def update(self, **kwargs):
        self.produto_service.update(**kwargs)

    def delete(self, **kwargs):
        self.produto_service.delete(**kwargs)

    def buscar_todos(self):
        obj = self.produto_service.buscar_todos()
        dados_convertidos = self._converter_obj(obj)
        return dados_convertidos
    
    def filtrar(self, **kwargs):
        obj = self.produto_service.filtrar(**kwargs)
        dados_convertidos = self._converter_obj(obj)
        return dados_convertidos

class EstoqueController:
    def __init__(self, estoque_service):
        self.estoque_service = estoque_service

    def _converter_obj(self, obj):
        dados_convertidos = [[i.produto.nome, i.produto.marca,
                              i.produto.categoria.nome, i.produto.sku,
                              str(i.produto.valor_unitario)] for i in obj]
        
        return dados_convertidos

    def adicionar_produto_estoque(self, **kwargs):
        self.estoque_service.adicionar_produto_estoque(**kwargs)

    def ajustar_produto(self, id, **kwargs):
        self.estoque_service.ajustar_produto(id, **kwargs)

    def inventario(self, id, **kwargs):\
        self.estoque_service.inventario(id, **kwargs)

    def buscar_todos(self):
        obj = self.estoque_service.buscar_todos()
        dados_convetidos = self._converter_obj(obj)
        return dados_convetidos
    
    def filtrar(self, **kwargs):
        obj = self.estoque_service.filtrar(**kwargs)
        dados_convetidos = self._converter_obj(obj)
        return dados_convetidos

class movimentacaoController:
    def __init__(self, movimentacao_service):
        self.movimentacao_service = movimentacao_service

    def _converter_obj(self, obj):
        dados_convertidos = [[str(i.data), i.tipo_movimentacao,
                              i.origem, i.nome,
                              i.marca, i.categoria,
                              i.sku, str(i.valor_unitario),
                              i.quantidade, str(i.valor_total)] for i in obj.dados]
        
        return dados_convertidos

    def buscar_todos(self):
        obj = self.movimentacao_service.buscar_todos()
        dados_convertidos = self._converter_obj(obj)
        return dados_convertidos
    
    def filtrar(self, **kwargs):
        obj = self.movimentacao_service.filtrar(**kwargs)
        dados_convertidos = self._converter_obj(obj)
        return dados_convertidos

class RelatorioController:
    def __init__(self, relatorio_service):
        self.relatorio_service = relatorio_service
        
    def gerar_relatorio_pdf(self, obj):
        self.relatorio_service.gerar_relatorio_pdf(obj)
