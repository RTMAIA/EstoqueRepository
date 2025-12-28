view {
    ProdutoView() {}

    CategoriaView() {}

    EstoqueView() {}
    
    MovimentacaView() {}
}
    

controller {
     ProdutoController() {
        criar_produto(**kwargs)
        buscar_todos()
        buscar_por_sku(sku)
        filtrar_por_nome(nome)
        filtrar_por_sku(sku)
        deletar_produto(sku)
        }

    CategoriaController() {
        criar_categoria(nome)
        buscar_todos_categoria()
        buscar_por_nome_categoria(nome)
        deletar_categoria(categoria)
    }

    EstoqueController() {
        adicionar_produto_estoque(produto)
        remover_produto_estoque(produto)
        buscar_produto_por_sku_estoque(sku)
        buscar_todos_produtos_estoque()
        filtrar_por_nome(nome)
        filtrar_por_sku(sku)
        }
    
    MovimentacaController() {
        movimentacoes()
        filtrar_por_data()
        filtrar_por_produto(produto)
        filtrar_por_marca(marca)
    }
}

model {
    Produtos()
    Categorias()
    Estoque()
    Movimentacao()
}

Ideia inicial: trata-se de um programa desktop de gestao de estoque onde temos 4 tabelas de que são: categorias, produtos, estoque e movimentacao.

categoria -> a tebela categoria recebe apenas o nome da categoria, um tipo str
categoria terá metodos para criar, buscar, atualizar e remover o crud completo
e metodos de busca

produto -> a tabela produtos recebe alguns parametros como:id, nome, marca, categoria, sku, valor_unitario e is_active sendo eles do tipo int autoincremnt, str para valores nome, marca e sku e float para valor unitario tambem teremos um fk em categorias para amarrar produto com categoria para ser usado posteriormente. ex:produto.categoria.nome
produto terá o crud completo e metodos de busca
is_active para soft delete no produto, para caso de arrependimento ter como retornar o produto 


estoque -> a tabela estoque terá como coluna, id, nome do produto, categoria, quantidade
no estoque entao teremos, estoque com fk em produtos garantido a relacao entre essas tabelas o restante dos dados serao acessados desse forma. ex: estoque.produto.categoria.nome.
tambem tera o crud completo e metodos de buscar mais especificos

movimentao -> colunas relativas a movimentacao,id created_at, nome do produto, quantidade, valor_unitario e valor total
ja movimentacao terá tera os registros de cada movimentacao no estoque desda de a criacao de um produto dentro do estoque até a saida do mesmo. para fins de relatorio
terá tambem o crud completo, mas esse será implementado automaticamente a cada movimentacao feita pelo usuario.
