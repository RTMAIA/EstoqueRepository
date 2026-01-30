from database.database import get_session
from model.repository.base_repository import *
from model.model import *


session = next(get_session())

repoProduto = BaseRepository(session, Produtos)
repoCategoria = BaseRepository(session, Categorias)
repoEstoque = BaseRepository(session, Estoque)
repoMovimentacao = BaseRepository(session, Movimentacao)