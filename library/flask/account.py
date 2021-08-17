import os
import logging
from bson.json_util import dumps
from flask import Response, request
from passlib.hash import pbkdf2_sha512
from mongoengine import errors
import uuid
import jwt

from odm.account import Account


class FlaskAccount:
    @staticmethod
    def create():
        json_data = request.get_json()
        logging.info('prepare data for create a new account')

        try:
            account = Account()
            account.email = json_data['email']
            account.password = pbkdf2_sha512.hash(json_data['password'])
            account.token = str(uuid.uuid4())
            account.first_name = json_data['first_name']
            account.last_name = json_data['last_name']
            account.save()

            logging.info('Account created!')

        except errors.NotUniqueError:
            logging.info('Email already exists')
            return Response(dumps({
                'status': 'Bad Request',
                'data': 'Email already exists',
                "code": 400
            }), mimetype='text/json'), 400

        return Response(dumps({
            'status': 'ok',
            "code": 200
        }), mimetype='text/json'), 200

    @staticmethod
    def update():
        pass

    @staticmethod
    def sign_in():
        pass

    @staticmethod
    def sign_out():
        pass
