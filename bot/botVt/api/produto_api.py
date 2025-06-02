import requests

BASE_URL = "http://localhost:8080/produtos"

def create_produto(data):
    """Cria um novo produto."""
    response = requests.post(BASE_URL, json=data)
    if response.status_code == 201:
        return response.json()
    else:
        return f"Erro ao criar produto: {response.status_code} - {response.text}"

def get_produto(produto_id):
    """Obtém um produto pelo ID."""
    url = f"{BASE_URL}/{produto_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Produto não encontrado: {response.status_code}"

def get_all_produtos():
    """Obtém todos os produtos."""
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Erro ao buscar produtos: {response.status_code}"

# def atualizar_produto(produto_id, data):
#     """Atualiza um produto existente pelo ID."""
#     url = f"{BASE_URL}/{produto_id}"
#     response = requests.put(url, json=data)
#     if response.status_code == 200:
#         return response.json()
#     elif response.status_code == 404:
#         return "Produto não encontrado para atualizar"
#     else:
#         return f"Erro ao atualizar produto: {response.status_code}"

# def delete_produto(produto_id):
#     """Remove um produto pelo ID."""
#     url = f"{BASE_URL}/{produto_id}"
#     response = requests.delete(url)
#     if response.status_code == 204:
#         return "Produto deletado com sucesso"
#     elif response.status_code == 404:
#         return "Produto não encontrado para deletar"
#     else:
#         return f"Erro ao deletar produto: {response.status_code}"

# # Exemplos de uso:
# if __name__ == "__main__":
#     # Exemplo de criação
#     novo_produto = {
#         "produtoNome": "Caneca Personalizada",
#         "produtoCategoria": "Utilidades",
#         "preco": 49.90,
#         "imageUrl": "http://exemplo.com/caneca.png",
#         "produtoDescrisao": "Caneca com estampa personalizada"
#     }
#     criado = create_produto(novo_produto)
#     print("Criado:", criado)

#     # Buscar todos os produtos
#     todos = get_all_produtos()
#     print("Todos:", todos)

#     # Supondo que você tenha o ID do produto criado
#     if isinstance(criado, dict) and "id" in criado:
#         produto_id = criado["id"]

#         # Buscar
#         prod = get_produto(produto_id)
#         print("Produto:", prod)

#         # Atualizar
#         atualizado = atualizar_produto(produto_id, {
#             "produtoNome": "Caneca Nova",
#             "produtoCategoria": "Presentes",
#             "preco": 39.90,
#             "imageUrl": "http://exemplo.com/caneca-new.png",
#             "produtoDescrisao": "Caneca edição especial"
#         })
#         print("Atualizado:", atualizado)

#         # Deletar
#         deletado = delete_produto(produto_id)
#         print("Deletado:", deletado)