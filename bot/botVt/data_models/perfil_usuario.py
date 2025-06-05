class PerfilUsuario:
    """
    Representa os dados cadastrais de um usuário no sistema de e-commerce,
    incluindo informações pessoais, lista de cartões de crédito e endereços vinculados.
    """

    def __init__(
        self,
        nome: str,
        email: str,
        dt_nascimento: str,
        cpf: str,
        telefone: str,
        cartoes: list = None,
        enderecos: list = None
    ):
        self.nome = nome
        self.email = email
        self.dt_nascimento = dt_nascimento
        self.cpf = cpf
        self.telefone = telefone
        self.cartoes = cartoes or []
        self.enderecos = enderecos or []
