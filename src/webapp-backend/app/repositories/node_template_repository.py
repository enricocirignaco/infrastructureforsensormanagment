from app.utils.triplestore_client import TripleStoreClient


class NodeTemplateRepository:
    def __init__(self, triplestore_client: TripleStoreClient):
        self.triplestore_client = triplestore_client
