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
            'code': 200
        }), mimetype='text/json'), 200

    @staticmethod
    def update():
        pass

    @staticmethod
    def sign_in():
        logging.info('execute account sign in')

        email = request.args.get('email')
        password = request.args.get('password')

        account = Account.objects(email=email).only(
            'password',
            'token'
        ).first()

        if account:
            if pbkdf2_sha512.verify(password, account['password']):
                logging.info('sign in success')

                token_encode = jwt.encode({
                    'id': str(account.pk),
                    'token': account.token
                }, os.getenv('JWT_TOKEN_SECRET'), algorithm='HS256')

                return Response(dumps({
                    'status': 'ok',
                    'token': token_encode,
                    # 'token': jwt.decode(token_encode, os.getenv('JWT_TOKEN_SECRET'), algorithms=["HS256"]),
                    'code': 200
                }), mimetype='text/json'), 200
            else:
                logging.info('sign in unauthorized: wrong password')

                return Response(dumps({
                    'status': 'unauthorized',
                    'data': 'Unauthorized User',
                    'code': 401
                }), mimetype='text/json'), 401
        else:
            logging.info('sign in unauthorized: account not exists')
            
            return Response(dumps({
                'status': 'unauthorized',
                'data': 'Unauthorized User',
                'code': 401
            }), mimetype='text/json'), 401

    @staticmethod
    def sign_out():
        pass
