import os
import requests as req
import json
import jwt
import logging


class AuthenticateYandex:

    @classmethod
    def get_tokens_yandex(cls, code, code_verifier):
        response = req.post(
            f'https://oauth.yandex.ru/token', headers={
                "Content-type": "application/x-www-form-urlencoded",
                "Accept": "application/json"},
            data={
                "grant_type": "authorization_code",
                "code": f'{code}',
                "client_id": f'{os.getenv("YANDEX_CLIENT_ID")}',
                "client_secret": f'{os.getenv("YANDEX_CLIENT_SECRET")}',
                "code_challenge_method": "S256",
                "code_verifier": f'{code_verifier}',
            }
        )
        response_data = json.loads(response.content.decode("utf-8"))
        return response_data

    @classmethod
    def get_scope_yandex(cls, access_token, refresh_token):
        data = cls.get_decode_jwt_yandex(access_token)
        if data:
            return data
        else:
            new_tokens = cls.get_update_tokens_yandex(refresh_token)
            new_data = cls.get_decode_jwt_yandex(new_tokens.get("access_token"))
            return new_data

    @classmethod
    def get_decode_jwt_yandex(cls, access_token):
        jwt_decode = None

        scope_jwt = req.get("https://login.yandex.ru/info?format=jwt", headers={
            "Authorization": f'OAuth {access_token}'
        })
        if scope_jwt.content:
            try:
                jwt_decode = jwt.api_jwt.decode_complete(scope_jwt.content, os.getenv("YANDEX_CLIENT_SECRET"),
                                                         algorithms=['HS256'])

            except jwt.exceptions.ImmatureSignatureError as err:
                logging.warning(err)
                jwt_decode = jwt.api_jwt.decode_complete(scope_jwt.content, os.getenv("YANDEX_CLIENT_SECRET"),
                                                         algorithms=['HS256'], options={"verify_iat": False})

            except jwt.exceptions.InvalidSignatureError as err:
                logging.warning(err)
            except jwt.exceptions.DecodeError as err:
                logging.warning(err)
        return jwt_decode

    @classmethod
    def get_update_tokens_yandex(cls, refresh_token):
        logging.info("refresh token")
        response = req.post(
            f'https://oauth.yandex.ru/token', headers={
                "Content-type": "application/x-www-form-urlencoded",
                "Accept": "application/json"},
            data={
                "grant_type": "refresh_token",
                "refresh_token": f'{refresh_token}',
                "client_id": f'{os.getenv("YANDEX_CLIENT_ID")}',
                "client_secret": f'{os.getenv("YANDEX_CLIENT_SECRET")}',
            }
        )
        response_data = json.loads(response.content.decode("utf-8"))
        return response_data
