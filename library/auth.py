import os
import logging
import jwt
from bson.json_util import dumps
from mongoengine.errors import DoesNotExist

from odm.account import Account


class AuthToken:
    @staticmethod
    def decode_token(token: str):
        try:
            token = jwt.decode(token, os.getenv('JWT_TOKEN_SECRET'), algorithms=["HS256"])
            logging.info('token decoded success')
        except jwt.DecodeError:
            logging.info('token decoded failed')
            token = None

        return token

    @staticmethod
    def verify(token: str):
        logging.info('token verify starting')
        token = AuthToken.decode_token(token=token)

        if token:
            try:
                account = Account.objects.get(pk=token['id'], token=token['token'])
                logging.info('Account matched, token verify success')
                return True
            except DoesNotExist:
                logging.info('Account not matched, token verify failed')
                return False
        else:
            return None
