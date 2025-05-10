from app.utils.triplestore_client import TripleStoreClient

from rdflib import Graph, URIRef, Literal, RDF

class SensorNodeRepository:

    def __init__(self, triplestore_client: TripleStoreClient):
        self.triplestore_client = triplestore_client
        self.schema = URIRef("http://schema.org/")
        self.bfh = URIRef("http://data.bfh.ch/")