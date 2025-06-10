class EnderecoUsuario:
    def __init__(
        self,
        logradouro: str,
        complemento: str,
        bairro: str,
        cidade: str,
        estado: str,
        cep: str
    ):
        self.logradouro = logradouro
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.cep = cep
