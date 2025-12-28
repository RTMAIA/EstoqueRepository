from model.service.service import *
from model.service.service import repoProduto
from model.validators.validators import *
from database.database import get_session

session = next(get_session())

class ProdutosController():
    def __init__(self):
        categoria_service = CategoriaService(repoCategoria)
        self.service_produto = ProdutoService(repoProduto, categoria_service)

    def criar_produto(self, **kwargs):
        return self.service_produto.criar(**kwargs)
    
    def buscar_todos(self):
        return self.service_produto.buscar_todos()
    
    def buscar_por_id(self, id):
        return self.service_produto.buscar_por_id(id)

    def update(self, id, **kwargs):
        return self.service_produto.update(id, **kwargs)
    
    def delete(self, id):
        return self.service_produto.delete(id)

class CategoriasControler():
    ...

class EstoqueController():
    ...

class movimentacaoController():
    ...
