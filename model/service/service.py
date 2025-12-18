from sqlalchemy import select, desc
from model.repository.base_repository import BaseRepository
from model.model import *
from database.database import get_session

session = next(get_session())

repoProduto = BaseRepository(session, Produtos)
repoCategoria = BaseRepository(session, Categorias)
repoEstoque = BaseRepository(session, Estoque)
repoMovimentacao = BaseRepository(session, Movimentacao)



class Service():
    def __init__(self, session):
        self.session = session

    def gerar_sku(self, **kwargs) -> str:
            param = ['id_categoria', 'nome', 'marca']
            variacao = 'N01'
            for i in kwargs:
                if i in param:
                    if not len(kwargs[i]) >= 3:
                        raise ValueError(f'O campo "{i}" Deve maior ou igual a 3.')
            sku = (kwargs['nome'][0:3] + '-' + kwargs['marca'][0:3] + '-' + kwargs['id_categoria'][0:3] + '-' + variacao).upper()
            obj = self.session.scalar(select(Produtos).where(Produtos.sku.like(f'{sku[0:11]}%')).order_by(desc(Produtos.sku)))
            if not obj:
                return sku
            sku = f'{obj.sku[0:12]}{obj.sku[12:13]}{int(obj.sku[13:15]) + 1:02d}'
            return sku

    def exists_categoria(self,nome):
        obj = self.session.scalar(select(Categorias).where(Categorias.nome == nome))
        if obj:
            return obj.id
        raise NameError('Categoria não existe.')