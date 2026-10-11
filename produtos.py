def cadastrar_produtos():
    produtos = []

    nome = input("Digite o nome do produto: ")
    preco = float(input("Digite o preco do produto: "))
    quantidade = int(input("Digite a quantidade do produto: "))

    produto = {
        "nome": nome,
        "preco": preco,
        "quantidade": quantidade
    }
    produtos.append(produto)

    print("Cadastrando produtos")