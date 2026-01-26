from sqlalchemy import select, desc, and_, extract
from model.repository.base_repository import BaseRepository
from model.model import *
from database.database import get_session
from model.validators.validators import *
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from datetime import datetime

session = next(get_session())

repoProduto = BaseRepository(session, Produtos)
repoCategoria = BaseRepository(session, Categorias)
repoEstoque = BaseRepository(session, Estoque)
repoMovimentacao = BaseRepository(session, Movimentacao)


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
    
    def filtrar(self, model, campo, valor):
        obj = session.scalars(select(model).where(getattr(model, campo).like(f'{valor}%'))).all()
        return obj
    
class CategoriaService(GenericService):
        def __init__(self, repo):
              self.campos_permitidos = ['nome']
              super().__init__(repo)
        
        def _validate_create(self, **kwargs):
            if CategoriaValidation(**kwargs):
                if self.existe_categoria(kwargs['nome']):
                    return super()._validate_create(**kwargs)

        def criar(self, **kwargs):
            dados = self._validar_campos_permitidos(self.campos_permitidos, **kwargs)
            dados = self._validate_create(**dados)
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
            sku = f'{kwargs['nome'][0:3]}-{kwargs['marca'][0:3]}-{kwargs['categoria'][0:3]}-N01'.upper()
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
        
        def filtrar_por_marca(self, marca):
             obj = session.scalars(select(Produtos).where(Produtos.marca.like(f'{marca}%')).filter(Produtos.is_active == True)).all()
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

class EstoqueService(GenericService):
    def __init__(self, repo, produto_service, movimentacao_service):
        self.campos_permitidos = ['id_produto', 'quantidade', 'estoque_minimo']
        self.produto_service = produto_service
        self.movimentacao_service = movimentacao_service
        super().__init__(repo)

    def _validate_create(self, **kwargs):
        if EstoqueValidation(**kwargs):
            id_estoque = self._buscar_estoque_por_id_produto(id_produto=kwargs['id_produto'])
            _ = self.produto_service.buscar_por_id(id=id_estoque)
            return super()._validate_create(**kwargs)

    def _atualizar_produto_e_registrar(self, id, origem, **kwargs):
        try:
            if EstoqueValidation(**kwargs):
                _ = self._validar_campos_permitidos(self.campos_permitidos, **kwargs)
                obj_estoque = self.buscar_por_id(id)
                for i in kwargs:
                    quantidade_anterior = obj_estoque.quantidade
                    setattr(obj_estoque, i, kwargs[i])
                if 'quantidade' in kwargs:
                    dados_payload = self.movimentacao_service._retorna_tipo_e_quantidade(quantidade_anterior=quantidade_anterior, quantidade_atual=obj_estoque.quantidade)
                    payload = self.movimentacao_service._payload_registro(tipo_movimentacao=dados_payload['tipo_movimentacao'], origem=origem,quantidade=dados_payload['diferenca'], obj_estoque=obj_estoque)
                    self.movimentacao_service.criar(**payload)
                session.commit()
        except Exception as e:
             session.rollback()
             raise ValueError(f'erro: {e}')      
                
    def _buscar_estoque_por_id_produto(self, id_produto):  
        obj = session.scalar(select(Estoque).where(id_produto == Estoque.id_produto))
        if obj:
            raise ValueError('O produto já existe no estoque.')
        return id_produto

    def criar(self, **kwargs):
        obj = Estoque(**kwargs)
        session.add(obj)
        session.flush()
        return obj
    
    def adicionar_produto_estoque(self, **kwargs):
        try:
            _ = self._validar_campos_permitidos(self.campos_permitidos, **kwargs)
            dados_validados = self._validate_create(**kwargs)
            obj_estoque = self.criar(**dados_validados)
            payload = self.movimentacao_service._payload_registro(tipo_movimentacao='ENTRADA', origem='SALDO_INICIAL', quantidade=kwargs['quantidade'], obj_estoque=obj_estoque)
            _ = self.movimentacao_service.criar(**payload)
            session.commit()
        except Exception as e:
            session.rollback()
            raise ValueError(f'erro: {e}')

    def ajustar_produto(self, id, **kwargs):
        AJUSTE = 'AJUSTE'
        self._atualizar_produto_e_registrar(id=id, origem=AJUSTE, **kwargs)
    
    def inventario(self, id, **kwargs):
        INVENTARIO = 'INVENTARIO'
        self._atualizar_produto_e_registrar(id=id, origem=INVENTARIO, **kwargs)

    def buscar_por_id(self, id):
        obj = session.scalar(select(Estoque).where(id == Estoque.id))
        if not obj:
            raise ValueError('O produto não existe no estoque.')
        return obj

    def buscar_todos(self):
         return super().buscar_todos()
      
    def filtrar_por_nome(self, **kwargs):
        obj = session.scalars(select(Estoque).join(Estoque.produto).where(Produtos.nome.like(f'{kwargs['nome']}%'))).all()
        return obj
    
    def filtrar_por_categoria(self, **kwargs):
        obj = session.scalars(select(Estoque).join(Estoque.produto).where(and_(Produtos.categoria.has(nome=kwargs['nome']),Categorias.nome.like(f'{kwargs['nome']}%')))).all()
        return obj
    
    def filtrar_por_marca(self, marca):
        obj = session.scalars(select(Estoque).join(Produtos).where(Produtos.marca.like(f'{marca}%'))).all()
        return obj

    def filtrar_por_valor_unitario(self, **kwargs):
        obj = session.scalars(select(Estoque).join(Estoque.produto).where(kwargs['valor_unitario'] == Produtos.valor_unitario)).all()
        return obj
    
    def filtrar_por_sku(self, **kwargs):
        obj = session.scalars(select(Estoque).join(Estoque.produto).where(Produtos.sku.like(f'{kwargs['sku']}%'))).all()
        return obj

class MovimentacaoService(GenericService):
    def __init__(self, repo):
        super().__init__(repo)

    def _payload_registro(self, tipo_movimentacao, origem, quantidade, obj_estoque):
        payload = {
                 'tipo_movimentacao':tipo_movimentacao,
                 'origem': origem,
                 'id_produto': obj_estoque.id_produto,
                 'nome': obj_estoque.produto.nome,
                 'categoria': obj_estoque.produto.categoria.nome,
                 'marca': obj_estoque.produto.marca,
                 'sku': obj_estoque.produto.sku,
                 'valor_unitario': obj_estoque.produto.valor_unitario,
                 'quantidade': quantidade,
                 'valor_total': obj_estoque.produto.valor_unitario * obj_estoque.quantidade
                 }
        return payload

    def _retorna_tipo_e_quantidade(self, quantidade_anterior, quantidade_atual):
        diferenca = quantidade_atual - quantidade_anterior
        if diferenca > 0:
            tipo_movimentacao = 'ENTRADA'
        if diferenca < 0:
            tipo_movimentacao = 'SAIDA'
        if diferenca == 0:
             raise ValueError('A quantidade informada não pode ser igual a quantidade atual do estoque.')
        return {'tipo_movimentacao': tipo_movimentacao, 'diferenca': abs(diferenca)}

    def _filtrar_startwith(self, **kwargs):
        for i in kwargs:
            obj = session.scalars(select(Movimentacao).where(getattr(Movimentacao, i).like(f'{kwargs[i]}%'))).all()  
        return obj
         
    def _query_caracteristicas(self, query_base, filtro_caracteristicas):
        for chave in filtro_caracteristicas:
                query_base = query_base.filter(filtro_caracteristicas[chave] == getattr(Movimentacao, chave))
        return query_base
    
    def _query_datas(self, query_base, filtro_datas):
        for chave in filtro_datas:
            if chave == 'ano':
               ano = 'year'
               query_base = query_base.filter(extract(ano, Movimentacao.data) == filtro_datas[chave])
            if chave == 'mes':
               mes = 'month'
               query_base = query_base.filter(extract(mes, Movimentacao.data) == filtro_datas[chave])

            if chave == 'dia':
               dia = 'day'
               query_base = query_base.filter(extract(dia, Movimentacao.data) == filtro_datas[chave])
        return query_base

    def _query_intervalo(self, query_base, filtro_intervalo):     
        filtro_intervalo_lista = list(set(filtro_intervalo))
        filtro_ativo = False

        if set(['ano_inicial', 'ano_final']).issubset(filtro_intervalo_lista):
            filtro_ativo = True
            ano = 'year'
            query_base = query_base.filter(extract(ano , Movimentacao.data).between(filtro_intervalo['ano_inicial'], filtro_intervalo['ano_final']))

        if set(['mes_inicial', 'mes_final']).issubset(filtro_intervalo_lista):
            filtro_ativo = True
            mes = 'month'
            query_base = query_base.filter(extract(mes , Movimentacao.data).between(filtro_intervalo['mes_inicial'], filtro_intervalo['mes_final']))

        if set(['dia_inicial', 'dia_final']).issubset(filtro_intervalo_lista):
            filtro_ativo = True
            dia = 'day'
            query_base = query_base.filter(extract(dia , Movimentacao.data).between(filtro_intervalo['dia_inicial'], filtro_intervalo['dia_final']))
        if filtro_ativo == True:
            return query_base
        raise ValueError('O intervalo deve ter inicio e fim. Verifique o campo.')
    
    def _converte_obj_para_dict(self, obj):
        obj_dict = {'data': [], 'tipo_movimentacao': [], 'origem': [],'nome': [], 'categoria': [],
                     'marca': [],'sku': [], 'valor_unitario': [], 'quantidade':[], 'valor_total': []}
        for chave in obj_dict:
            for item in obj:
                obj_dict[chave].append(getattr(item, chave))
            
        return obj_dict

    def criar(self, **kwargs):
        obj = Movimentacao(**kwargs)
        session.add(obj)
    
    def buscar_todos(self):
        dados = super().buscar_todos()
        resultado = ResultadoBusca(dados=dados)
        return resultado
    
    def filtrar(self, **kwargs):
        intervalos = ['ano_inicial', 'ano_final', 'mes_inicial', 'mes_final', 'dia_inicial', 'dia_final']
        caracteristicas = ['nome', 'categoria', 'marca', 'sku', 'valor_unitario','tipo_movimentacao', 'origem']           
        datas = ['ano', 'mes','dia']

        campos = intervalos + caracteristicas + datas
        campos_validados = self._validar_campos_permitidos(campos, **kwargs)

        filtros = {'caracteristicas':{} , 'datas':{} , 'intervalos': {}}

        for item in campos_validados:
            if item in caracteristicas:
                filtros['caracteristicas'].update({item: kwargs[item]})
            if item in datas:
                filtros['datas'].update({item: kwargs[item]})
            if item in intervalos:
                filtros['intervalos'].update({item: kwargs[item]})

        query_base = select(Movimentacao)
        if filtros['caracteristicas']:
            query = self._query_caracteristicas(query_base, filtros['caracteristicas'])
        if filtros['datas']:
            query = self._query_datas(query_base, filtros['datas'])
        if filtros['intervalos']:
            query= self._query_intervalo(query_base, filtros['intervalos'])

        dados = session.scalars(query).all()
        resultado = ResultadoBusca(dados=dados, filtros=kwargs)
        print(resultado.gerar_nome())
        return resultado

class RelatorioService:
    def __init__(self, movimentacao_service):
        self.movimentacao_service = movimentacao_service

    def _dataframe_to_list(self, obj_convertido):
        df = pd.DataFrame(obj_convertido)
        df = df.astype(str)
        tabela_dados = [df.columns.tolist()] + df.values.tolist()
        for c, v in enumerate(tabela_dados[0]):
            tabela_dados[0][c] = v.upper()  
        return tabela_dados
    
    def _tabela_estilo(self,  tabela):
        tabela.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                    ('FONTSIZE', (0, 0), (-1, -1), 5),]))

    def gerar_relatorio_pdf(self, obj):
        _ = ResultadoBusca(obj.dados, obj.filtros)
        obj_conv = self.movimentacao_service._converte_obj_para_dict(obj.dados)
        tabela_dados = self._dataframe_to_list(obj_conv)
        nome = _.gerar_nome()
        pdf = SimpleDocTemplate(nome, pagesize=A4, rightMargin=20, leftMargin=20, topMargin=20, BottomMargin=20)
        colWidths = (A4[0] - 15) / len(tabela_dados[0])
        tabela = Table(tabela_dados, colWidths=colWidths)
        _ = self._tabela_estilo(tabela)
        
        pdf.build([tabela])

class ResultadoBusca:
    def __init__(self, dados, filtros=None):
        self.dados = dados
        self.filtros = filtros

    def gerar_nome(self):
        timestamp = int(datetime.now().timestamp())
        data = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        nome = f'Relatorio_{data}'

        if not self.filtros:
            return f'{nome}_GERAL-{data}_{timestamp}.pdf'
        for i in self.filtros:
            if i == 'nome' or i == 'categoria' or i == 'marca' or i == 'sku' or i == 'valor_unitario' or i == 'tipo_movimentacao' or i == 'origem':
                nome += f'_{i.upper()}-' + str(self.filtros[i])
        if 'ano_inicial' in self.filtros and 'ano_final' in self.filtros:
            return f'{nome}_PERIODO-{self.filtros['ano_inicial']}-a-{self.filtros['ano_final']}_{timestamp}.pdf'
        if 'mes_inicial' in self.filtros and 'mes_final' in self.filtros:
            return f'{nome}_PERIODO-{self.filtros['mes_inicial']}-a-{self.filtros['mes_final']}_{timestamp}.pdf'
        if 'dia_inicial' in self.filtros and 'dia_final' in self.filtros:
            return f'{nome}_PERIODO-{self.filtros['dia_inicial']}-a-{self.filtros['dia_final']}_{timestamp}.pdf'
        
# categoria_service = CategoriaService(repoCategoria)
# categoria_service.criar(nome='pessoa')

# produto_service = ProdutoService(repoProduto, categoria_service)
# produto_service.criar(nome='rafael', marca='maia', categoria='pessoa', valor_unitario=2.89)

# movimentacao_service = MovimentacaoService(repoMovimentacao,)
# a = (movimentacao_service.filtrar(nome='rafael', marca='maia', ano_inicial='2026', ano_final='2027'))
# a = movimentacao_service.buscar_todos()


# relatorio_service = RelatorioService(movimentacao_service)
# relatorio_service.gerar_relatorio_pdf(a)

# est = EstoqueService(repoEstoque, produto_service, movimentacao_service)
# print(est.filtrar_por_marca('maia'))
# print(est.ajustar_produto(id=1, quantidade=10))