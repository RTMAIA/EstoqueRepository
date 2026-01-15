from pydantic import ValidationError, BaseModel, Field, field_validator, ValidationInfo
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

    @field_validator("nome", "marca")
    @classmethod
    def valida_campo(cls, valor, info: ValidationInfo):
        if valor is None:
            raise ValueError(f'{info.field_name} não pode ser vazio.')
        if valor.isdigit():
            raise ValueError(f'{info.field_name} não pode conter apenas números.')
        if valor is not None and (len(valor) < 3 or len(valor) > 50):
            raise ValueError(f'O {info.field_name} deve ter pelos menos 3 caracteres ou menos de 50 caracteres.')
        return valor
        
    @field_validator("valor_unitario")
    @classmethod
    def valida_valor_unitario(cls, valor):
        if valor is not None and valor <= 0:
         raise ValueError('O Valor Unitario deve ser maior que 0.')    
        return valor
    

class CategoriaValidation(BaseModel):
    nome: str = Field(min_length=3, max_length=50)

class EstoqueValidation(BaseModel):
    id_produto: int | None = None
    quantidade: int | None = None
    estoque_minimo: int | None = None

    @field_validator('id_produto', 'quantidade', 'estoque_minimo')
    @classmethod

    def valida_campo(cls, valor, info: ValidationInfo):
        if valor is not None and valor < 0:
            raise ValueError(f'O campo {info.field_name} deve ser maior que zero.')
        if not isinstance(valor, int):
            raise ValueError(f'O campo {info.field_name} deve ser um inteiro.')
        

class MovimentacaoValidation(BaseModel):
    data: date
    tipo_movimento: str
    id_produto: int
    valor_unitario: Decimal = Field(gt=0)
    quantidade: int = Field(gt=0)
    valor_total: Decimal = Field(gt=0)