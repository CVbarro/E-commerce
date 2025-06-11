import requests

class PedidoAPI:
    BASE_URL = "http://localhost:8080/pedidos"

    @staticmethod
    def criar_pedido(dados_pedido):
        resp = requests.post(PedidoAPI.BASE_URL, json=dados_pedido)
        try:
            return resp.status_code, resp.json()
        except Exception:
            return resp.status_code, resp.text

    @staticmethod
    def listar_todos_pedidos():
        resp = requests.get(PedidoAPI.BASE_URL)
        try:
            return resp.status_code, resp.json()
        except Exception:
            return resp.status_code, resp.text

    @staticmethod
    def buscar_pedidos_por_usuario(usuario_id):  # <- nome alterado aqui
        url = f"{PedidoAPI.BASE_URL}/usuario/{usuario_id}"
        resp = requests.get(url)
        try:
            return resp.status_code, resp.json()
        except Exception:
            return resp.status_code, resp.text

    @staticmethod
    def deletar_pedido(usuario_id, pedido_id):
        url = f"{PedidoAPI.BASE_URL}/{usuario_id}/{pedido_id}"
        resp = requests.delete(url)
        return resp.status_code, resp.text
