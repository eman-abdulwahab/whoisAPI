from opensearchpy import OpenSearch
from src import app


class OpenSearchWrapper:
    @staticmethod
    def create_client():
        # Create OpenSearch client
        host = app.config['OPENSEARCH_HOST']
        port = app.config['OPENSEARCH_PORT']
        auth = (app.config['OPENSEARCH_USER'], app.config['OPENSEARCH_PASSWORD'])

        return OpenSearch(
            hosts=[{'host': host, 'port': port}],
            http_compress=True,  # enables gzip compression for request bodies
            http_auth=auth,
            use_ssl=True,
            verify_certs=False,
            ssl_assert_hostname=False,
            ssl_show_warn=False,
        )

