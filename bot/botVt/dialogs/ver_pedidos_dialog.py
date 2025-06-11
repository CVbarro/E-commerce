from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory
from api.pedido_api import PedidoAPI
from api.usuario_api import UsuarioAPI
from datetime import datetime

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
            await step_context.context.send_activity("❌ Usuário não encontrado com esse e-mail.")
            return await step_context.end_dialog()

        usuario_id = usuario["id"]
        pedido_api = PedidoAPI()
        status_code, pedidos = pedido_api.buscar_pedidos_por_usuario(usuario_id)

        if status_code != 200 or not pedidos:
            await step_context.context.send_activity("📭 Nenhum pedido encontrado para esse usuário.")
            return await step_context.end_dialog()

        for pedido in pedidos:
            data_pedido = pedido.get("dataPedido", "")
            try:
                data_formatada = datetime.fromisoformat(data_pedido).strftime("%d/%m/%Y %H:%M")
            except:
                data_formatada = data_pedido

            endereco = pedido.get("enderecoEntrega", {})
            endereco_str = (
                f"{endereco.get('logradouro', '')}, {endereco.get('numero', '')}, "
                f"{endereco.get('bairro', '')} - {endereco.get('cidade', '')}"
            )

            itens = pedido.get("itens", [])
            itens_texto = ""
            for item in itens:
                nome = item.get("nomeProduto", "Produto desconhecido")
                qtd = item.get("quantidade", 1)
                preco = item.get("precoUnitario", 0.0)
                itens_texto += f"  - {qtd}x {nome} — R$ {preco:.2f}\n"

            resumo = (
                f"🧾 *Pedido realizado em:* {data_formatada}\n"
                f"📍 *Endereço:* {endereco_str}\n"
                f"🛒 *Itens:*\n{itens_texto}\n"
                f"💰 *Total:* R$ {pedido.get('valorTotal', 0.0):.2f}\n"
                "----------------------\n"
            )

            await step_context.context.send_activity(MessageFactory.text(resumo))

        return await step_context.end_dialog()
