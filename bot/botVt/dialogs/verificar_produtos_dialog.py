from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    TextPrompt,
    PromptOptions,
    DialogTurnStatus,
    DialogTurnResult,
)
from botbuilder.core import MessageFactory, UserState, CardFactory
from botbuilder.schema import HeroCard, CardAction, CardImage, ActionTypes
from dialogs.comprar_produto_dialog import ComprarProdutoDialog
from api.produto_api import ProductAPI

class VerificarProdutosDialog(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(VerificarProdutosDialog, self).__init__("VerificarProdutosDialog")

        self.add_dialog(TextPrompt("NomeProdutoPrompt"))
        self.add_dialog(ComprarProdutoDialog(user_state))

        self.add_dialog(
            WaterfallDialog(
                "fluxoVerProduto",
                [
                    self.perguntar_nome_produto,
                    self.apresentar_resultado_busca,
                    self.iniciar_compra_produto
                ]
            )
        )

        self.initial_dialog_id = "fluxoVerProduto"

    async def perguntar_nome_produto(self, passo: WaterfallStepContext):
        # Solicita ao usuário o nome do produto desejado
        mensagem = MessageFactory.text("Digite o nome do item que deseja procurar:")
        opcoes = PromptOptions(
            prompt=mensagem,
            retry_prompt=MessageFactory.text("Não entendi. Por favor, informe o nome do produto.")
        )
        return await passo.prompt("NomeProdutoPrompt", opcoes)

    async def apresentar_resultado_busca(self, passo: WaterfallStepContext):
        termo_pesquisa = passo.result
        await self.exibir_produtos(termo_pesquisa, passo)

        return DialogTurnResult(status=DialogTurnStatus.Waiting)

    async def iniciar_compra_produto(self, passo: WaterfallStepContext):
        acao_usuario = passo.context.activity.value

        if not acao_usuario:
            return await passo.end_dialog()

        if acao_usuario.get("acao") == "comprar":
            id_produto = acao_usuario.get("productId")
            return await passo.begin_dialog("ComprarProdutoDialog", {"productId": id_produto})

        return await passo.end_dialog()

    async def exibir_produtos(self, termo, passo: WaterfallStepContext):
        api = ProductAPI()
        lista_produtos = api.search_product(termo)

        for item in lista_produtos:
            cartao = CardFactory.hero_card(
                HeroCard(
                    title=item["productName"],
                    subtitle=item["productDescription"],
                    text=f"💵 Preço: R$ {item['price']}",
                    images=[CardImage(url=img) for img in item["imageUrl"]],
                    buttons=[
                        CardAction(
                            type=ActionTypes.post_back,
                            title=f"Comprar {item['productName']}",
                            value={"acao": "comprar", "productId": item["id"]}
                        )
                    ]
                )
            )
            await passo.context.send_activity(MessageFactory.attachment(cartao))
