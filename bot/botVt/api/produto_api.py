import requests

class ProdutoAPI:
    BASE_URL = "http://localhost:8080/produtos"

    @staticmethod
    def create_produto(data):
        """Cria um novo produto."""
        response = requests.post(ProdutoAPI.BASE_URL, json=data)
        if response.status_code == 201:
            return response.json()
        else:
            return f"Erro ao criar produto: {response.status_code} - {response.text}"

    @staticmethod
    def get_usuario_by_email(email):
        url = f"{ProdutoAPI.BASE_URL}/email/{email}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    @staticmethod
    def get_produto(produto_id):
        """Obtém um produto pelo ID."""
        url = f"{ProdutoAPI.BASE_URL}/{produto_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Produto não encontrado: {response.status_code}"

    @staticmethod
    def get_all_produtos():
        """Obtém todos os produtos."""
        response = requests.get(ProdutoAPI.BASE_URL)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Erro ao buscar produtos: {response.status_code}"

    @staticmethod
    def search_product(produto_nome):
        """Busca produtos pelo nome."""
        url = f"{ProdutoAPI.BASE_URL}/procurar"
        response = requests.get(url, params={"produtoNome": produto_nome})
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return []
        else:
            return f"Erro ao buscar produto por nome: {response.status_code}"

    @staticmethod
    def atualizar_produto(produto_id, data):
        """Atualiza um produto existente pelo ID."""
        url = f"{ProdutoAPI.BASE_URL}/{produto_id}"
        response = requests.put(url, json=data)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return "Produto não encontrado para atualizar"
        else:
            return f"Erro ao atualizar produto: {response.status_code}"

    @staticmethod
    def delete_produto(produto_id):
        """Remove um produto pelo ID."""
        url = f"{ProdutoAPI.BASE_URL}/{produto_id}"
        response = requests.delete(url)
        if response.status_code == 204:
            return "Produto deletado com sucesso"
        elif response.status_code == 404:
            return "Produto não encontrado para deletar"
        else:
            return f"Erro ao deletar produto: {response.status_code}"
