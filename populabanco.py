import requests
from requests.exceptions import ConnectionError
import logging
from model import * 
from DAO import *
from sqlalchemy import *
from datetime import datetime
from decimal import *
import time

class DB:
    @staticmethod
    def insert(obj):
        try:
            session = DAO.getSession()
            DAO.insert(session, obj)
            session.commit()
            session.close()
            return 1
        except:
            return 0

    @staticmethod
    def select_user(user_id):
        try:
            session = DAO.getSession()
            session.expire_on_commit = False
            user = DAOUser.select(session, user_id) 
            session.commit()
            session.close()
            return user
        except:
            return 0

    @staticmethod
    def selectChannel(channel_id):
        try:
            session = DAO.getSession()
            session.expire_on_commit = False
            channel = DAOChannel.select(session, channel_id)  # Assuming you have a select method in DAOChannel
            session.commit()
            session.close()
            return channel
        except:
            return 0
        
    @staticmethod
    def selectStream(id):
        try:
            session = DAO.getSession()
            session.expire_on_commit = False
            stream = DAOStream.select(session, id)
            session.commit()
            session.close()
            return stream
        except:
            return 0
        
    @staticmethod
    def selectVideo(video_id):
        try:
            session = DAO.getSession()
            session.expire_on_commit = False
            video = DAOVideo.select(session, video_id)  # Assuming you have a select method in DAOVideo
            session.commit()
            session.close()
            return video
        except:
            return 0

    @staticmethod
    def selectCategory(channel_id):
        try:
            session = DAO.getSession()
            session.expire_on_commit = False
            category = DAOCategory.select(session, channel_id)
            session.commit()
            session.close()
            return category
        except:
            return 0
        

    # Obtém os ids dos usuários já cadastrados no banco
    @staticmethod
    def get_user_ids_from_users():
        try:
            session = DAO.getSession()
            user_ids = DAOUser.get_user_ids(session)  # Assuming you have a get_user_ids method in DAOUser
            session.commit()
            session.close()
            return user_ids
        except Exception as e:
            print(f"Erro para pegar User_id: {str(e)}")
            return []

    # Obtém os ids dos canais já cadastrados no banco
    @staticmethod
    def get_broadcaster_ids_from_canais():
        try:
            session = DAO.getSession()
            channel_id = DAOChannel.get_broadcaster_ids(session)  # Assuming you have a get_broadcaster_ids method in DAOChannel
            session.commit()
            session.close()
            return channel_id
        except:
            return []
        
    # Obtém os nomes das categorias já cadastradas no banco
    @staticmethod
    def get_category_names_from_categories():
        try:
            session = DAO.getSession()
            category_name = DAOCategory.get_category_names(session)
            session.commit()
            session.close()
            return category_name
        except:
            return []


class API:
    def __init__(self):
        self.client_id = 'qphncqmutk6rmxx5dgbrihjmxzh03d' 
        self.client_secret = 'zozuslb1mq6vfph841e9v5wpcjm73f'

    # Obter o token de acesso
    def get_app_access_token(self):
        url = 'https://id.twitch.tv/oauth2/token'
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        }
        response = requests.post(url, params=params)
        data = response.json()
        return data.get('access_token')


    def get_users(self, token_acesso):
        broadcaster_names = self.get_broadcaster_names(token_acesso)

        # Divida a lista de logins em lotes de 100
        batches = [broadcaster_names[i:i + 100] for i in range(0, len(broadcaster_names), 100)]

        for batch in batches:
            url = 'https://api.twitch.tv/helix/users'
            
            params = {
                'login': batch
            }

            headers = {
                'Client-ID': self.client_id,
                'Authorization': f'Bearer {token_acesso}'
            }

            response = requests.get(url, params=params, headers=headers)
            data = response.json()

            for usuario in data.get('data', []):
                userObj = Usuario(user_id=usuario.get("id"),
                                login=usuario.get("login"),
                                display_name=usuario.get("display_name"),
                                user_type=usuario.get("type"),
                                broadcaster_type=usuario.get("broadcaster_type"),
                                description=usuario.get("description"),
                                created_at=usuario.get("created_at"))

                #print(f"Usuário: {userObj.user_id}, Login: {userObj.login}")

                # Verifica se o usuário já foi cadastrado
                check = DB.select_user(userObj.user_id)

                # Se não foi cadastrado, inserimos
                if not check:
                    DB.insert(userObj)
                # Se foi cadastrado, printamos uma mensagem
                #else:
                    #print(f"Usuário: {userObj.user_id} já cadastrado!")

    # Função para obter os nomes dos transmissores
    def get_broadcaster_names(self, token_acesso):
        total_streams = 4000
        batch_size = 100
        broadcaster_names = []

        url = 'https://api.twitch.tv/helix/streams'

        # Variável para armazenar o cursor para a próxima página de resultados
        cursor = None

        for _ in range(total_streams // batch_size):
            params = {
                'first': batch_size,
                'after': cursor  # cursor à requisição para obter os próximos registros
            }

            headers = {
                'Client-ID': self.client_id,
                'Authorization': f'Bearer {token_acesso}'
            }

            response = requests.get(url, params=params, headers=headers)
            data = response.json()

            #print(data)

            batch_names = [stream.get("user_login").lower() for stream in data.get('data', [])]
            broadcaster_names.extend(batch_names)

            # Atualiza o cursor para a próxima página de resultados
            cursor = data.get('pagination', {}).get('cursor')

            #print("Batch Broadcaster Names:", batch_names)

        #print("Total Broadcaster Names:", broadcaster_names)

        return broadcaster_names

    
    def get_canais(self, token_acesso):
        # Obtém os user_ids da tabela de usuários
        user_ids_from_db = DB.get_user_ids_from_users()

        # Verifica se há user_ids para evitar uma requisição desnecessária se a lista estiver vazia
        if user_ids_from_db:
            #print(f"User IDs from database: {user_ids_from_db}")

            url = 'https://api.twitch.tv/helix/channels'

            for batch in [user_ids_from_db[i:i + 100] for i in range(0, len(user_ids_from_db), 100)]:
                #print(f"Processing batch: {batch}")

                params = {
                    'first': 100,
                    'broadcaster_id': batch
                }
                headers = {
                    'Client-ID': self.client_id,
                    'Authorization': f'Bearer {token_acesso}'
                }

                response = requests.get(url, params=params, headers=headers)
                data = response.json()

                for canal in data.get('data', []):
                    canalObj = Canais(
                        channel_id=canal.get("broadcaster_id"),
                        broadcaster_name=canal.get("broadcaster_name"),
                        broadcaster_lang=canal.get("broadcaster_language")
                    )

                    # verifica se o canal já foi cadastrado
                    check = DB.selectChannel(canalObj.channel_id)
                    canalID = canalObj.channel_id

                    # se não foi cadastrado, inserimos
                    if not check:
                        result = DB.insert(canalObj)
                        if result:
                            print(f"Canal: {canalID} inserido com sucesso!")
                        else:
                            print(f"Erro ao inserir o canal: {canalID}")
                    # se foi cadastrado, printamos uma mensagem
                    else:
                        print(f"Canal: {canalID} já cadastrado!")
        else:
            print("Lista de user_ids está vazia. Nenhuma solicitação será feita.")


    # Faz uma solicitação para obter informações sobre as streams
    def get_streams(self, token_acesso):
        # Chame a função para obter os nomes dos transmissores
        broadcaster_ids_db = DB.get_broadcaster_ids_from_canais()

        # Obter as categorias
        category_ids_db = DB.get_category_names_from_categories()

        # Verifica se há user_ids para evitar uma requisição desnecessária se a lista estiver vazia
        if not broadcaster_ids_db or not category_ids_db:
            print("Lista de broadcaster_ids ou category_ids está vazia. Nenhuma solicitação será feita.")
            return

        #print(f"Broadcaster IDs from database: {broadcaster_ids_db}")

        url = 'https://api.twitch.tv/helix/streams'

        for batch in [broadcaster_ids_db[i:i + 100] for i in range(0, len(broadcaster_ids_db), 100)]:
            #print(f"Processing batch: {batch}")

            params = {
                'first': 100,
                'user_id': batch
            }
            headers = {
                'Client-ID': self.client_id,
                'Authorization': f'Bearer {token_acesso}'
            }

            response = requests.get(url, params=params, headers=headers)
            data = response.json()

            for stream in data.get('data', []):
                streamObj = Streams(
                    stream_id = stream.get("id"),
                    broadcaster_name = stream.get("user_name"),
                    title = stream.get("title"),
                    started_at = stream.get("started_at"),
                    viewer_count = stream.get("viewer_count"),
                    stream_lang = stream.get("language"),
                    category_name = stream.get("game_name")
                )

                # Verifica se a stream já foi cadastrada
                check = DB.selectStream(streamObj.stream_id)

                # Verifica se o nome da categoria é válido (está presente na tabela "Categories")
                if streamObj.category_name not in category_ids_db:
                    print(f"Ignorando stream {streamObj.stream_id}: Categoria inválida.")
                    continue

                # Debug
                # print(f"Stream ID: {streamID}, Check: {check}")

                # Se não foi cadastrado, inserimos
                if not check:
                    result = DB.insert(streamObj)
                    # DB.insert(streamObj)
                # Se foi cadastrado, printamos uma mensagem
                # else:
                #    print(f"Stream: {streamID} já cadastrada!")


    # Função para obter informações das categorias (jogos)
    def get_top_games(self, token_acesso):
        # Construa a URL com a consulta atual
        url = 'https://api.twitch.tv/helix/games/top'
        params = {
            'first': 100,
        }
        headers = {
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {token_acesso}'
        }

        response = requests.get(url, params=params, headers=headers)
        data = response.json()

        for categoria in data.get('data', []):
            categoriaObj = Category(category_id=categoria.get("id"),
                                    category_name=categoria.get("name"))

            # verifica se o canal já foi cadastrado
            check = DB.selectCategory(categoriaObj.category_id)
            categoriaID = categoriaObj.category_id

            # se não foi cadastrado, inserimos
            if not check:
                DB.insert(categoriaObj)
            # se foi cadastrado, printamos uma mensagem
            else:
                print(f"Canal: {categoriaID} já cadastrada!")
      

    def get_videos(self, access_token):
        user_ids_from_db = DB.get_user_ids_from_users()

        if user_ids_from_db:
            url = 'https://api.twitch.tv/helix/videos'

            for batch in [user_ids_from_db[i:i + 100] for i in range(0, len(user_ids_from_db), 100)]:
                params = {
                    'user_id': batch
                }
                headers = {
                    'Client-ID': self.client_id,
                    'Authorization': f'Bearer {access_token}'
                }

                response = requests.get(url, params=params, headers=headers)
                data = response.json()

                for video in data.get('data', []):
                    videoObj = Videos(
                        video_id=video.get('id'),
                        user_id=video.get('user_id'),
                        title=video.get('title'),
                        created_at=video.get('created_at'),
                        published_at=video.get('published_at'),
                        view_count=video.get('view_count'),
                        video_language=video.get('language'),
                        video_type=video.get('type'),
                        duration=video.get('duration')
                    )

                
                    check = DB.selectVideo(videoObj.video_id)
                    canalID = videoObj.video_id

                    # se não foi cadastrado, inserimos
                    if not check:
                        result = DB.insert(videoObj)

        else:
            print("List of user_ids is empty. No requests will be made.")
    




