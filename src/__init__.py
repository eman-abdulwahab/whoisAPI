from flask import Flask

app = Flask(__name__)
app.config.from_envvar('APP_SETTINGS')

from src.helpers import format_response
from src.services.opensearch_wrapper import OpenSearchWrapper
from src.resources.domain import Domain
from src import routes

