from model.service.service import Service
from model.service.service import repoProduto
from model.validators.validators import *
from database.database import get_session

session = next(get_session())


class ProdutosController():
    # Fazer o restante do crud para o controller

    def criar_produto(self, **kwargs):
        service = Service(session=session)
        sku = service.gerar_sku(**kwargs)
        id = service.exists_categoria(kwargs['id_categoria'])
        kwargs['id_categoria'] = id
        kwargs['sku'] = sku
        if ProdutoValidation(**kwargs):
            repoProduto.criar(**kwargs)
                
        

class CategoriasControler():
    ...

class EstoqueController():
    ...

class movimentacaoController():
    ...

a = ProdutosController()
a.criar_produto(id_categoria='PESSOA', nome='rafael', marca='maia', valor_unitario=1)
