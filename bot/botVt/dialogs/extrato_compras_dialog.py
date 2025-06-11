from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.core import MessageFactory, CardFactory
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.schema import HeroCard
from api.pedido_api import PedidoAPI
from api.usuario_api import UsuarioAPI
from datetime import datetime

class ExtratoComprasDialog(ComponentDialog):
    def __init__(self):
        super(ExtratoComprasDialog, self).__init__("VerExtratoDialog")

        self.add_dialog(TextPrompt(TextPrompt.__name__))

        self.add_dialog(
            WaterfallDialog(
                "fluxoExtratoCompra",
                [
                    self.obter_email_step,
                    self.buscar_extrato_usuario,
                ],
            )
        )

        self.initial_dialog_id = "fluxoExtratoCompra"

    async def obter_email_step(self, step_context: WaterfallStepContext):
        mensagem = MessageFactory.text("🔐 Por favor, informe seu e-mail para consultar o extrato de compras:")
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=mensagem)
        )

    async def buscar_extrato_usuario(self, step_context: WaterfallStepContext):
        email_usuario = step_context.result.strip()

        usuario = UsuarioAPI.get_usuario_by_email(email_usuario)
        usuario_id = usuario.get("id") if usuario else None

        if not usuario_id:
            await step_context.context.send_activity("🚫 E-mail não encontrado no sistema.")
            return await step_context.end_dialog()

        pedido_api = PedidoAPI()
        status_code, historico = pedido_api.buscar_pedidos_por_usuario(usuario_id)

        if status_code != 200 or not historico:
            await step_context.context.send_activity("📭 Nenhum pedido foi encontrado no seu histórico.")
            return await step_context.end_dialog()

        total_valor = 0.0
        await step_context.context.send_activity("📋 *Aqui está o seu extrato de compras:*")

        for pedido in historico:
            card, valor_pedido = self.formatar_pedido_para_card(pedido)
            total_valor += valor_pedido
            await step_context.context.send_activity(
                MessageFactory.attachment(CardFactory.hero_card(card))
            )

        await step_context.context.send_activity(
            MessageFactory.text(f"💳 *Valor total de todas as compras:* R$ {total_valor:.2f}")
        )
        await step_context.context.send_activity("🔁 Digite qualquer coisa para voltar ao menu principal.")
        return await step_context.end_dialog()

       

    def formatar_pedido_para_card(self, pedido):
        data_iso = pedido.get("dataPedido", "")
        try:
            data_formatada = datetime.fromisoformat(data_iso).strftime("%d/%m/%Y %H:%M")
        except Exception as e:
            print(f"Erro ao formatar data: {e}")
            data_formatada = data_iso

        endereco = pedido.get("enderecoEntrega", {})
        endereco_str = (
            f"{endereco.get('logradouro', '')}, {endereco.get('numero', '')}, "
            f"{endereco.get('bairro', '')} - {endereco.get('cidade', '')}"
        )

        itens = pedido.get("itens", [])
        produtos_texto = ""
        valor_total_pedido = 0.0

        for item in itens:
            nome = item.get("nomeProduto", "Produto")
            qtd = item.get("quantidade", 1)
            valor_unit = item.get("precoUnitario", 0.0)
            produtos_texto += f"- {qtd}x {nome} — R$ {valor_unit:.2f} cada\n"
            valor_total_pedido += valor_unit * qtd

        resumo = (
            f"📦 *Data:* {data_formatada}\n"
            f"📍 *Endereço:* {endereco_str}\n\n"
            f"🛒 *Itens:*\n{produtos_texto}\n"
            f"💰 *Total do pedido:* R$ {valor_total_pedido:.2f}"
        )

        card = HeroCard(
            title="🧾 Pedido",
            subtitle=f"Realizado em {data_formatada}",
            text=resumo
        )

        return card, valor_total_pedido
