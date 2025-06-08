from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.core import MessageFactory

class VerPedidosDialog(ComponentDialog):
    def __init__(self):
        super(VerPedidosDialog, self).__init__("VerPedidosDialog")

        self.add_dialog(
            WaterfallDialog(
                "fluxoVerPedidos",
                [
                    self.exibir_mensagem_inicial
                ],
            )
        )

        self.initial_dialog_id = "fluxoVerPedidos"

    async def exibir_mensagem_inicial(self, contexto_passos: WaterfallStepContext):
        # Mensagem inicial informando que a consulta foi iniciada
        await contexto_passos.context.send_activity(
            MessageFactory.text("🔎 Consulta de pedidos iniciada. Em breve você poderá ver seus pedidos.")
        )
        return await contexto_passos.end_dialog()
