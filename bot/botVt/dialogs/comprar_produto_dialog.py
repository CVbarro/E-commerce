from botbuilder.core import MessageFactory, UserState
from botbuilder.schema import ActivityTypes
import requests
import json
from datetime import datetime
from decimal import Decimal
from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    TextPrompt,
    NumberPrompt,
    ConfirmPrompt,
    PromptOptions
)

from api.usuario_api import UsuarioAPI


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)


class ComprarProdutoDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(ComprarProdutoDialog, self).__init__(ComprarProdutoDialog.__name__)

        self.user_state = user_state
        self.BASE_URL = "http://ecommerce-api-g4fbecf2f3fxa5b4.centralus-01.azurewebsites.net/pedidos"

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(NumberPrompt(NumberPrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))

        self.add_dialog(
            WaterfallDialog(
                "FluxoCompraProduto",
                [
                    self.obter_email_step,
                    self.obter_quantidade_step,
                    self.obter_cartao_step,
                    self.obter_cvv_step,
                    self.obter_validade_step,
                    self.obter_logradouro_step,
                    self.obter_complemento_step,
                    self.obter_bairro_step,
                    self.obter_cidade_step,
                    self.obter_estado_step,
                    self.obter_cep_step,
                    self.confirmar_pedido_step,
                    self.finalizar_pedido_step
                ]
            )
        )

        self.initial_dialog_id = "FluxoCompraProduto"

    async def obter_email_step(self, step_context: WaterfallStepContext):
        mensagem = MessageFactory.text("🔐 Antes de continuarmos, por favor, digite seu e-mail para login:")
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=mensagem, retry_prompt=MessageFactory.text("❌ E-mail inválido. Tente novamente."))
        )

    async def obter_quantidade_step(self, step_context: WaterfallStepContext):
        email = step_context.result
        usuario = UsuarioAPI.get_usuario_by_email(email)

        if not usuario or "id" not in usuario:
            await step_context.context.send_activity(MessageFactory.text("❌ Não foi possível encontrar o usuário com esse e-mail."))
            return await step_context.end_dialog()

        step_context.values["usuario_id"] = str(usuario["id"])
        step_context.values["id_produto"] = str(step_context.options["productId"])
        step_context.values["nome_produto"] = "Produto"
        step_context.values["preco_produto"] = 0.0

        mensagem = MessageFactory.text("Por favor, digite a quantidade que deseja comprar:")
        return await step_context.prompt(
            NumberPrompt.__name__,
            PromptOptions(prompt=mensagem, retry_prompt=MessageFactory.text("Digite um número válido para a quantidade."))
        )

    async def obter_cartao_step(self, step_context: WaterfallStepContext):
        step_context.values["quantidade"] = step_context.result
        mensagem = MessageFactory.text("Digite o número do cartão de crédito (sem espaços ou traços):")
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=mensagem, retry_prompt=MessageFactory.text("Digite um número de cartão válido."))
        )

    async def obter_cvv_step(self, step_context: WaterfallStepContext):
        step_context.values["numero_cartao"] = step_context.result
        mensagem = MessageFactory.text("Digite o CVV do cartão (3 ou 4 dígitos):")
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=mensagem, retry_prompt=MessageFactory.text("Digite um CVV válido."))
        )

    async def obter_validade_step(self, step_context: WaterfallStepContext):
        step_context.values["cvv"] = step_context.result
        mensagem = MessageFactory.text("Digite a data de validade do cartão (MM/AA):")
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=mensagem, retry_prompt=MessageFactory.text("Digite no formato MM/AA."))
        )

    async def obter_logradouro_step(self, step_context: WaterfallStepContext):
        step_context.values["validade_cartao"] = step_context.result
        mensagem = MessageFactory.text("🏠 Digite o logradouro (ex: Rua Exemplo, 123):")
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=mensagem, retry_prompt=MessageFactory.text("Digite um logradouro válido."))
        )

    async def obter_complemento_step(self, step_context: WaterfallStepContext):
        step_context.values["logradouro"] = step_context.result
        mensagem = MessageFactory.text("📦 Digite o complemento (ex: Apto 101, Bloco B):")
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=mensagem, retry_prompt=MessageFactory.text("Digite um complemento ou 'Nenhum'."))
        )

    async def obter_bairro_step(self, step_context: WaterfallStepContext):
        step_context.values["complemento"] = step_context.result
        mensagem = MessageFactory.text("🏘️ Digite o bairro:")
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=mensagem, retry_prompt=MessageFactory.text("Digite um bairro válido."))
        )

    async def obter_cidade_step(self, step_context: WaterfallStepContext):
        step_context.values["bairro"] = step_context.result
        mensagem = MessageFactory.text("🌆 Digite a cidade:")
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=mensagem, retry_prompt=MessageFactory.text("Digite uma cidade válida."))
        )

    async def obter_estado_step(self, step_context: WaterfallStepContext):
        step_context.values["cidade"] = step_context.result
        mensagem = MessageFactory.text("🗺️ Digite o estado (ex: RJ, SP):")
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=mensagem, retry_prompt=MessageFactory.text("Digite um estado válido."))
        )

    async def obter_cep_step(self, step_context: WaterfallStepContext):
        step_context.values["estado"] = step_context.result
        mensagem = MessageFactory.text("🏷️ Digite o CEP (ex: 12345-678):")
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=mensagem, retry_prompt=MessageFactory.text("Digite um CEP válido."))
        )

    async def confirmar_pedido_step(self, step_context: WaterfallStepContext):
        step_context.values["cep"] = step_context.result

        resumo = (
            f"📦 Resumo do Pedido:\n\n"
            f"Produto: {step_context.values['nome_produto']}\n"
            f"Quantidade: {step_context.values['quantidade']}\n\n"
            f"📍 Endereço:\n"
            f"{step_context.values['logradouro']}, {step_context.values['complemento']}\n"
            f"{step_context.values['bairro']} - {step_context.values['cidade']}/{step_context.values['estado']}\n"
            f"CEP: {step_context.values['cep']}\n\n"
            f"💳 Cartão terminado em ...{step_context.values['numero_cartao'][-4:]}\n\n"
            "Confirma a compra?"
        )

        return await step_context.prompt(
            ConfirmPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text(resumo))
        )

    async def finalizar_pedido_step(self, step_context: WaterfallStepContext):
        if step_context.result:
            usuario_id = int(step_context.values["usuario_id"])
            validade_input = step_context.values["validade_cartao"]

            try:
                validade_convertida = datetime.strptime(validade_input, "%m/%y")
                validade_formatada = validade_convertida.replace(day=10, hour=15, minute=30, second=0).isoformat()
            except ValueError:
                validade_formatada = "2025-06-10T15:30:00"

            dados_pedido = {
                "usuarioId": usuario_id,
                "itens": [{
                    "produtoId": step_context.values["id_produto"],
                    "quantidade": int(step_context.values["quantidade"])
                }],
                "numeroCartao": step_context.values["numero_cartao"],
                "cvv": step_context.values["cvv"],
                "dtExpiracao": validade_formatada,
                "endereco": {
                    "logradouro": step_context.values["logradouro"],
                    "complemento": step_context.values["complemento"],
                    "bairro": step_context.values["bairro"],
                    "cidade": step_context.values["cidade"],
                    "estado": step_context.values["estado"],
                    "cep": step_context.values["cep"]
                }
            }

            try:
                print(f"🔍 URL da API: {self.BASE_URL}")
                print(f"🔍 Dados enviados: {dados_pedido}")

                resposta = requests.post(
                    self.BASE_URL,
                    data=json.dumps(dados_pedido, cls=DecimalEncoder),
                    headers={"Content-Type": "application/json"}
                )

                print(f"🔍 Status Code: {resposta.status_code}")
                print(f"🔍 Resposta da API: {resposta.text}")

                if resposta.status_code in [200, 201]:
                    await step_context.context.send_activity(
                        MessageFactory.text("✅ Pedido realizado com sucesso! Obrigado pela compra!")
                    )
                else:
                    try:
                        erro_json = resposta.json()
                        if isinstance(erro_json, dict):
                            mensagem_erro = erro_json.get("message", f"Erro HTTP {resposta.status_code}")
                        else:
                            mensagem_erro = f"Erro HTTP {resposta.status_code}: {erro_json}"
                    except:
                        mensagem_erro = f"Erro HTTP {resposta.status_code}: {resposta.text}"

                    await step_context.context.send_activity(
                        MessageFactory.text(f"❌ Erro ao processar pedido: {mensagem_erro}")
                    )

                await step_context.context.send_activity("🔁 Digite qualquer coisa para voltar ao menu principal.")
            except Exception as erro:
                print(f"🔍 Exceção capturada: {str(erro)}")
                await step_context.context.send_activity(
                    MessageFactory.text(f"⚠️ Falha na comunicação com o sistema: {str(erro)}")
                )
                await step_context.context.send_activity("🔁 Digite qualquer coisa para voltar ao menu principal.")
        else:
            await step_context.context.send_activity(
                MessageFactory.text("❎ Compra cancelada. Você pode tentar novamente quando quiser.")
            )
            await step_context.context.send_activity("🔁 Digite qualquer coisa para voltar ao menu principal.")

        return await step_context.end_dialog()
