from typing import List

from app.utils.triplestore_client import TripleStoreClient
from app.models.user import UserInDB

class UserRepository:
    def __init__(self, triplestore_client: TripleStoreClient):
        self.triplestore_client = triplestore_client

    def create_user(self, user: UserInDB) -> UserInDB:
        sparql_update = f"""
        INSERT DATA {{
            GRAPH <http://example.org/users> {{
                <http://example.org/users/{user.username}> a <http://schema.org/Person> ;
                    <http://schema.org/name> "{user.full_name}" ;
                    <http://schema.org/email> "{user.email}" .
            }}
        }}
        """
        self.triplestore_client.update(sparql_update)

    def find_all_users(self) -> List[UserInDB]:
        sparql_query = """
        PREFIX schema: <http://schema.org/>
        SELECT ?id ?name ?email WHERE {
            ?user a schema:Person ;
                schema:identifier ?id ;
                schema:name ?name ;
                schema:email ?email .
        }
        """
        results = self.triplestore_client.query(sparql_query)
        users = [
            {
                "id": binding["id"]["value"],
                "name": binding["name"]["value"],
                "email": binding["email"]["value"],
            }
            for binding in results.get("results", {}).get("bindings", [])
        ]
        return users

    def find_user(self, user_id: str) -> UserInDB:
        sparql_query = f"""
        SELECT ?name ?email WHERE {{
            GRAPH <http://example.org/users> {{
                <http://example.org/users/{user_id}> a <http://schema.org/Person> ;
                    <http://schema.org/name> ?name ;
                    <http://schema.org/email> ?email .
            }}
        }}
        """
        results = self.triplestore_client.query(sparql_query)
        bindings = results.get("results", {}).get("bindings", [])
        if bindings:
            return {
                "id": user_id,
                "name": bindings[0]["name"]["value"],
                "email": bindings[0]["email"]["value"],
            }
        return None
