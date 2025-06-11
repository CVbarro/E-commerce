from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
    ChoicePrompt,
    PromptOptions,
)
from botbuilder.dialogs.choices import Choice
from botbuilder.core import MessageFactory, UserState

from dialogs.ver_pedidos_dialog import VerPedidosDialog
from dialogs.extrato_compras_dialog import ExtratoComprasDialog
from dialogs.verificar_produtos_dialog import VerificarProdutosDialog
from dialogs.comprar_produto_dialog import ComprarProdutoDialog  # usado indiretamente

class MainDialog(ComponentDialog):
    def __init__(self, estado_usuario: UserState):
        super(MainDialog, self).__init__(MainDialog.__name__)

        # Acessor para armazenar dados do usuário, se necessário
        self.perfil_usuario_accessor = estado_usuario.create_property("PerfilUsuario")

        # Diálogos registrados
        self.add_dialog(VerificarProdutosDialog(estado_usuario))
        self.add_dialog(VerPedidosDialog())
        self.add_dialog(ExtratoComprasDialog())
        self.add_dialog(ComprarProdutoDialog(estado_usuario))  # usado indiretamente

        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))

        self.add_dialog(
            WaterfallDialog(
                "FluxoPrincipal",
                [
                    self.exibir_menu,
                    self.redirecionar_para_dialogo
                ]
            )
        )

        self.initial_dialog_id = "FluxoPrincipal"

    async def exibir_menu(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("📋 O que deseja fazer?"),
                choices=[
                    Choice("🛍️ Consultar Produtos"),
                    Choice("📦 Ver Pedidos"),
                    Choice("📑 Ver Extrato de Compras")
                ],
            )
        )

    async def redirecionar_para_dialogo(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        escolha = step_context.result.value

        if escolha == "🛍️ Consultar Produtos":
            return await step_context.begin_dialog("VerificarProdutosDialog")

        elif escolha == "📦 Ver Pedidos":
            return await step_context.begin_dialog("VerPedidosDialog")

        elif escolha == "📑 Ver Extrato de Compras":
            return await step_context.begin_dialog("VerExtratoDialog")

        await step_context.context.send_activity("❌ Opção inválida.")
        return await step_context.end_dialog()
