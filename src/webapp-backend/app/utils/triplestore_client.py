from SPARQLWrapper import SPARQLWrapper, JSON

class TripleStoreClient:
    def __init__(self, endpoint_url: str):
        self.sparql = SPARQLWrapper(endpoint_url)
        self.sparql.setReturnFormat(JSON)

    def query(self, sparql_query: str) -> dict:
        self.sparql.setQuery(sparql_query)
        try:
            return self.sparql.query().convert()
        except Exception as e:
            raise RuntimeError(f"SPARQL query failed: {e}")

    def update(self, sparql_update: str) -> None:
        self.sparql.setQuery(sparql_update)
        self.sparql.setMethod("POST")
        try:
            self.sparql.query()
        except Exception as e:
            raise RuntimeError(f"SPARQL update failed: {e}")
