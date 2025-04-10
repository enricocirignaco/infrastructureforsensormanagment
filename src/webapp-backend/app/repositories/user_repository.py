from typing import List
from uuid import UUID

from app.utils.triplestore_client import TripleStoreClient
from app.models.user import UserInDB, RoleEnum

class UserRepository:
    def __init__(self, triplestore_client: TripleStoreClient):
        self.triplestore_client = triplestore_client

    def create_user(self, user: UserInDB) -> UserInDB:
        sparql_update = f"""
        PREFIX schema: <http://schema.org/>
        PREFIX bfh: <http://ld.bfh.ch/>
        INSERT DATA {{
            <http://ld.bfh.ch/users/{user.uuid}> a schema:Person ;
                schema:identifier "{user.uuid}" ;
                schema:name "{user.full_name}" ;
                schema:email "{user.email}" ;
                bfh:password "{user.hashed_password}" ;
                bfh:hasRole {user.role.rdf_uri} .
        }}
        """
        self.triplestore_client.update(sparql_update)

        return self.find_user_by_uuid(user.uuid)

    def find_all_users(self) -> List[UserInDB]:
        sparql_query = """
        PREFIX schema: <http://schema.org/>
        PREFIX bfh: <http://ld.bfh.ch/>
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

    def find_user_by_uuid(self, uuid: UUID) -> UserInDB:
        sparql_query = f"""
        PREFIX schema: <http://schema.org/>
        PREFIX bfh: <http://ld.bfh.ch/>
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
        PREFIX bfh: <http://ld.bfh.ch/>
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