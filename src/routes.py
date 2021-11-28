from flask_restful import Api
from src import app
from src import Domain
import logging


@app.route("/")
def index():
    logging.info(app.config)
    return 'Test'


api = Api(app)
api.add_resource(Domain, '/whois/<string:domain>')

