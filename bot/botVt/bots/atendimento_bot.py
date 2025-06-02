# Copyright (c) Microsoft Corporation. Todos os direitos reservados.
# Licenciado sob a Licença MIT.

from botbuilder.core import ActivityHandler, ConversationState, TurnContext, UserState
from botbuilder.dialogs import Dialog
from helpers.dialog_helper import DialogHelper


class atendimento_bot(ActivityHandler):
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

    async def on_turn(self, contexto: TurnContext):
        # Executa o processamento padrão de cada turno e salva o estado
        await super().on_turn(contexto)
        await self.estado_conversa.save_changes(contexto)
        await self.estado_usuario.save_changes(contexto)

    async def on_message_activity(self, contexto: TurnContext):
        # Dispara ou continua o diálogo com base na mensagem recebida
        await DialogHelper.run_dialog(
            self.fluxo_dialogo,
            contexto,
            self.estado_conversa.create_property("EstadoDoDialogo"),
        )

    async def on_members_added_activity(self, membros_adicionados, contexto: TurnContext):
        # Envia uma mensagem de boas-vindas a novos usuários no chat
        for membro in membros_adicionados:
            if membro.id != contexto.activity.recipient.id:
                await contexto.send_activity(
                    "👋 Olá! Bem-vindo(a) ao assistente virtual do nosso ecommerce. "
                    "Estou aqui para ajudar você. Digite qualquer mensagem para começarmos o atendimento!"
                )
