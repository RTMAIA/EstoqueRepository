from pydantic import ValidationError, BaseModel, Field
from decimal import Decimal
from datetime import date
import re


class ProdutoValidation(BaseModel):
    id_categoria: int
    sku: str = Field(pattern=r'^[a-zA-Z0-9]{3}\-[a-zA-Z0-9]{3}\-[a-zA-Z0-9]{3}\-[a-zA-Z0-9]{3}')
    marca: str = Field(min_length=3, max_length=50)
    nome: str = Field(min_length=3, max_length=50)
    valor_unitario: Decimal = Field(gt=0)
    is_active: bool

class CategoriaValidation(BaseModel):
    nome: str = Field(min_length=3, max_length=50)

class EstoqueValidation(BaseModel):
    id_produto: int
    quantidade: int = Field(gt=0)
    estoque_minimo: int = Field(gt=0)

class MovimentacaoValidation(BaseModel):
    data: date
    tipo_movimento: str
    id_produto: int
    valor_unitario: Decimal = Field(gt=0)
    quantidade: int = Field(gt=0)
    valor_total: Decimal = Field(gt=0)