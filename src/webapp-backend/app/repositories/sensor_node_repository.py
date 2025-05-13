from app.utils.triplestore_client import TripleStoreClient
from app.models.sensor_node import SensorNodeDB, SensorNodeOutSlim, SensorNodeLocation, SensorNodeStateEnum, ConfigurableAssignment, ConfigurableTypeEnum, SensorNodeLogbookEntry, SensorNodeLogbookEnum
from app.models.node_template import NodeTemplateOutSlim, HardwareBoard, NodeTemplateStateEnum
from app.models.user import UserOut, RoleEnum
from app.models.project import ProjectOutSlim, ProjectStateEnum

from rdflib import Graph, URIRef, Literal, RDF
from uuid import UUID
from typing import List
from datetime import datetime

class SensorNodeRepository:

    def __init__(self, triplestore_client: TripleStoreClient):
        self.triplestore_client = triplestore_client
        self.schema = URIRef("http://schema.org/")
        self.bfh = URIRef("http://data.bfh.ch/")

    def create_sensor_node(self, sensor_node: SensorNodeDB) -> SensorNodeDB:
        g = Graph()
        g.bind('schema', self.schema)
        g.bind('bfh', self.bfh)

        sensor_uri = URIRef(f"http://data.bfh.ch/sensorNodes/{sensor_node.uuid}")

        # Basisdaten
        g.add((sensor_uri, RDF.type, URIRef(self.bfh + "SensorNode")))
        g.add((sensor_uri, URIRef(self.bfh + "identifier"), Literal(str(sensor_node.uuid))))
        g.add((sensor_uri, URIRef(self.schema + "name"), Literal(sensor_node.name)))
        if sensor_node.description:
            g.add((sensor_uri, URIRef(self.schema + "description"), Literal(sensor_node.description)))
        g.add((sensor_uri, URIRef(self.bfh + "state"), URIRef(sensor_node.state.rdf_uri)))
        g.add((sensor_uri, URIRef(self.bfh + "ttnDeviceLink"), Literal(str(sensor_node.ttn_device_link))))
        
        # Standort
        if sensor_node.location.latitude is not None:
            g.add((sensor_uri, URIRef(self.bfh + "latitude"), Literal(sensor_node.location.latitude)))
        if sensor_node.location.longitude is not None:
            g.add((sensor_uri, URIRef(self.bfh + "longitude"), Literal(sensor_node.location.longitude)))
        if sensor_node.location.altitude is not None:
            g.add((sensor_uri, URIRef(self.bfh + "altitude"), Literal(sensor_node.location.altitude)))
        if sensor_node.location.postalcode:
            g.add((sensor_uri, URIRef(self.bfh + "postalcode"), Literal(sensor_node.location.postalcode)))

        # Verlinkung zum NodeTemplate
        g.add((sensor_uri, URIRef(self.bfh + "usesNodeTemplate"),
            URIRef(f"http://data.bfh.ch/nodeTemplates/{sensor_node.node_template_uuid}")))

        # Verlinkung zum Projekt
        g.add((sensor_uri, URIRef(self.bfh + "partOfProject"),
            URIRef(f"http://data.bfh.ch/projects/{sensor_node.project_uuid}")))

        # Configurables
        for idx, conf in enumerate(sensor_node.configurables):
            conf_uri = URIRef(f"{sensor_uri}/configurable/{idx}")
            g.add((sensor_uri, URIRef(self.bfh + "hasConfigurable"), conf_uri))
            g.add((conf_uri, RDF.type, URIRef(self.bfh + "ConfigurableAssignment")))
            g.add((conf_uri, URIRef(self.schema + "name"), Literal(conf.name)))
            g.add((conf_uri, URIRef(self.bfh + "type"), URIRef(conf.type.rdf_uri)))
            g.add((conf_uri, URIRef(self.schema + "value"), Literal(conf.value)))

        # Logbuch
        for idx, entry in enumerate(sensor_node.logbook):
            log_uri = URIRef(f"{sensor_uri}/log/{idx}")
            g.add((sensor_uri, URIRef(self.bfh + "hasLogEntry"), log_uri))
            g.add((log_uri, RDF.type, URIRef(self.bfh + "LogEntry")))
            g.add((log_uri, URIRef(self.bfh + "logType"), Literal(entry.type.value)))
            g.add((log_uri, URIRef(self.schema + "dateCreated"), Literal(entry.date.isoformat())))
            g.add((log_uri, URIRef(self.schema + "creator"), URIRef(f"http://data.bfh.ch/users/{entry.user.uuid}")))

        # Persistiere Graph
        query = f"""INSERT DATA {{ {g.serialize(format='nt')} }}"""
        self.triplestore_client.update(query)

        return self.find_sensor_node_by_uuid(sensor_node.uuid)
    
    def find_all_sensor_nodes(self) -> List[SensorNodeOutSlim]:
        sparql_query = f"""
        PREFIX schema: <http://schema.org/>
        PREFIX bfh: <http://data.bfh.ch/>

        SELECT ?uuid ?name ?nodeState ?templateUri ?projectUri ?templateUuid ?projectUuid ?templateName ?projectUuid ?projectName ?core ?variant ?templateState ?projectState ?projectShortName
        WHERE {{
        ?s a bfh:SensorNode ;
            bfh:identifier ?uuid ;
            schema:name ?name ;
            bfh:state ?nodeState ;
            bfh:usesNodeTemplate ?templateUri ;
            bfh:partOfProject ?projectUri .

        ?templateUri bfh:identifier ?templateUuid ;
                    schema:name ?templateName ;
                    bfh:state ?templateState ;
                    bfh:boardCore ?core ;
                    bfh:boardVariant ?variant .

        ?projectUri schema:identifier ?projectUuid ;
                    schema:name ?projectName ;
                    bfh:state ?projectState ;
                    schema:alternateName ?projectShortName .
        }}
        """
        res = self.triplestore_client.query(sparql_query)

        return [
            SensorNodeOutSlim(
                uuid=UUID(b['uuid']['value']),
                name=b['name']['value'],
                state=SensorNodeStateEnum.from_rdf_uri(b['nodeState']['value']),
                node_template=NodeTemplateOutSlim(
                    uuid=UUID(b['templateUuid']['value']),
                    name=b['templateName']['value'],
                    board=HardwareBoard(
                        core=b['core']['value'],
                        variant=b['variant']['value']
                    ),
                    state=NodeTemplateStateEnum.from_rdf_uri(b['templateState']['value'])
                ),
                project=ProjectOutSlim(
                    uuid=UUID(b['projectUuid']['value']),
                    name=b['projectName']['value'],
                    state=ProjectStateEnum.from_rdf_uri(b['projectState']['value']),
                    short_name=b['projectShortName']['value']
                )
            )
            for b in res.get('results', {}).get('bindings', [])
        ]

    def find_sensor_node_by_uuid(self, uuid: UUID) -> SensorNodeDB | None:
        sensor_uri = f"<http://data.bfh.ch/sensorNodes/{uuid}>"

        # 1) Basisdaten abfragen
        sparql_base = f"""
        PREFIX schema: <http://schema.org/>
        PREFIX bfh: <http://data.bfh.ch/>

        SELECT ?name ?description ?state ?ttn ?lat ?long ?alt ?postal ?templateUuid ?projectUuid
        WHERE {{
            {sensor_uri} a bfh:SensorNode ;
                        bfh:identifier "{uuid}" ;
                        schema:name ?name ;
                        bfh:state ?state ;
                        bfh:ttnDeviceLink ?ttn ;
                        bfh:usesNodeTemplate ?templateUri ;
                        bfh:partOfProject ?projectUri .
            OPTIONAL {{ {sensor_uri} schema:description ?description }}
            OPTIONAL {{ {sensor_uri} bfh:latitude ?lat }}
            OPTIONAL {{ {sensor_uri} bfh:longitude ?long }}
            OPTIONAL {{ {sensor_uri} bfh:altitude ?alt }}
            OPTIONAL {{ {sensor_uri} bfh:postalcode ?postal }}
            ?templateUri bfh:identifier ?templateUuid .
            ?projectUri schema:identifier ?projectUuid .
        }}
        """
        base_res = self.triplestore_client.query(sparql_base)
        base_bindings = base_res["results"]["bindings"]
        if not base_bindings:
            return None
        base = base_bindings[0]

        sensor_node = SensorNodeDB(
            uuid=uuid,
            name=base["name"]["value"],
            description=base["description"]["value"] if "description" in base else None,
            state=SensorNodeStateEnum.from_rdf_uri(base["state"]["value"]),
            ttn_device_link=base["ttn"]["value"],
            location=SensorNodeLocation(
                latitude=float(base["lat"]["value"]) if "lat" in base else None,
                longitude=float(base["long"]["value"]) if "long" in base else None,
                altitude=int(base["alt"]["value"]) if "alt" in base else None,
                postalcode=base["postal"]["value"] if "postal" in base else None  
            ),
            node_template_uuid=UUID(base["templateUuid"]["value"]),
            project_uuid=UUID(base["projectUuid"]["value"]),
            configurables=[],
            logbook=[]
        )

        # 2) Configurables abfragen
        sparql_config = f"""
        PREFIX schema: <http://schema.org/>
        PREFIX bfh: <http://data.bfh.ch/>

        SELECT ?name ?type ?value
        WHERE {{
            {sensor_uri} bfh:hasConfigurable ?conf .
            ?conf a bfh:ConfigurableAssignment ;
                schema:name ?name ;
                bfh:type ?type ;
                schema:value ?value .
        }}
        """
        config_res = self.triplestore_client.query(sparql_config)
        for row in config_res["results"]["bindings"]:
            sensor_node.configurables.append(
                ConfigurableAssignment(
                    name=row["name"]["value"],
                    type=ConfigurableTypeEnum.from_rdf_uri(row["type"]["value"]),
                    value=row["value"]["value"]
                )
            )

        # 3) Logbuch abfragen
        sparql_logs = f"""
        PREFIX schema: <http://schema.org/>
        PREFIX bfh: <http://data.bfh.ch/>

        SELECT ?logType ?logDate ?creatorUuid ?creatorEmail ?creatorFullName ?creatorRole
        WHERE {{
            {sensor_uri} bfh:hasLogEntry ?logEntry .
            ?logEntry a bfh:LogEntry ;
                    bfh:logType ?logType ;
                    schema:dateCreated ?logDate ;
                    schema:creator ?creator .
            ?creator a schema:Person ;
                    schema:identifier ?creatorUuid ;
                    schema:email ?creatorEmail ;
                    schema:name ?creatorFullName ;
                    bfh:hasRole ?creatorRole .
        }}
        """
        log_res = self.triplestore_client.query(sparql_logs)
        for row in log_res["results"]["bindings"]:
            sensor_node.logbook.append(
                SensorNodeLogbookEntry(
                    type=SensorNodeLogbookEnum(row["logType"]["value"]),
                    date=datetime.fromisoformat(row["logDate"]["value"]),
                    user=UserOut(
                        uuid=row["creatorUuid"]["value"],
                        full_name=row["creatorFullName"]["value"],
                        email=row["creatorEmail"]["value"],
                        role=RoleEnum.from_rdf_uri(row["creatorRole"]["value"])
                    )
                )
            )

        return sensor_node

    def delete_sensor_node(self, uuid: UUID) -> None:
        sparql_query = f"""
        PREFIX schema: <http://schema.org/>
        PREFIX bfh: <http://data.bfh.ch/>

        DELETE {{
            ?s ?p ?o .
        }}
        WHERE {{
            ?s ?p ?o .
            FILTER (
                STRSTARTS(STR(?s), "http://data.bfh.ch/sensorNodes/{uuid}/log/") ||
                STRSTARTS(STR(?s), "http://data.bfh.ch/sensorNodes/{uuid}/configurable/") ||
                STR(?s) = "http://data.bfh.ch/sensorNodes/{uuid}"
            )
        }}
        """
        self.triplestore_client.update(sparql_query)

    def update_sensor_node(self, sensor_node: SensorNodeDB) -> SensorNodeDB:
        self.delete_sensor_node(sensor_node.uuid)
        return self.create_sensor_node(sensor_node)