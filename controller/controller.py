from model.service.service import Service
from model.service.service import repoProduto
from model.validators.validators import *
from database.database import get_session

session = next(get_session())

class ProdutosController():
    def __init__(self):
    # Fazer o restante do crud para o controller
        self.service = Service(session=session)

    def criar_produto(self, **kwargs):
        sku = self.service.gerar_sku(**kwargs)
        if CategoriaValidation(**kwargs):
            id = self.service.exists_categoria(kwargs['id_categoria'])
            kwargs['id_categoria'] = id
            kwargs['sku'] = sku
            if ProdutoValidation(**kwargs):
                repoProduto.criar(**kwargs)
    
    def buscar_todos(self):
        return self.service.buscar_todos()
    
    def buscar_por_id(self, id):
        return self.service.buscar_por_id(id)

    def update(self, id, **kwargs):
        return repoProduto.update(id, **kwargs)

class CategoriasControler():
    ...

class EstoqueController():
    ...

class movimentacaoController():
    ...

a = ProdutosController()
# a.criar_produto(nome='rafael', marca='maia', id_categoria='PESSOA', valor_unitario=1)
# print(a.buscar_por_id(1))
# print(a.buscar_por_id(17))

