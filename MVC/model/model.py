from sqlalchemy import String, Integer, Column, ForeignKey, DateTime, func, DECIMAL, select
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class Produtos(Base):
    __tablename__ = 'produtos'

    id: Mapped[int] =  mapped_column(Integer, primary_key=True, autoincrement=True)
    id_categoria: Mapped[int] = mapped_column(Integer, ForeignKey('categorias.id'))
    sku: Mapped[str] = mapped_column(String(15), unique=True)
    marca: Mapped[str] = mapped_column(String(15))
    nome: Mapped[str] = mapped_column(String(50))
    valor_unitario: Mapped[float] = mapped_column(DECIMAL)

    categoria: Mapped['Categorias'] = relationship('Categorias')

    def __init__(self, id_categoria, marca, nome, valor_unitario, session):
        self.id_categoria = id_categoria
        self.sku = self.gerar_sku(session)
        self.marca = marca
        self.nome = nome
        self.valor_unitario = valor_unitario
       

    def gerar_sku(self,session):
        numeracao = 1
        sku = f'{self.marca[:3]}-{self.nome[:3]}'.upper()
        obj = session.execute(select(Produtos).where(Produtos.sku == sku).order_by(Produtos.sku.desc())).scalar()
        if not obj:
            sku = f'{self.marca[:3]}-{self.nome[:3]}-{numeracao:03}'.upper()
        else:
            numeracao = int(obj.sku[8:]) + 1
            sku = f'{self.marca[:3]}-{self.nome[:3]}-{numeracao:03}'.upper()
        return sku.upper()
            

class Categorias(Base):
    __tablename__ = 'categorias'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(50))

class Estoque(Base):
    __tablename__ = 'estoque'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_produto: Mapped[int] = mapped_column(Integer, ForeignKey('produtos.id'))
    quantidade: Mapped[int] = mapped_column(Integer)
    estoque_minimo: Mapped[int] = mapped_column(Integer)

    produto: Mapped['Produtos'] = relationship('Produtos')

class Movimentacao(Base):
    __tablename__ = 'movimentacao'

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(DateTime(timezone=True), server_default=func.now())
    tipo_movimentacao = Column(String(7))
    id_produto = Column(Integer, ForeignKey('estoque.id'))
    valor_unitario = Column(DECIMAL)
    quantidade = Column(Integer)
    valor_total = Column(DECIMAL)
    
    produto: Mapped['Estoque'] = relationship('Estoque')
