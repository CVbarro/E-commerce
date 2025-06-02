from botbuilder.dialogs import Dialog
from botbuilder.core import TurnContext, ConversationState

class DialogHelper:
    @staticmethod
    async def run_dialog(dialog: Dialog, turn_context: TurnContext, conversation_state_property: ConversationState):
        dialog_set = DialogSet(conversation_state_property)
        dialog_set.add(dialog)

        dialog_context = await dialog_set.create_context(turn_context)

        results = await dialog_context.continue_dialog()
        if results.status == DialogTurnStatus.Empty:
            await dialog_context.begin_dialog(dialog.id)
