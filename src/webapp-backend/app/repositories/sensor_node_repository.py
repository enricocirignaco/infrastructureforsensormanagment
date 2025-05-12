from app.utils.triplestore_client import TripleStoreClient
from app.models.sensor_node import SensorNodeDB, SensorNodeOutSlim, SensorNodeOutFull, SensorNodeStateEnum
from app.models.node_template import NodeTemplateOutSlim, HardwareBoard, NodeTemplateStateEnum
from app.models.project import ProjectOutSlim, ProjectStateEnum

from rdflib import Graph, URIRef, Literal, RDF
from uuid import UUID
from typing import List

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
        if sensor_node.latitude is not None:
            g.add((sensor_uri, URIRef(self.bfh + "latitude"), Literal(sensor_node.latitude)))
        if sensor_node.longitude is not None:
            g.add((sensor_uri, URIRef(self.bfh + "longitude"), Literal(sensor_node.longitude)))
        if sensor_node.altitude is not None:
            g.add((sensor_uri, URIRef(self.bfh + "altitude"), Literal(sensor_node.altitude)))
        if sensor_node.postalcode:
            g.add((sensor_uri, URIRef(self.bfh + "postalcode"), Literal(sensor_node.postalcode)))

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

        SELECT ?uuid ?name ?nodeState ?templateUuid ?templateName ?projectUuid ?projectName ?core ?variant ?templateState ?projectState ?projectShortName
        WHERE {{
        ?s a bfh:SensorNode ;
            bfh:identifier ?uuid ;
            schema:name ?name ;
            bfh:state ?state ;
            bfh:usesNodeTemplate ?templateUri ;
            bfh:partOfProject ?projectUri .

        ?templateUri bfh:identifier ?templateUuid ;
                    schema:name ?templateName .
                    bfh:state ?templateState ;
                    bfh:boardCore ?core ;
                    bfh:boardVariant ?variant .

        ?projectUri bfh:identifier ?projectUuid ;
                    schema:name ?projectName .
                    bfh:state ?projectState .
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

    