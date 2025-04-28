from collections import defaultdict
from typing import List
from uuid import UUID
from datetime import datetime

from rdflib import Graph, URIRef, Literal, RDF

from app.utils.triplestore_client import TripleStoreClient
from app.models.project import (
    ProjectInDB,
    ProjectOutSlim,
    ProjectOutFull,
    ProjectLink,
    ProjectLogbookEntry,
    ProjectStateEnum,
    ProjectLinkEnum,
    ProjectLogbookEnum
)
from app.models.user import UserOut, RoleEnum

class ProjectRepository:
    def __init__(self, triplestore_client: TripleStoreClient):
        self.triplestore_client = triplestore_client
        self.schema = URIRef("http://schema.org/")
        self.bfh = URIRef("http://data.bfh.ch/")

    def create_project(self, project: ProjectInDB) -> ProjectInDB:
        g = Graph()
        project_uri = URIRef(f"http://data.bfh.ch/projects/{project.uuid}")

        # Basisdaten
        g.add((project_uri, RDF.type, URIRef(self.schema + "Project")))
        g.add((project_uri, URIRef(self.schema + "identifier"), Literal(str(project.uuid))))
        g.add((project_uri, URIRef(self.schema + "name"), Literal(project.name)))
        g.add((project_uri, URIRef(self.schema + "alternateName"), Literal(project.short_name)))
        g.add((project_uri, URIRef(self.schema + "description"), Literal(project.description)))
        g.add((project_uri, URIRef(self.bfh + "state"), URIRef(project.state.rdf_uri)))

        # Links
        for idx, link in enumerate(project.external_props):
            link_uri = URIRef(f"http://data.bfh.ch/projects/{project.uuid}/link/{idx}")
            g.add((project_uri, URIRef(self.schema + "hasPart"), link_uri))
            g.add((link_uri, RDF.type, URIRef(self.schema + "WebPage")))
            g.add((link_uri, URIRef(self.schema + "url"), Literal(link.url)))
            g.add((link_uri, URIRef(self.bfh + "linkType"), URIRef(link.type.rdf_uri)))
            if link.name:
                g.add((link_uri, URIRef(self.schema + "name"), Literal(link.name)))

        # Logbuch
        for idx, entry in enumerate(project.logbook):
            log_uri = URIRef(f"http://data.bfh.ch/projects/{project.uuid}/log/{idx}")
            g.add((project_uri, URIRef(self.bfh + "hasLogEntry"), log_uri))
            g.add((log_uri, RDF.type, URIRef(self.bfh + "LogEntry")))
            g.add((log_uri, URIRef(self.bfh + "logType"), Literal(entry.type.value)))
            g.add((log_uri, URIRef(self.schema + "dateCreated"), Literal(entry.date.isoformat())))
            g.add((log_uri, URIRef(self.schema + "creator"), URIRef(f"http://data.bfh.ch/users/{entry.user.uuid}")))

        query = f"""INSERT DATA {{ {g.serialize(format="nt")} }}"""
        self.triplestore_client.update(query)

        return self.find_project_by_uuid(project.uuid)

    def find_all_projects(self) -> List[ProjectOutSlim]:
        sparql_query = """
        PREFIX schema: <http://schema.org/>
        PREFIX bfh: <http://data.bfh.ch/>

        SELECT ?uuid ?name ?shortName ?state
        WHERE {
            ?project a schema:Project ;
                     schema:identifier ?uuid ;
                     schema:name ?name ;
                     schema:alternateName ?shortName ;
                     bfh:state ?state .
        }
        """
        results = self.triplestore_client.query(sparql_query)
        return [
            ProjectOutSlim(
                uuid=UUID(binding["uuid"]["value"]),
                name=binding["name"]["value"],
                short_name=binding["shortName"]["value"],
                state=ProjectStateEnum.from_rdf_uri(binding["state"]["value"])
            )
            for binding in results.get("results", {}).get("bindings", [])
        ]

    def find_project_by_uuid(self, uuid: UUID) -> ProjectInDB | None:
        project_uri = f"<http://data.bfh.ch/projects/{uuid}>"

        # 1) Basisdaten abfragen
        sparql_base = f"""
        PREFIX schema: <http://schema.org/>
        PREFIX bfh: <http://data.bfh.ch/>

        SELECT ?name ?shortName ?description ?state
        WHERE {{
            {project_uri} a schema:Project ;
                            schema:name ?name ;
                            schema:alternateName ?shortName ;
                            schema:description ?description ;
                            bfh:state ?state .
        }}"""
        base_res = self.triplestore_client.query(sparql_base)
        base_bindings = base_res.get("results", {}).get("bindings", [])
        if not base_bindings:
            return None
        base = base_bindings[0]

        project = ProjectInDB(
            uuid=uuid,
            name=base['name']['value'],
            short_name=base['shortName']['value'],
            description=base['description']['value'],
            state=ProjectStateEnum.from_rdf_uri(base['state']['value']),
            external_props=[],
            logbook=[]
        )

        # 2) Links abfragen
        sparql_links = f"""
        PREFIX schema: <http://schema.org/>
        PREFIX bfh: <http://data.bfh.ch/>

        SELECT ?linkUrl ?linkName ?linkType
        WHERE {{
            {project_uri} schema:hasPart ?link .
            ?link a schema:WebPage ;
                schema:url ?linkUrl ;
                bfh:linkType ?linkType .
            OPTIONAL {{ ?link schema:name ?linkName . }}
        }}"""
        link_res = self.triplestore_client.query(sparql_links)
        for row in link_res.get("results", {}).get("bindings", []):
            project.external_props.append(
                ProjectLink(
                    name=row.get('linkName', {}).get('value'),
                    url=row['linkUrl']['value'],
                    type=ProjectLinkEnum.from_rdf_uri(row['linkType']['value'])
                )
            )

        # 3) Logbuch abfragen
        sparql_logs = f"""
        PREFIX schema: <http://schema.org/>
        PREFIX bfh: <http://data.bfh.ch/>

        SELECT ?logType ?logDate ?creatorUuid ?creatorEmail ?creatorFullName ?creatorRole
        WHERE {{
            {project_uri} bfh:hasLogEntry ?logEntry .
            ?logEntry a bfh:LogEntry ;
                    bfh:logType ?logType ;
                    schema:dateCreated ?logDate ;
                    schema:creator ?creator .
            ?creator a schema:Person ;
                    schema:identifier ?creatorUuid ;
                    schema:email ?creatorEmail ;
                    schema:name ?creatorFullName ;
                    bfh:hasRole ?creatorRole .
        }}"""
        log_res = self.triplestore_client.query(sparql_logs)
        for row in log_res.get("results", {}).get("bindings", []):
            project.logbook.append(
                ProjectLogbookEntry(
                    type=ProjectLogbookEnum(row['logType']['value']),
                    date=datetime.fromisoformat(row['logDate']['value']),
                    user=UserOut(
                        uuid=row['creatorUuid']['value'],
                        full_name=row['creatorFullName']['value'],
                        email=row['creatorEmail']['value'],
                        role=RoleEnum.from_rdf_uri(row['creatorRole']['value'])
                    )
                )
            )

        return project


    def delete_project(self, uuid: UUID) -> None:
        sparql_delete = f"""
        PREFIX schema: <http://schema.org/>
        PREFIX bfh: <http://data.bfh.ch/>

        DELETE {{
            ?s ?p ?o
        }}
        WHERE {{
            ?s ?p ?o .
            FILTER (
                STRSTARTS(STR(?s), "http://data.bfh.ch/projects/{uuid}/link/") ||
                STRSTARTS(STR(?s), "http://data.bfh.ch/projects/{uuid}/log/") ||
                STR(?s) = "http://data.bfh.ch/projects/{uuid}"
            )
        }}
        """
        self.triplestore_client.update(sparql_delete)



    def update_project(self, project: ProjectOutFull) -> ProjectInDB:
        self.delete_project(project.uuid)
        project_db = ProjectInDB(**project.model_dump())
        return self.create_project(project_db)
