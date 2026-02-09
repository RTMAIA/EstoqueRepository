from controller import controller
from model.service import service
from database.context.context import *

categoria = service.CategoriaService(repoCategoria)
produto = service.ProdutoService(repoProduto, categoria)
movimentacao = service.MovimentacaoService(repoMovimentacao)
estoque = service.EstoqueService(repoEstoque, produto, movimentacao)
relatorio = service.RelatorioService(movimentacao)

categoria_controller = controller.CategoriasControler(categoria)
produto_controller = controller.ProdutosController(produto)
estoque_controller = controller.EstoqueController(estoque)
movimentacao_controller = controller.movimentacaoController(movimentacao)
relatorio_controller = controller.RelatorioController(relatorio)
