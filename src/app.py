from flask import Flask
from flask_restful import Api
from src.resources.domain import Domain

app = Flask(__name__)
app.config.from_envvar('APP_SETTINGS')
api = Api(app)

api.add_resource(Domain, '/whois/<string:domain>')

if __name__ == '__main__':
    app.run(debug=True)
