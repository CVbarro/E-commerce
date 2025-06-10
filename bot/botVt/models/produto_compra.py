class produto_compra:
    """
    Representa as informações necessárias para efetuar a compra de um produto.
    """

    def __init__(
        self,
        id_produto: str,
        numero_cartao: str,
        validade_cartao: str,
        cvv: str
    ):
        self.id_produto = id_produto
        self.numero_cartao = numero_cartao
        self.validade_cartao = validade_cartao
        self.codigo_cvv = cvv
