from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory
from api.pedido_api import PedidoAPI
from api.usuario_api import UsuarioAPI

class VerPedidosDialog(ComponentDialog):
    def __init__(self):
        super(VerPedidosDialog, self).__init__("VerPedidosDialog")

        self.add_dialog(TextPrompt("EmailPrompt"))

        self.add_dialog(
            WaterfallDialog(
                "fluxoVerPedidos",
                [
                    self.solicitar_email_step,
                    self.buscar_pedidos_step
                ],
            )
        )

        self.initial_dialog_id = "fluxoVerPedidos"

    async def solicitar_email_step(self, step_context: WaterfallStepContext):
        mensagem = MessageFactory.text("📧 Por favor, informe seu e-mail para verificar seus pedidos:")
        return await step_context.prompt(
            "EmailPrompt",
            PromptOptions(prompt=mensagem)
        )

    async def buscar_pedidos_step(self, step_context: WaterfallStepContext):
        email = step_context.result
        usuario = UsuarioAPI.get_usuario_by_email(email)

        if not usuario or "id" not in usuario:
            await step_context.context.send_activity(
                MessageFactory.text("❌ Usuário não encontrado com esse e-mail.")
            )
            return await step_context.end_dialog()

        usuario_id = usuario["id"]
        pedido_api = PedidoAPI()
        status_code, pedidos = pedido_api.buscar_pedidos_por_usuario(usuario_id)

        if status_code != 200 or not pedidos:
            await step_context.context.send_activity(
                MessageFactory.text("📭 Nenhum pedido encontrado para esse usuário.")
            )
            return await step_context.end_dialog()

        mensagem = "📦 *Seus pedidos:*\n\n"
        for pedido in pedidos:
            data = pedido.get("data", "Data não informada")
            endereco = pedido.get("endereco", "Endereço não informado")
            mensagem += f"🗓️ {data} - Entrega: {endereco}\n"

            itens = pedido.get("itens", [])
            for item in itens:
                produto = item.get("produto", "Produto desconhecido")
                quantidade = item.get("quantidade", 1)
                mensagem += f"    - {quantidade}x {produto}\n"
            mensagem += "\n"

        await step_context.context.send_activity(MessageFactory.text(mensagem))
        return await step_context.end_dialog()
