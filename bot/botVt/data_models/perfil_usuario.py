class PerfilUsuario:
    """
    Representa os dados do usuário no sistema de e-commerce.
    """

    def __init__(
        self,
        nome: str = None,
        email: str = None,
        numero_cartao: str = None,
        data_validade: str = None,
        cvv: str = None,
        saldo: float = 0.0
    ):
        self.nome = nome
        self.email = email
        self.numero_cartao = numero_cartao
        self.data_validade = data_validade
        self.cvv = cvv
        self.saldo = saldo
