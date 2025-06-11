from botbuilder.core import ActivityHandler, ConversationState, TurnContext, UserState
from botbuilder.dialogs import Dialog
from helpers.dialog_helper import DialogHelper

class AtendimentoBot(ActivityHandler):
    """
    Bot responsável por conduzir o fluxo de atendimento, controlando mensagens, estados e interações com o usuário.
    """

    def __init__(
        self,
        estado_conversa: ConversationState,
        estado_usuario: UserState,
        fluxo_dialogo: Dialog,
    ):
        if estado_conversa is None:
            raise TypeError(
                "Erro ao iniciar o bot: o estado da conversa não foi fornecido."
            )
        if estado_usuario is None:
            raise TypeError(
                "Erro ao iniciar o bot: o estado do usuário é obrigatório."
            )
        if fluxo_dialogo is None:
            raise Exception("Erro de inicialização: o fluxo de diálogo está ausente.")

        self.estado_conversa = estado_conversa
        self.estado_usuario = estado_usuario
        self.fluxo_dialogo = fluxo_dialogo

    async def on_turn(self, turn_context: TurnContext):
        # Executa o processamento padrão de cada turno e salva o estado
        await super().on_turn(turn_context)
        await self.estado_conversa.save_changes(turn_context)
        await self.estado_usuario.save_changes(turn_context)

    async def on_message_activity(self, turn_context: TurnContext):
        # Dispara ou continua o diálogo com base na mensagem recebida
        await DialogHelper.run_dialog(
            self.fluxo_dialogo,
            turn_context,
            self.estado_conversa.create_property("EstadoDoDialogo"),
        )

    async def on_members_added_activity(self, members_added, turn_context: TurnContext):
        # Envia uma mensagem de boas-vindas a novos usuários no chat
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    "👋 Olá! Bem-vindo(a) ao assistente virtual do nosso ecommerce. "
                    "Estou aqui para ajudar você. Digite qualquer mensagem para começarmos o atendimento!"
                )

        await DialogHelper.run_dialog(
            self.fluxo_dialogo,
            turn_context,
            self.estado_conversa.create_property("EstadoDoDialogo"),
        )