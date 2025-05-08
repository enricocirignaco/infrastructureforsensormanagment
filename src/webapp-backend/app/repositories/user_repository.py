from typing import List
from uuid import UUID
from rdflib import Graph, URIRef, Literal, RDF

from app.utils.triplestore_client import TripleStoreClient
from app.models.user import UserInDB, RoleEnum

class UserRepository:
    def __init__(self, triplestore_client: TripleStoreClient):
        self.triplestore_client = triplestore_client
        self.schema = URIRef("http://schema.org/")
        self.bfh = URIRef("http://data.bfh.ch/")

    def create_user(self, user: UserInDB) -> UserInDB:
        g = Graph()
        g.bind('schema', self.schema)
        g.bind('bfh', self.bfh)

        user_uri = URIRef(f"http://data.bfh.ch/users/{user.uuid}")

        g.add((user_uri, RDF.type, URIRef(self.schema + "Person")))
        g.add((user_uri, URIRef(self.schema + "identifier"), Literal(str(user.uuid))))
        g.add((user_uri, URIRef(self.schema + "name"), Literal(user.full_name)))
        g.add((user_uri, URIRef(self.schema + "email"), Literal(user.email)))
        g.add((user_uri, URIRef(self.bfh + "password"), Literal(user.hashed_password)))
        g.add((user_uri, URIRef(self.bfh + "hasRole"), URIRef(user.role.rdf_uri)))

        sparql_update = f"INSERT DATA {{ {g.serialize(format='nt')} }}"
        self.triplestore_client.update(sparql_update)

        return self.find_user_by_uuid(user.uuid)
    
    def update_user(self, user: UserInDB) -> UserInDB:
        sparql_update = f"""
        PREFIX schema: <http://schema.org/>
        PREFIX bfh: <http://data.bfh.ch/>

        DELETE {{
            <http://data.bfh.ch/users/{user.uuid}> schema:name ?name ;
                                            schema:email ?email ;
                                            bfh:hasRole ?role .
        }}
        INSERT {{
            <http://data.bfh.ch/users/{user.uuid}> schema:name "{user.full_name}" ;
                                            schema:email "{user.email}" ;
                                            bfh:hasRole {user.role.rdf_uri} .
        }}
        WHERE {{
            <http://data.bfh.ch/users/{user.uuid}> schema:name ?name ;
                                            schema:email ?email ;
                                            bfh:hasRole ?role .
        }}
        """
        self.triplestore_client.update(sparql_update)

        return self.find_user_by_uuid(user.uuid)
    
    def change_password(self, user: UserInDB) -> UserInDB:
        sparql_update = f"""
        PREFIX schema: <http://schema.org/>
        PREFIX bfh: <http://data.bfh.ch/>

        DELETE {{
            <http://data.bfh.ch/users/{user.uuid}> bfh:password ?oldPassword .
        }}
        INSERT {{
            <http://data.bfh.ch/users/{user.uuid}> bfh:password "{user.hashed_password}" .
        }}
        WHERE {{
            <http://data.bfh.ch/users/{user.uuid}> bfh:password ?oldPassword .
        }}
        """
        self.triplestore_client.update(sparql_update)

        return self.find_user_by_uuid(user.uuid)

    def find_all_users(self) -> List[UserInDB]:
        sparql_query = """
        PREFIX schema: <http://schema.org/>
        PREFIX bfh: <http://data.bfh.ch/>
        SELECT ?uuid ?name ?email ?password ?role WHERE {{
            ?user a schema:Person ;
                schema:identifier ?uuid ;
                schema:name ?name ;
                schema:email ?email ;
                bfh:password ?password ;
                bfh:hasRole ?role .
        }}
        """
        results = self.triplestore_client.query(sparql_query)
        users = [
            UserInDB(
                uuid=binding["uuid"]["value"],
                full_name=binding["name"]["value"],
                email=binding["email"]["value"],
                hashed_password=binding["password"]["value"],
                role=RoleEnum.from_rdf_uri(binding["role"]["value"])
            )
            for binding in results.get("results", {}).get("bindings", [])
        ]
        return users

    def find_user_by_uuid(self, uuid: UUID) -> UserInDB | None:
        sparql_query = f"""
        PREFIX schema: <http://schema.org/>
        PREFIX bfh: <http://data.bfh.ch/>
        SELECT ?name ?email ?password ?role WHERE {{
            ?user a schema:Person ;
                schema:identifier "{uuid}" ;
                schema:name ?name ;
                schema:email ?email ;
                bfh:password ?password ;
                bfh:hasRole ?role .
        }}
        """
        results = self.triplestore_client.query(sparql_query)
        bindings = results.get("results", {}).get("bindings", [])
        if bindings:
            return UserInDB(
                uuid=uuid,
                full_name=bindings[0]["name"]["value"],
                email=bindings[0]["email"]["value"],
                hashed_password=bindings[0]["password"]["value"],
                role=RoleEnum.from_rdf_uri(bindings[0]["role"]["value"])
            )
        return None
    
    def find_user_by_email(self, email: str) -> UserInDB | None:
        sparql_query = f"""
        PREFIX schema: <http://schema.org/>
        PREFIX bfh: <http://data.bfh.ch/>
        SELECT ?uuid ?name ?password ?role WHERE {{
            ?user a schema:Person ;
                schema:identifier ?uuid ;
                schema:name ?name ;
                schema:email "{email}" ;
                bfh:password ?password ;
                bfh:hasRole ?role .
        }}
        """
        results = self.triplestore_client.query(sparql_query)
        bindings = results.get("results", {}).get("bindings", [])
        if bindings:
            return UserInDB(
                uuid=bindings[0]["uuid"]["value"],
                full_name=bindings[0]["name"]["value"],
                email=email,
                hashed_password=bindings[0]["password"]["value"],
                role=RoleEnum.from_rdf_uri(bindings[0]["role"]["value"])
            )
        return None