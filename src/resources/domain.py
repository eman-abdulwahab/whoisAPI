import whois
import validators
from datetime import datetime
from flask_restful import Resource
from src import format_response
from src import OpenSearchWrapper


class Domain(Resource):
    def get(self, domain):
        if domain is None:
            return format_response(success=False, message='Please enter a domain name', code=400)

        # get domain data
        domain = domain.lower()
        data = whois.whois(domain)

        # check if valid domain
        if not validators.domain(domain):
            return format_response(success=False, message='Please enter a valid domain name', code=400)

        # Create OpenSearch client from wrapper
        index_name = 'whois-searches'
        client = OpenSearchWrapper.create_client()

        # check if domain already exists
        exists = client.exists(index_name, domain)
        if exists:
            # update existing record
            data['updated_at'] = datetime.today().isoformat()
            client.update(index=index_name, body={'doc': data}, id=domain)
        else:
            # create new record with current date as creation date
            data['created_at'] = datetime.today().isoformat()
            data['updated_at'] = datetime.today().isoformat()  # default
            client.index(index=index_name, body=data, id=domain)

        # return data
        data = client.get(index=index_name, id=domain)
        return format_response(success=True, data=data)

