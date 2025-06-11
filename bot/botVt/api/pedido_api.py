import requests

class PedidoAPI:
    BASE_URL = "http://ecommerce-api-g4fbecf2f3fxa5b4.centralus-01.azurewebsites.net/pedidos"

    @staticmethod
    def criar_pedido(dados_pedido):
        try:
            resp = requests.post(PedidoAPI.BASE_URL, json=dados_pedido)
            return resp.status_code, resp.json()
        except Exception:
            return resp.status_code, resp.text

    @staticmethod
    def listar_todos_pedidos():
        try:
            resp = requests.get(PedidoAPI.BASE_URL)
            return resp.status_code, resp.json()
        except Exception:
            return resp.status_code, resp.text

    @staticmethod
    def buscar_pedidos_por_usuario(usuario_id):
        url = f"{PedidoAPI.BASE_URL}/usuario/{usuario_id}"
        try:
            resp = requests.get(url)
            return resp.status_code, resp.json()
        except Exception:
            return resp.status_code, resp.text

    @staticmethod
    def deletar_pedido(usuario_id, pedido_id):
        url = f"{PedidoAPI.BASE_URL}/{usuario_id}/{pedido_id}"
        try:
            resp = requests.delete(url)
            return resp.status_code, resp.text
        except Exception as e:
            return 500, f"Erro ao deletar pedido: {e}"
