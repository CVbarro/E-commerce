class CartaoCredito:
    def __init__(
        self,
        numero: str,
        dt_expiracao: str,
        cvv: str,
        saldo: float
    ):
        self.numero = numero
        self.dt_expiracao = dt_expiracao
        self.cvv = cvv
        self.saldo = saldo
