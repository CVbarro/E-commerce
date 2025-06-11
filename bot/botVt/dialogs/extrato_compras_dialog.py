from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.core import MessageFactory, CardFactory
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.schema import HeroCard
from api.pedido_api import PedidoAPI
import requests
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

        usuario_id = self.obter_usuario_id_por_email(email_usuario)
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
            data_iso = pedido.get("dataPedido", "")
            try:
                data_formatada = datetime.fromisoformat(data_iso).strftime("%d/%m/%Y %H:%M")
            except:
                data_formatada = data_iso

            endereco = pedido.get("enderecoEntrega", {})
            endereco_str = (
                f"{endereco.get('logradouro', '')}, {endereco.get('numero', '')}, "
                f"{endereco.get('bairro', '')} - {endereco.get('cidade', '')}"
            )

            itens = pedido.get("itens", [])
            valor_pedido = sum(item.get("precoUnitario", 0.0) * item.get("quantidade", 1) for item in itens)
            total_valor += valor_pedido

            produtos_texto = ""
            for item in itens:
                nome = item.get("nomeProduto", "Produto")
                qtd = item.get("quantidade", 1)
                valor = item.get("precoUnitario", 0.0)
                produtos_texto += f"- {qtd}x {nome} — R$ {valor:.2f} cada\n"

            resumo = (
                f"📦 *Data:* {data_formatada}\n"
                f"📍 *Endereço:* {endereco_str}\n\n"
                f"🛒 *Itens:*\n{produtos_texto}\n"
                f"💰 *Total do pedido:* R$ {valor_pedido:.2f}"
            )

            card = HeroCard(
                title="🧾 Pedido",
                subtitle=f"Realizado em {data_formatada}",
                text=resumo
            )

            await step_context.context.send_activity(
                MessageFactory.attachment(CardFactory.hero_card(card))
            )

        await step_context.context.send_activity(
            MessageFactory.text(f"💳 *Valor total de todas as compras:* R$ {total_valor:.2f}")
        )

        return await step_context.end_dialog()

    def obter_usuario_id_por_email(self, email):
        try:
            resp = requests.get("http://localhost:8080/users/buscar-por-email", params={"email": email})
            if resp.status_code == 200:
                return str(resp.text)
        except Exception as e:
            print("Erro ao buscar usuário por e-mail:", e)
        return None
