from app.utils.triplestore_client import TripleStoreClient
from app.models.node_template import (
    NodeTemplateDB, ProtobufDatatypeEnum, NodeTemplateOutSlim, NodeTemplateLogbookEnum, NodeTemplateLogbookEntry, NodeTemplateStateEnum, NodeTemplateField, ConfigurableDefinition, HardwareBoard, ConfigurableTypeEnum)
from app.models.user import UserOut, RoleEnum
from app.models.commercial_sensor import CommercialSensorOutSlim
from rdflib import Graph, URIRef, Literal, RDF

from typing import List
from uuid import UUID
from datetime import datetime


class NodeTemplateRepository:

    def __init__(self, triplestore_client: TripleStoreClient):
        self.triplestore_client = triplestore_client
        self.schema = URIRef("http://schema.org/")
        self.bfh = URIRef("http://data.bfh.ch/")

    def create_node_template(self, node_template: NodeTemplateDB) -> NodeTemplateDB:
        g = Graph()
        g.bind('schema', self.schema)
        g.bind('bfh', self.bfh)

        template_uri = URIRef(f"http://data.bfh.ch/nodeTemplates/{node_template.uuid}")

        # Basisdaten
        g.add((template_uri, RDF.type, URIRef(self.bfh + "NodeTemplate")))
        g.add((template_uri, URIRef(self.bfh + "identifier"), Literal(str(node_template.uuid))))
        g.add((template_uri, URIRef(self.schema + "name"), Literal(node_template.name)))
        g.add((template_uri, URIRef(self.schema + "description"), Literal(node_template.description)))
        g.add((template_uri, URIRef(self.schema + "url"), Literal(str(node_template.gitlab_url))))
        g.add((template_uri, URIRef(self.bfh + "state"), URIRef(node_template.state.rdf_uri)))

        # Board
        g.add((template_uri, URIRef(self.bfh + "boardCore"), Literal(node_template.board.core)))
        g.add((template_uri, URIRef(self.bfh + "boardVariant"), Literal(node_template.board.variant)))

        # Configurables
        for idx, conf in enumerate(node_template.configurables):
            conf_uri = URIRef(f"{template_uri}/configurable/{idx}")
            g.add((template_uri, URIRef(self.bfh + "hasConfigurable"), conf_uri))
            g.add((conf_uri, RDF.type, URIRef(self.bfh + "Configurable")))
            g.add((conf_uri, URIRef(self.schema + "name"), Literal(conf.name)))
            g.add((conf_uri, URIRef(self.bfh + "type"), URIRef(conf.type.rdf_uri)))

        # Felder
        for idx, field in enumerate(node_template.fields or []):
            field_uri = URIRef(f"{template_uri}/field/{idx}")
            g.add((template_uri, URIRef(self.bfh + "hasField"), field_uri))
            g.add((field_uri, RDF.type, URIRef(self.bfh + "Field")))
            g.add((field_uri, URIRef(self.bfh + "fieldName"), Literal(field.field_name)))
            g.add((field_uri, URIRef(self.bfh + "protobufDatatype"), URIRef(field.protbuf_datatype.rdf_uri)))
            g.add((field_uri, URIRef(self.bfh + "unit"), Literal(field.unit)))
            if field.commercial_sensor:
                sensor_uri = URIRef(f"http://data.bfh.ch/commercialSensors/{field.commercial_sensor.uuid}")
                g.add((field_uri, URIRef(self.bfh + "linkedCommercialSensor"), sensor_uri))

        # Logbuch
        for idx, entry in enumerate(node_template.logbook):
            log_uri = URIRef(f"{template_uri}/log/{idx}")
            g.add((template_uri, URIRef(self.bfh + "hasLogEntry"), log_uri))
            g.add((log_uri, RDF.type, URIRef(self.bfh + "LogEntry")))
            g.add((log_uri, URIRef(self.bfh + "logType"), Literal(entry.type.value)))
            g.add((log_uri, URIRef(self.schema + "dateCreated"), Literal(entry.date.isoformat())))
            g.add((log_uri, URIRef(self.schema + "creator"), URIRef(f"http://data.bfh.ch/users/{entry.user.uuid}")))

        # Persistiere Graph
        query = f"""INSERT DATA {{ {g.serialize(format='nt')} }}"""
        self.triplestore_client.update(query)

        return self.find_node_template_by_uuid(node_template.uuid)


    def find_all_node_templates(self) -> List[NodeTemplateOutSlim]:
        sparql_query = f"""
        PREFIX schema: <http://schema.org/>
        PREFIX bfh: <http://data.bfh.ch/>

        SELECT ?uuid ?name ?core ?variant ?state
        WHERE {{
          ?s a bfh:NodeTemplate ;
            bfh:identifier ?uuid ;
            schema:name ?name ;
            bfh:boardCore ?core ;
            bfh:boardVariant ?variant ;
            bfh:state ?state .
        }}
        """
        res = self.triplestore_client.query(sparql_query)
        return [
            NodeTemplateOutSlim(
                uuid=UUID(b['uuid']['value']),
                name=b['name']['value'],
                board=HardwareBoard(
                    core=b["core"]["value"],
                    variant=b["variant"]["value"]
                ),
                state=NodeTemplateStateEnum.from_rdf_uri(b["state"]["value"]),
                )
            for b in res.get('results', {}).get('bindings', [])
        ]
    
    def find_node_template_by_uuid(self, uuid: UUID) -> NodeTemplateDB | None:
        template_uri = f"<http://data.bfh.ch/nodeTemplates/{uuid}>"

        # 1) Basisdaten abfragen
        sparql_base = f"""
        PREFIX schema: <http://schema.org/>
        PREFIX bfh: <http://data.bfh.ch/>

        SELECT ?name ?description ?gitlab_url ?core ?variant ?state
        WHERE {{
            {template_uri} a bfh:NodeTemplate ;
                            bfh:identifier "{uuid}" ;
                            schema:name ?name ;
                            schema:description ?description ;
                            schema:url ?gitlab_url ;
                            bfh:boardCore ?core ;
                            bfh:boardVariant ?variant ;
                            bfh:state ?state .
        }}"""
        base_res = self.triplestore_client.query(sparql_base)
        base_bindings = base_res.get("results", {}).get("bindings", [])
        if not base_bindings:
            return None
        base = base_bindings[0]

        template = NodeTemplateDB(
            uuid=uuid,
            name=base["name"]["value"],
            description=base["description"]["value"],
            gitlab_url=base["gitlab_url"]["value"],
            board=HardwareBoard(
                core=base["core"]["value"],
                variant=base["variant"]["value"]
            ),
            state=NodeTemplateStateEnum.from_rdf_uri(base["state"]["value"]),
            fields=[],
            logbook=[],
            configurables=[]
        )

        # 2) Felder abfragen
        sparql_fields = f"""
        PREFIX schema: <http://schema.org/>
        PREFIX bfh: <http://data.bfh.ch/>

        SELECT ?fieldName ?datatype ?unit ?sensorUuid ?sensorName ?sensorAlias
        WHERE {{
            {template_uri} bfh:hasField ?field .
            ?field a bfh:Field ;
                    bfh:fieldName ?fieldName ;
                    bfh:protobufDatatype ?datatype ;
                    bfh:unit ?unit .
            OPTIONAL {{
                ?field bfh:linkedCommercialSensor ?sensor .
                ?sensor bfh:identifier ?sensorUuid .
                ?sensor schema:name ?sensorName .
                ?sensor schema:alternateName ?sensorAlias .
            }}
        }}"""
        field_res = self.triplestore_client.query(sparql_fields)
        for row in field_res.get("results", {}).get("bindings", []):
            sensor = None
            if "sensorUuid" in row:
                sensor = CommercialSensorOutSlim(
                    uuid=row["sensorUuid"]["value"],
                    name=row["sensorName"]["value"],
                    alias=row["sensorAlias"]["value"]
                )
            template.fields.append(
                NodeTemplateField(
                    field_name=row["fieldName"]["value"],
                    protbuf_datatype=ProtobufDatatypeEnum.from_rdf_uri(row["datatype"]["value"]),
                    unit=row["unit"]["value"],
                    commercial_sensor=sensor
                )
            )

        # 3) Configurables abfragen
        sparql_configurables = f"""
        PREFIX schema: <http://schema.org/>
        PREFIX bfh: <http://data.bfh.ch/>

        SELECT ?name ?type
        WHERE {{
            {template_uri} bfh:hasConfigurable ?config .
            ?config a bfh:Configurable ;
                    schema:name ?name ;
                    bfh:type ?type .
        }}"""
        config_res = self.triplestore_client.query(sparql_configurables)
        for row in config_res.get("results", {}).get("bindings", []):
            template.configurables.append(
                ConfigurableDefinition(
                    name=row["name"]["value"],
                    type=ConfigurableTypeEnum.from_rdf_uri(row["type"]["value"])
                    )
            )

        # 4) Logbuch abfragen
        sparql_logs = f"""
        PREFIX schema: <http://schema.org/>
        PREFIX bfh: <http://data.bfh.ch/>

        SELECT ?logType ?logDate ?creatorUuid ?creatorEmail ?creatorFullName ?creatorRole
        WHERE {{
            {template_uri} bfh:hasLogEntry ?logEntry .
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
            template.logbook.append(
                NodeTemplateLogbookEntry(
                    type=NodeTemplateLogbookEnum(row["logType"]["value"]),
                    date=datetime.fromisoformat(row["logDate"]["value"]),
                    user=UserOut(
                        uuid=row["creatorUuid"]["value"],
                        full_name=row["creatorFullName"]["value"],
                        email=row["creatorEmail"]["value"],
                        role=RoleEnum.from_rdf_uri(row["creatorRole"]["value"])
                    )
                )
            )

        return template


    
    def delete_node_template(self, uuid: UUID) -> None:
        sparql_query = f"""
        PREFIX schema: <http://schema.org/>
        PREFIX bfh: <http://data.bfh.ch/>

        DELETE {{
            ?s ?p ?o .
        }}
        WHERE {{
            ?s ?p ?o .
            FILTER (
                STRSTARTS(STR(?s), "http://data.bfh.ch/nodeTemplates/{uuid}/field/") ||
                STRSTARTS(STR(?s), "http://data.bfh.ch/nodeTemplates/{uuid}/log/") ||
                STRSTARTS(STR(?s), "http://data.bfh.ch/nodeTemplates/{uuid}/configurable/") ||
                STR(?s) = "http://data.bfh.ch/nodeTemplates/{uuid}"
            )
        }}
        """
        self.triplestore_client.update(sparql_query)

    def update_node_template(self, node_template: NodeTemplateDB) -> NodeTemplateDB:
        self.delete_node_template(node_template.uuid)
        return self.create_node_template(node_template)