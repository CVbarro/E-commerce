from botbuilder.dialogs import ComponentDialog
from bot.dialogs.comprar_produto_dialog import ComprarProdutoDialog

class MainDialog(ComponentDialog):
    def __init__(self, user_state):
        super(MainDialog, self).__init__("MainDialog")

        self.add_dialog(ComprarProdutoDialog(user_state))

        self.initial_dialog_id = "ComprarProdutoDialog"
