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

def converter_obj_dict(obj):
            dados = [{'id_categoria':i.categoria.nome ,'nome': i.nome, 'marca': i.marca, 'sku': i.sku, 'valor_unitario': f'{i.valor_unitario:.2f}'} for i in obj]
            return dados

class GenericService():
    def __init__(self, repo):
        self.repo = repo

    def _validate_create(self, **kwargs):
            return kwargs
    
    def _validate_update(self, **kwargs):
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
        def __init__(self, repo):
              super().__init__(repo)

        def criar(self, **kwargs):
            if CategoriaValidation(**kwargs):
                if self.existe_categoria(kwargs['nome']):
                    return super().criar(**kwargs)
                
        def buscar_por_id(self, id):
            return super().buscar_por_id(id)

        def buscar_por_nome(self, nome):
             id = self.retornar_id(nome)
             obj = self.buscar_por_id(id)
             return obj[0]
        
        def update(self, id, **kwargs):
            obj = session.scalar(select(Categorias).where(kwargs['nome'] == Categorias.nome))
            if not obj:
                return super().update(id, **kwargs)
            raise ValueError(f'Cateogria {kwargs['nome']} já existe.')
            
        def delete(self, id):
            obj = self.buscar_por_id(id)
            print(obj)
            if obj:
                 session.delete(obj[0])
                 session.commit()
                 return 'A categoria foi deletada.'
            raise ValueError(f'A categoria não existe.')

        def existe_categoria(self, nome):
            obj = session.scalar(select(Categorias).where(nome == Categorias.nome))
            if not obj:
                return nome
            raise ValueError(f'A categoria {nome} já existe.')

        def retornar_id(self, nome):
            obj = session.scalar(select(Categorias).where(nome == Categorias.nome))
            if not obj:
                raise ValueError(f'Categoria "{nome}" não existe.')
            return obj.id
        
class ProdutoService(GenericService):
        def __init__(self, repo_produto, categoria_service):
            self.campos_permitidos = ['nome', 'marca', 'categoria', 'valor_unitario']
            self.categoria_service = categoria_service
            super().__init__(repo_produto)

        def _gerar_sku(self, **kwargs):
            sku = f'{kwargs['nome'][0:3]}-{kwargs['marca'][0:3]}-{kwargs['id_categoria'][0:3]}-N01'.upper()
            obj = session.scalars(select(Produtos).where(Produtos.sku.like(f'{sku[0:11]}%')).order_by(desc(Produtos.sku))).first()
            if not obj:
                return (sku)
            sku = obj.sku[0:13] + str(f'{int(obj.sku[13:16]) + 1:02d}')
            return sku
                       
        def _validate_create(self, **kwargs):
            if kwargs['categoria']:
                if CategoriaValidation(**kwargs):
                    id = self.categoria_service.retornar_id(nome=kwargs['categoria'])
                    sku = self._gerar_sku(**kwargs)
                    print(f'aqui é o dict antigo {kwargs}')
                    novo_dado = kwargs.pop('categoria')
                    kwargs['sku'] = sku
                    kwargs['id_categoria'] = id
                    kwargs['is_active'] = True
                    print(f'aqui é o dict novo {kwargs}')
            if ProdutoCreateValidation(**kwargs):
                    return kwargs
            
        def _validate_update(self, **kwargs):
            if 'id_categoria' in kwargs:
                if CategoriaValidation(**kwargs):
                    id = self.categoria_service.retornar_id(nome=kwargs['categoria'])
                    dado_deletado = kwargs.pop['categoria']
                    kwargs['id_categoria'] = id
            if ProdutoUpdateValidation(**kwargs):
                return kwargs
    
        def criar(self, **kwargs):
                dados = self._validar_campos_permitidos(self.campos_permitidos, **kwargs)
                dados = self._validate_create(**dados)
                return super().criar(**dados)

        def buscar_todos(self):
              return super().buscar_todos()
        
        def buscar_por_id(self, id):
              obj = session.scalars(select(Produtos).where(id == Produtos.id).filter(Produtos.is_active == True)).all()
              if not obj:
                   raise ValueError('O produto não existe ou está inativo.')
              return obj

        def filtrar_por_categoria(self, categoria):
            obj = session.scalars(select(Produtos).join(Produtos.categoria).where(Categorias.nome.like(f'{categoria}%')).filter(Produtos.is_active == True)).all()
            return obj
        
        def filtrar_por_nome(self, nome):
            obj = session.scalars(select(Produtos).where(Produtos.nome.like(f'{nome}%')).filter(Produtos.is_active == True)).all()
            return obj
        
        def filtrar_por_sku(self, sku):
              obj = session.scalars(select(Produtos).where(Produtos.sku.like(f'%{sku}%')).filter(Produtos.is_active == True)).all()
              return obj
        
        def update(self, id, **kwargs):
            try:
                dados_validados = self._validate_update(**kwargs)
                obj = self.buscar_por_id(id)
                for i in dados_validados:
                    setattr(obj[0], i, dados_validados[i])
                dados_sku = {'nome': obj[0].nome, 'marca': obj[0].marca, 'id_categoria': obj[0].categoria.nome}
                dados_chave = set({'nome', 'marca', 'id_categoria'})
                if dados_chave.intersection(dados_validados.keys()):
                    sku = self._gerar_sku(**dados_sku)
                    obj[0].sku = sku
                    session.commit()
                return obj
            except Exception as e:
                session.rollback()
                raise Exception(f'Erro: {e}')

        def delete(self, id):
            obj = self.buscar_por_id(id)
            obj[0].is_active = False
            session.commit()
            return f'Produto {obj[0].nome} Apagado com sucesso.'

class MovimentacaoService(GenericService):
    def __init__(self, repo):
        super().__init__(repo)

    def criar(self, **kwargs):
         return super().criar(**kwargs)
    
     
mov = MovimentacaoService(repoMovimentacao)
mov.criar(tipo_movimentacao='ENTRADA', id_produto=1, valor_unitario=12, quantidade=10, valor_total=1200)

