from pydantic import ValidationError, BaseModel, Field, field_validator
from decimal import Decimal
from datetime import date
import re


class ProdutoCreateValidation(BaseModel):
    id_categoria: int
    sku: str = Field(pattern=r'^[a-zA-Z0-9]{3}\-[a-zA-Z0-9]{3}\-[a-zA-Z0-9]{3}\-[a-zA-Z0-9]{3}')
    marca: str = Field(min_length=3, max_length=50)
    nome: str = Field(min_length=3, max_length=50)
    valor_unitario: Decimal = Field(gt=0)
    is_active: bool

class ProdutoUpdateValidation(BaseModel):
    nome: str | None = None
    marca: str | None = None
    id_categoria: int | None = None
    valor_unitario: Decimal | None = None

    @field_validator("nome")
    @classmethod
    def valida_nome(cls, valor):
        if valor.isdigit():
            raise ValueError('Nome não pode conter apenas números.')
        if valor is not None and len(valor) < 3 or len(valor) > 50:
            raise ValueError('O nome deve ter pelos menos 3 caracteres ou menos de 50 caracteres.')
        return valor
    
    @field_validator("marca")
    @classmethod
    def valida_marca(cls, valor):
        if valor.isdigit():
            raise ValueError('Marca não pode conter apenas números.')
        if valor is not None and len(valor) < 3 or len(valor) > 50:
            raise ValueError('O nome deve ter pelos menos 3 caracteres ou menos de 50 caracteres.')
        return valor
        
    @field_validator("valor_unitario")
    @classmethod
    def valida_valor_unitario(cls, valor):
        if valor is not None and valor <= 0:
         raise ValueError('O Valor Unitario deve ser maior que 0.')    
        return valor
    

class CategoriaValidation(BaseModel):
    id_categoria: str = Field(min_length=3, max_length=50)

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