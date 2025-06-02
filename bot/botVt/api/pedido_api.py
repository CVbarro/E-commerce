import requests

BASE_URL = "http://localhost:8080/pedidos"

def criar_pedido(dados_pedido):
    """
    Envia um novo pedido para a API.
    dados_pedido: dicionário com os campos esperados pelo seu PedidoRequest
    """
    resp = requests.post(BASE_URL, json=dados_pedido)
    try:
        resposta = resp.json()
    except Exception:
        resposta = resp.text
    return resp.status_code, resposta

def listar_todos_pedidos():
    """
    Busca todos os pedidos cadastrados (admin ou listagem geral).
    """
    resp = requests.get(BASE_URL)
    try:
        return resp.status_code, resp.json()
    except Exception:
        return resp.status_code, resp.text

def listar_pedidos_por_usuario(usuario_id):
    """
    Busca todos os pedidos de um usuário específico.
    """
    url = f"{BASE_URL}/usuario/{usuario_id}"
    resp = requests.get(url)
    try:
        return resp.status_code, resp.json()
    except Exception:
        return resp.status_code, resp.text

def deletar_pedido(usuario_id, pedido_id):
    """
    Remove um pedido específico de um usuário.
    """
    url = f"{BASE_URL}/{usuario_id}/{pedido_id}"
    resp = requests.delete(url)
    return resp.status_code, resp.text

# # EXEMPLO DE USO:
# if __name__ == "__main__":
#     # Para criar um pedido, adapte conforme o esperado pelo PedidoRequest do seu Java
#     novo_pedido = {
#         "usuarioId": "usuario-123",
#         "itens": [
#             {
#                 "produtoId": "produto-xyz",
#                 "quantidade": 2
#             }
#         ],
#         "numeroCartao": "1234567890123456",
#         "cvv": "123",
#         "dtExpiracao": "12/26",
#         "endereco": "Rua Teste, 123"
#     }
#     status, resposta = criar_pedido(novo_pedido)
#     print("CRIAR PEDIDO:", status, resposta)

#     # Listar todos os pedidos
#     status, pedidos = listar_todos_pedidos()
#     print("TODOS OS PEDIDOS:", status, pedidos)

#     # Listar pedidos por usuário
#     usuario_id = "usuario-123"
#     status, pedidos_usuario = listar_pedidos_por_usuario(usuario_id)
#     print(f"PEDIDOS DO USUÁRIO ({usuario_id}):", status, pedidos_usuario)

#     # Exemplo de exclusão de um pedido (substitua pelos valores reais)
#     pedido_id = "id-do-pedido-a-excluir"
#     status, del_resp = deletar_pedido(usuario_id, pedido_id)
#     print(f"DELETAR PEDIDO {pedido_id}:", status, del_resp)