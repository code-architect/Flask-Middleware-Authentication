import logging
from flask import Flask

# middleware here

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
#app.wsgi_app = middleware(app.wsgi_app)


app.add_url_rule('/account', view_func=, methods=['PUT'])
app.add_url_rule('/account', view_func=, methods=['POST'])
app.add_url_rule('/account/sign-in', view_func=, methods=['GET'])
app.add_url_rule('/account/sign-out', view_func=, methods=['GET'])


if __name__ == '__main__':
    app.run('0.0.0.0', '5000', debug=True)