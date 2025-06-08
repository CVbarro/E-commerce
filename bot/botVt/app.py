# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import sys
import traceback
from datetime import datetime
from dotenv import load_dotenv
from aiohttp import web
from aiohttp.web import Request, Response, json_response

from botbuilder.core import (
    BotFrameworkAdapterSettings,
    TurnContext,
    BotFrameworkAdapter,
    ConversationState,
    MemoryStorage,
    UserState,
)
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.schema import Activity, ActivityTypes

from bots.atendimento_bot import AtendimentoBot
from dialogs.main_dialog import MainDialog  # <- seu MainDialog
from config import DefaultConfig

# Carrega variáveis de ambiente (.env)
load_dotenv()
CONFIG = DefaultConfig()

# Configura o adaptador do bot
SETTINGS = BotFrameworkAdapterSettings("", "")
ADAPTER = BotFrameworkAdapter(SETTINGS)

# Tratamento global de erros
async def on_error(context: TurnContext, error: Exception):
    print(f"\n [on_turn_error] unhandled error: {error}", file=sys.stderr)
    traceback.print_exc()

    await context.send_activity("⚠️ O bot encontrou um erro ou bug.")
    await context.send_activity("Por favor, corrija o código fonte para continuar.")

    if context.activity.channel_id == "emulator":
        trace_activity = Activity(
            label="TurnError",
            name="on_turn_error Trace",
            timestamp=datetime.utcnow(),
            type=ActivityTypes.trace,
            value=f"{error}",
            value_type="https://www.botframework.com/schemas/error",
        )
        await context.send_activity(trace_activity)

ADAPTER.on_turn_error = on_error

# ---------------------
# ESTADO E INSTÂNCIAS
# ---------------------

# Armazenamento de estado em memória (pode ser trocado por Cosmos DB no futuro)
MEMORY = MemoryStorage()
CONVERSATION_STATE = ConversationState(MEMORY)
USER_STATE = UserState(MEMORY)

# Instância do diálogo principal
MAIN_DIALOG = MainDialog(USER_STATE)

# Cria o bot com os estados e o diálogo principal
BOT = AtendimentoBot(CONVERSATION_STATE, USER_STATE, MAIN_DIALOG)

# ---------------------
# ROTA PRINCIPAL
# ---------------------

async def messages(req: Request) -> Response:
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return Response(status=415)

    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    response = await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
    if response:
        return json_response(data=response.body, status=response.status)
    return Response(status=201)

# App AIOHTTP
APP = web.Application(middlewares=[aiohttp_error_middleware])
APP.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    try:
        web.run_app(APP, host="localhost", port=CONFIG.PORT)
    except Exception as error:
        raise error
