from flask import Flask, request
import whois
from datetime import datetime
from opensearchpy import OpenSearch
from flask_restful import Resource
from src.helpers import format_response
from src.app import app

class Domain(Resource):
    def get(self, domain):
        if domain is None:
            return format_response(success=False, message='Please enter a domain name', code=400)

        # todo: check if valid domain

        # get domain data
        domain = domain.lower()
        data = whois.whois(domain)  # TODO: find a better module

        # TODO: fix error
        # Create OpenSearch client
        host = app.config['OPENSEARCH_HOST']
        port = app.config['OPENSEARCH_PORT']
        auth = (app.config['OPENSEARCH_USER'], app.config['OPENSEARCH_PASSWORD'])  # For testing only
        index_name = 'whois-searches'

        client = OpenSearch(
            hosts=[{'host': host, 'port': port}],
            http_compress=True,  # enables gzip compression for request bodies
            http_auth=auth,
            use_ssl=True,
            verify_certs=False,
            ssl_assert_hostname=False,
            ssl_show_warn=False,
        )

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

