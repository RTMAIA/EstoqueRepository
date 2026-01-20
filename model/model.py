from sqlalchemy import String, Integer, Column, ForeignKey, DateTime, func, DECIMAL, Boolean, select
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class Categorias(Base):
    __tablename__ = 'categorias'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(50))

class Produtos(Base):
    __tablename__ = 'produtos'

    id: Mapped[int] =  mapped_column(Integer, primary_key=True, autoincrement=True)
    id_categoria: Mapped[int] = mapped_column(Integer, ForeignKey('categorias.id'))
    sku: Mapped[str] = mapped_column(String(15), unique=True)
    marca: Mapped[str] = mapped_column(String(15))
    nome: Mapped[str] = mapped_column(String(50))
    valor_unitario: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean)

    categoria: Mapped['Categorias'] = relationship('Categorias')

    def __init__(self, id_categoria,sku, marca, nome, valor_unitario, is_active):
        self.id_categoria = id_categoria
        self.sku = sku
        self.marca = marca
        self.nome = nome
        self.valor_unitario = valor_unitario
        self.is_active = is_active
       
            
class Estoque(Base):
    __tablename__ = 'estoque'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_produto: Mapped[int] = mapped_column(Integer, ForeignKey('produtos.id'))
    quantidade: Mapped[int] = mapped_column(Integer)
    estoque_minimo: Mapped[int] = mapped_column(Integer)

    produto: Mapped['Produtos'] = relationship('Produtos')

class Movimentacao(Base):
    __tablename__ = 'movimentacao'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    data: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    tipo_movimentacao: Mapped[str] = mapped_column(String(7))
    origem: Mapped[str] = mapped_column(String(13))
    id_produto: Mapped[int] = mapped_column(Integer, ForeignKey('estoque.id'))
    nome: Mapped[str] = mapped_column(String(50))
    categoria: Mapped[str] = mapped_column(String(50))
    marca: Mapped[str] = mapped_column(String(50))
    sku: Mapped[str] = mapped_column(String(15))
    valor_unitario: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), nullable=False)
    quantidade: Mapped[int] = mapped_column(Integer)
    valor_total: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), nullable=False)

    produto: Mapped['Estoque'] = relationship('Estoque')
