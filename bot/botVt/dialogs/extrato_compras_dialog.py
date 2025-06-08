from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.core import MessageFactory
from api.pedido_api import PedidoAPI  # você precisa ter essa classe

class ExtratoComprasDialog(ComponentDialog):
    def __init__(self):
        super(ExtratoComprasDialog, self).__init__("VerExtratoDialog")

        self.add_dialog(
            WaterfallDialog(
                "fluxoExtratoCompra",
                [
                    self.buscar_extrato_usuario,
                ],
            )
        )

        self.initial_dialog_id = "fluxoExtratoCompra"

    async def buscar_extrato_usuario(self, contexto_passos: WaterfallStepContext):
        usuario_id = 1  # depois, pegue do UserState

        pedido_api = PedidoAPI()
        historico = pedido_api.buscar_pedidos_por_usuario(usuario_id)

        if not historico:
            await contexto_passos.context.send_activity(
                MessageFactory.text("📭 Nenhuma compra encontrada no seu histórico.")
            )
            return await contexto_passos.end_dialog()

        mensagem = "📋 *Resumo das suas compras:*\n\n"
        for pedido in historico:
            data = pedido.get("data", "Data não informada")
            endereco = pedido.get("endereco", "Endereço não informado")
            itens = pedido.get("itens", [])
            for item in itens:
                mensagem += f"- 📦 {item['quantidade']}x {item['produto']} em {data} — entregue em {endereco}\n"

        await contexto_passos.context.send_activity(MessageFactory.text(mensagem))
        return await contexto_passos.end_dialog()
