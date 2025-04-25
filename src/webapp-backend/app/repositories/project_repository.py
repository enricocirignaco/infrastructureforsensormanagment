from typing import List
from uuid import UUID

from app.utils.triplestore_client import TripleStoreClient
from app.models.project import ProjectInDB, ProjectLink, ProjectStateEnum, ProjectOutSlim, ProjectLinkEnum, ProjectOutFull
from collections import defaultdict

class ProjectRepository:
    def __init__(self, triplestore_client: TripleStoreClient):
        self.triplestore_client = triplestore_client

    def create_project(self, project: ProjectInDB) -> ProjectInDB:
        def build_links(links: List[ProjectLink]):
            return "\n    ".join([
                f"""schema:hasPart [
                    a schema:WebPage ;
                    schema:name "{link.name or link.type.value}" ;
                    schema:url "{link.url}" ;
                    bfh:linkType "{link.type.rdf_uri}"
                ] ;""" for link in links
            ])

        links_block = build_links(project.external_props or [])

        sparql_update = f"""
        PREFIX schema: <http://schema.org/>
        PREFIX bfh: <http://data.bfh.ch/>

        INSERT DATA {{
        <http://data.bfh.ch/projects/{project.uuid}> a schema:Project ;
            schema:identifier "{project.uuid}" ;
            schema:name "{project.name}" ;
            schema:alternateName "{project.short_name}" ;
            schema:description "{project.description}" ;
            bfh:state "{project.state.rdf_uri}" ;
            {links_block}
            .
        }}
        """

        self.triplestore_client.update(sparql_update)
        return self.find_project_by_uuid(project.uuid)


    def find_all_projects(self) -> List[ProjectOutSlim]:
        sparql_query = f"""
        PREFIX schema: <http://schema.org/>
        PREFIX bfh: <http://data.bfh.ch/>

        SELECT ?uuid ?name ?shortName ?state
        WHERE {{
        ?project a schema:Project ;
                schema:identifier ?uuid ;
                schema:name ?name ;
                schema:alternateName ?shortName ;
                bfh:state ?state .
        }}
        """
        results = self.triplestore_client.query(sparql_query)
        projects = [
            ProjectOutSlim(
                uuid=binding["uuid"]["value"],
                name=binding["name"]["value"],
                short_name=binding["shortName"]["value"],
                state=ProjectStateEnum.from_rdf_uri(binding["state"]["value"])
            )
            for binding in results.get("results", {}).get("bindings", [])
        ]
        return projects

    def find_project_by_uuid(self, uuid: UUID) -> ProjectInDB | None:
        sparql_query = f"""
        PREFIX schema: <http://schema.org/>
        PREFIX bfh: <http://data.bfh.ch/>

        SELECT ?project ?name ?shortName ?description ?state ?linkName ?linkUrl ?linkType
        WHERE {{
        ?project a schema:Project ;
                schema:identifier "{uuid}" ;
                schema:name ?name ;
                schema:alternateName ?shortName ;
                schema:description ?description ;
                bfh:state ?state .

        OPTIONAL {{
            ?project schema:hasPart ?link .
            ?link a schema:WebPage ;
                schema:url ?linkUrl ;
                bfh:linkType ?linkType .
            OPTIONAL {{ ?link schema:name ?linkName. }}
        }}
        }}
        """
        results = self.triplestore_client.query(sparql_query)
        bindings = results.get("results", {}).get("bindings", [])
        if not bindings:
            return None
            raise ValueError("No project with this uuid found")
        
        grouped = defaultdict(list)
        for row in bindings:
            project_id = row['project']['value']
            grouped[project_id].append(row)

        # Take first element (only one project expected)
        _, rows = next(iter(grouped.items()))
        first_row = rows[0]

        project = ProjectInDB(
            uuid=UUID(first_row['project']['value'].split("/")[-1]),
            name=first_row['name']['value'],
            short_name=first_row['shortName']['value'],
            description=first_row['description']['value'],
            state=ProjectStateEnum.from_rdf_uri(first_row['state']['value']),
            external_props=[]
        )

        for row in rows:
            if 'linkUrl' in row and 'linkType' in row:
                project.external_props.append(ProjectLink(
                    name=row.get('linkName', {}).get('value'),
                    url=row['linkUrl']['value'],
                    type=ProjectLinkEnum.from_rdf_uri(row['linkType']['value'])
                ))
        return project
    
    def delete_project(self, uuid: UUID) -> None:
        sparql_delete = f"""
        PREFIX schema: <http://schema.org/>
        PREFIX bfh: <http://data.bfh.ch/>

        DELETE WHERE {{
            <http://data.bfh.ch/projects/{uuid}> ?p ?o .
        }}
        """

        self.triplestore_client.update(sparql_delete)

    def update_project(self, uuid: UUID, project: ProjectOutFull) -> ProjectInDB:
        self.delete_project(uuid)

        project_in_db = ProjectInDB(
            uuid=uuid,
            name=project.name,
            short_name=project.short_name,
            description=project.description,
            state=project.state,
            external_props=project.external_props,
        )

        return self.create_project(project_in_db)
