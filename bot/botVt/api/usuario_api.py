import requests
from decimal import Decimal

class UsuarioAPI:
    BASE_URL = "http://localhost:8080/users"

    @staticmethod
    def _converter_decimals(obj):
        """Converte recursivamente objetos Decimal para float"""
        if isinstance(obj, dict):
            return {key: UsuarioAPI._converter_decimals(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [UsuarioAPI._converter_decimals(item) for item in obj]
        elif isinstance(obj, Decimal):
            return float(obj)
        else:
            return obj

    @staticmethod
    def get_usuario_by_email(email):
        url = f"{UsuarioAPI.BASE_URL}/email/{email}"

        try:
            response = requests.get(url)

            if response.status_code == 200:
                usuario = response.json()

                # Converter todos os valores Decimal para float
                if usuario:
                    usuario = UsuarioAPI._converter_decimals(usuario)

                return usuario

            return None

        except requests.RequestException as e:
            print(f"Erro na requisição: {e}")
            return None
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return None