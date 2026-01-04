from sqlalchemy import select, desc
from model.repository.base_repository import BaseRepository
from model.model import *
from database.database import get_session
from model.validators.validators import *

session = next(get_session())

repoProduto = BaseRepository(session, Produtos)
repoCategoria = BaseRepository(session, Categorias)
repoEstoque = BaseRepository(session, Estoque)
repoMovimentacao = BaseRepository(session, Movimentacao)

def serializar(obj):
            dados = [{'id_categoria':i.categoria.nome ,'nome': i.nome, 'marca': i.marca, 'sku': i.sku, 'valor_unitario': f'{i.valor_unitario:.2f}'} for i in obj]
            return dados

class GenericService():
    def __init__(self, repo):
        self.repo = repo

    def _validate(self, **kwargs):
           return kwargs
    
    def _validar_campos_permitidos(self, campos_permitidos, **kwargs):
            for i in kwargs:
              if not i in campos_permitidos:
                raise ValueError(f'Campo "{i}" não permitido.')
            return kwargs

    def criar(self, **kwargs):
            obj = self.repo.criar(**kwargs)
            return obj
    
    def buscar_todos(self):
            obj = self.repo.buscar_todos()
            return obj
    
    def buscar_por_id(self, id):
            obj = self.repo.buscar_por_id(id)
            return obj
    
    def update(self, id, **kwargs):
          obj = self.repo.update(id, **kwargs)
          return obj
    
    def delete(self, id):
          obj = self.repo.delete(id)
          return obj
    
    def filtrar(self, campo, valor):
        
        obj = session.scalars(select(Produtos).where(getattr(Produtos, campo).like(f'{valor}%'))).all()
        return obj
    
class CategoriaService(GenericService):
        campos_permitidos = ['nome']

        def __init__(self, repo):
              super().__init__(repo)

        def existe_categoria(self, nome):
              obj = session.scalar(select(Categorias).where(nome == Categorias.nome))
              if not obj:
                    raise ValueError(f'Categoria "{nome}" não existe.')
              return obj.id

class ProdutoService(GenericService):
        def __init__(self, repo_produto, categoria_service):
            self.campos_permitidos = ['nome', 'marca', 'id_categoria', 'valor_unitario']
            self.categoria_service = categoria_service
            super().__init__(repo_produto)

        def _gerar_sku(self, **kwargs):
            sku = f'{kwargs['nome'][0:3]}-{kwargs['marca'][0:3]}-{kwargs['id_categoria'][0:3]}-N01'.upper()
            obj = session.scalars(select(Produtos).where(Produtos.sku.like(f'{sku[0:11]}%')).order_by(desc(Produtos.sku))).first()
            if not obj:
                return (sku)
            sku = obj.sku[0:13] + str(f'{int(obj.sku[13:16]) + 1:02d}')
            return sku
                       
        def _validate(self, **kwargs):
            if kwargs['id_categoria']:
                if CategoriaValidation(**kwargs):
                    id = self.categoria_service.existe_categoria(nome=kwargs['id_categoria'])
                    sku = self._gerar_sku(**kwargs)
                    kwargs['sku'] = sku
                    kwargs['id_categoria'] = id
                    kwargs['is_active'] = True
            if ProdutoValidation(**kwargs):
                    return kwargs
            
        def criar(self, **kwargs):
                dados = self._validar_campos_permitidos(self.campos_permitidos, **kwargs)
                dados = self._validate(**dados)
                return super().criar(**dados)

        def buscar_todos(self):
              return super().buscar_todos()
        
        def buscar_por_id(self, id):
              return super().buscar_por_id(id)

        def filtrar(self, campo, valor):
              return super().filtrar(campo=campo, valor=valor)
        
        def filtrar_por_categoria(self, categoria):
            obj = session.scalars(select(Produtos).join(Produtos.categoria).where(Categorias.nome.like(f'{categoria}%')).filter(Produtos.is_active == True)).all()
            return obj
        
        def filtrar_por_nome(self, nome):
            obj = session.scalars(select(Produtos).where(Produtos.nome.like(f'{nome}%')).filter(Produtos.is_active == True)).all()
            return obj
        
        def filtrar_por_sku(self, sku):
              obj = session.scalars(select(Produtos).where(Produtos.sku.like(f'%{sku}%')).filter(Produtos.is_active == True)).all()
              return obj
        

categoria_service = CategoriaService(repoCategoria)
a = ProdutoService(repoProduto, categoria_service)
print(a.filtrar_por_sku('raf-mai'))
