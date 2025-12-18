from model.repository.base_repository import BaseRepository
from model.model import *
from database.database import get_session
from model.validators.validators import *

session = get_session()
next_session = next(session)

base = BaseRepository(next_session, Produtos)

class ProdutosController():
    def __init__(self, **kwargs):
    #     self.kwargs = kwargs
    #     if ProdutoValidation(**kwargs):
    #         base.criar(**kwargs)
        base.gerar_sku(**kwargs)

class CategoriasControoler():
    ...

class EstoqueController():
    ...

class movimentacaoController():
    ...

a = ProdutosController(produto='rafael', marca='maia', categoria='pessoa')
