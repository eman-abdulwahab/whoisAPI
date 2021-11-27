from flask_restful import Api
from src import app
from src import Domain

api = Api(app)
api.add_resource(Domain, '/whois/<string:domain>')
