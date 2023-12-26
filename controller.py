from model import *
from populabanco import *
from view import View

class Controller:
    def __init__(self, API):
        self.view = View()
        self.API = API

    def start(self):
        opcao = self.view.start()

        while opcao != 6:
            if opcao == 1: # Usuarios
                token_acesso = self.API.get_app_access_token()
                usuarios = self.API.get_users(token_acesso)

            if opcao == 2: # Canais
                token_acesso = self.API.get_app_access_token()
                canais = self.API.get_canais(token_acesso)

            if opcao == 3: # Categories
                token_acesso = self.API.get_app_access_token()
                top_games = self.API.get_top_games(token_acesso)

            if opcao == 4: # Streams
                token_acesso = self.API.get_app_access_token()
                streams = self.API.get_streams(token_acesso)

            if opcao == 5: # Videos
                token_acesso = self.API.get_app_access_token()
                videos = self.API.get_videos(token_acesso)
            
            opcao = self.view.menu()


if __name__ == "__main__":
    # Obtém o app access token
    token_acesso = API()
    controlador = Controller(token_acesso)
    controlador.start()
    