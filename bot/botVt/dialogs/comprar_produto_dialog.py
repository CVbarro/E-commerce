from botbuilder.core import MessageFactory, UserState
from botbuilder.schema import ActivityTypes
import requests
import json
from datetime import datetime
from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    TextPrompt,
    NumberPrompt,
    ConfirmPrompt,
    PromptOptions
)


class ComprarProdutoDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(ComprarProdutoDialog, self).__init__(ComprarProdutoDialog.__name__)

        self.user_state = user_state
        self.BASE_URL = "http://localhost:8080/pedidos"

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(NumberPrompt(NumberPrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))

        self.add_dialog(
            WaterfallDialog(
                "FluxoCompraProduto",
                [
                    self.obter_quantidade_step,
                    self.obter_cartao_step,
                    self.obter_cvv_step,
                    self.obter_validade_step,
                    self.obter_endereco_step,
                    self.confirmar_pedido_step,
                    self.finalizar_pedido_step
                ]
            )
        )

        self.initial_dialog_id = "FluxoCompraProduto"

    async def obter_quantidade_step(self, step_context: WaterfallStepContext):
        # Obtém o ID do produto do diálogo pai
        step_context.values["id_produto"] = step_context.options["productId"]

        # Em um cenário real, você buscaria os detalhes do produto na API
        step_context.values["nome_produto"] = "Produto"  # Placeholder
        step_context.values["preco_produto"] = 0.0  # Placeholder

        mensagem = MessageFactory.text(
            "Por favor, digite a quantidade que deseja comprar:"
        )

        return await step_context.prompt(
            NumberPrompt.__name__,
            PromptOptions(
                prompt=mensagem,
                retry_prompt=MessageFactory.text("Por favor, digite um número válido para a quantidade.")
            )
        )

    async def obter_cartao_step(self, step_context: WaterfallStepContext):
        quantidade = step_context.result
        step_context.values["quantidade"] = quantidade

        # Pede o número do cartão de crédito
        mensagem = MessageFactory.text(
            "Por favor, digite o número do cartão de crédito (sem espaços ou traços):"
        )

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(
                prompt=mensagem,
                retry_prompt=MessageFactory.text("Por favor, digite um número de cartão válido.")
            )
        )

    async def obter_cvv_step(self, step_context: WaterfallStepContext):
        step_context.values["numero_cartao"] = step_context.result

        # Pede o CVV
        mensagem = MessageFactory.text(
            "Por favor, digite o CVV do cartão (os 3 ou 4 números atrás do cartão):"
        )

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(
                prompt=mensagem,
                retry_prompt=MessageFactory.text("Por favor, digite um CVV válido (3 ou 4 dígitos).")
            )
        )

    async def obter_validade_step(self, step_context: WaterfallStepContext):
        step_context.values["cvv"] = step_context.result

        # Pede a data de validade
        mensagem = MessageFactory.text(
            "Por favor, digite a data de validade do cartão (MM/AA):"
        )

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(
                prompt=mensagem,
                retry_prompt=MessageFactory.text("Por favor, digite a data no formato MM/AA.")
            )
        )

    async def obter_endereco_step(self, step_context: WaterfallStepContext):
        step_context.values["validade_cartao"] = step_context.result

        # Pede o endereço de entrega
        mensagem = MessageFactory.text(
            "Por favor, digite o endereço completo para entrega:"
        )

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(
                prompt=mensagem,
                retry_prompt=MessageFactory.text("Por favor, digite um endereço válido.")
            )
        )

    async def confirmar_pedido_step(self, step_context: WaterfallStepContext):
        step_context.values["endereco_entrega"] = step_context.result

        # Mostra resumo e pede confirmação
        resumo = (
            f"📦 Resumo do Pedido:\n\n"
            f"Produto: {step_context.values['nome_produto']}\n"
            f"Quantidade: {step_context.values['quantidade']}\n"
            f"Endereço: {step_context.values['endereco_entrega']}\n\n"
            f"💳 Pagamento com cartão terminado em ...{step_context.values['numero_cartao'][-4:]}\n\n"
            "Confirma a compra?"
        )

        return await step_context.prompt(
            ConfirmPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text(resumo))
        )

    async def finalizar_pedido_step(self, step_context: WaterfallStepContext):
        if step_context.result:
            # Usuário confirmou a compra
            dados_pedido = {
                "usuarioId": "1",  # Deveria vir do estado do usuário
                "itens": [{
                    "produtoId": step_context.values["id_produto"],
                    "quantidade": step_context.values["quantidade"]
                }],
                "numeroCartao": step_context.values["numero_cartao"],
                "cvv": step_context.values["cvv"],
                "dtExpiracao": step_context.values["validade_cartao"],
                "endereco": step_context.values["endereco_entrega"]
            }

            try:
                resposta = requests.post(
                    self.BASE_URL,
                    json=dados_pedido,
                    headers={"Content-Type": "application/json"}
                )

                if resposta.status_code == 201:
                    await step_context.context.send_activity(
                        MessageFactory.text("✅ Pedido realizado com sucesso! Obrigado pela compra!")
                    )
                else:
                    mensagem_erro = resposta.json().get("message", "Erro desconhecido")
                    await step_context.context.send_activity(
                        MessageFactory.text(f"❌ Erro ao processar pedido: {mensagem_erro}")
                    )
            except Exception as erro:
                await step_context.context.send_activity(
                    MessageFactory.text(f"⚠️ Falha na comunicação com o sistema: {str(erro)}")
                )
        else:
            await step_context.context.send_activity(
                MessageFactory.text("❎ Compra cancelada. Você pode tentar novamente quando quiser.")
            )

        return await step_context.end_dialog()