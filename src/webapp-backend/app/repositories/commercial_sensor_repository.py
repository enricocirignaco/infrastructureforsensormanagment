from typing import List
from uuid import UUID
from datetime import datetime

from rdflib import Graph, URIRef, Literal, RDF

from app.utils.triplestore_client import TripleStoreClient
from app.models.commercial_sensor import (
    CommercialSensorInDB,
    CommercialSensorLink,
    CommercialSensorLinkEnum,
    CommercialSensorProps,
    CommercialSensorOutSlim,
    CommercialSensorOutFull,
    CommercialSensorRange,
    CommercialSensorLogbookEnum,
    CommercialSensorLogbookEntry
)
from app.models.user import UserOut, RoleEnum

class CommercialSensorRepository:
    def __init__(self, triplestore_client: TripleStoreClient):
        self.triplestore_client = triplestore_client
        self.schema = URIRef("http://schema.org/")
        self.bfh = URIRef("http://data.bfh.ch/")


    def create_commercial_sensor(self, commercial_sensor: CommercialSensorInDB) -> CommercialSensorInDB:
        g = Graph()
        g.bind('schema', self.schema)
        g.bind('bfh', self.bfh)

        sensor_uri = URIRef(f"http://data.bfh.ch/commercialSensors/{commercial_sensor.uuid}")

        # Basisdaten
        g.add((sensor_uri, RDF.type, URIRef(self.bfh + "CommercialSensor")))
        g.add((sensor_uri, URIRef(self.bfh + "identifier"), Literal(str(commercial_sensor.uuid))))
        g.add((sensor_uri, URIRef(self.schema + "name"), Literal(commercial_sensor.name)))
        g.add((sensor_uri, URIRef(self.schema + "alternateName"), Literal(commercial_sensor.alias)))
        g.add((sensor_uri, URIRef(self.schema + "description"), Literal(commercial_sensor.description)))

        # External links
        for idx, link in enumerate(commercial_sensor.external_props or []):
            link_uri = URIRef(f"http://data.bfh.ch/commercialSensors/{commercial_sensor.uuid}/link/{idx}")
            g.add((sensor_uri, URIRef(self.schema + "hasPart"), link_uri))
            g.add((link_uri, RDF.type, URIRef(self.schema + "WebPage")))
            g.add((link_uri, URIRef(self.schema + "url"), Literal(link.url)))
            g.add((link_uri, URIRef(self.bfh + "linkType"), URIRef(link.type.rdf_uri)))
            if link.name:
                g.add((link_uri, URIRef(self.schema + "name"), Literal(link.name)))

        # Sensor properties
        for idx, prop in enumerate(commercial_sensor.sensor_props or []):
            prop_uri = URIRef(f"http://data.bfh.ch/commercialSensors/{commercial_sensor.uuid}/property/{idx}")
            g.add((sensor_uri, URIRef(self.bfh + "hasSensorProperty"), prop_uri))
            g.add((prop_uri, RDF.type, URIRef(self.bfh + "SensorProperty")))
            g.add((prop_uri, URIRef(self.bfh + "propName"), Literal(prop.name)))
            g.add((prop_uri, URIRef(self.bfh + "unit"), Literal(prop.unit)))
            g.add((prop_uri, URIRef(self.bfh + "precision"), Literal(prop.precision)))
            g.add((prop_uri, URIRef(self.bfh + "rangeMin"), Literal(prop.range.min)))
            g.add((prop_uri, URIRef(self.bfh + "rangeMax"), Literal(prop.range.max)))

        # Logbuch
        for idx, entry in enumerate(commercial_sensor.logbook):
            log_uri = URIRef(f"http://data.bfh.ch/commercialSensors/{commercial_sensor.uuid}/log/{idx}")
            g.add((sensor_uri, URIRef(self.bfh + "hasLogEntry"), log_uri))
            g.add((log_uri, RDF.type, URIRef(self.bfh + "LogEntry")))
            g.add((log_uri, URIRef(self.bfh + "logType"), Literal(entry.type.value)))
            g.add((log_uri, URIRef(self.schema + "dateCreated"), Literal(entry.date.isoformat())))
            g.add((log_uri, URIRef(self.schema + "creator"), URIRef(f"http://data.bfh.ch/users/{entry.user.uuid}")))

        # Persist graph
        query = f"""INSERT DATA {{ {g.serialize(format='nt')} }}"""
        self.triplestore_client.update(query)

        return self.find_commercial_sensor_by_uuid(commercial_sensor.uuid)

    def find_all_commercial_sensors(self) -> List[CommercialSensorOutSlim]:
        sparql_query = f"""
        PREFIX schema: <http://schema.org/>
        PREFIX bfh: <http://data.bfh.ch/>

        SELECT ?uuid ?name ?alias
        WHERE {{
          ?s a bfh:CommercialSensor ;
             bfh:identifier ?uuid ;
             schema:name ?name ;
             schema:alternateName ?alias .
        }}
        """
        res = self.triplestore_client.query(sparql_query)
        return [
            CommercialSensorOutSlim(
                uuid=UUID(b['uuid']['value']),
                name=b['name']['value'],
                alias=b['alias']['value'],
            )
            for b in res.get('results', {}).get('bindings', [])
        ]

    def find_commercial_sensor_by_uuid(self, uuid: UUID) -> CommercialSensorInDB | None:
        sensor_uri = f"<http://data.bfh.ch/commercialSensors/{uuid}>"

        # 1) Basisdaten abfragen
        sparql_base = f"""
        PREFIX schema: <http://schema.org/>
        PREFIX bfh: <http://data.bfh.ch/>

        SELECT ?name ?alias ?description
        WHERE {{
          {sensor_uri} a bfh:CommercialSensor ;
                         bfh:identifier "{uuid}" ;
                         schema:name ?name ;
                         schema:alternateName ?alias ;
                         schema:description ?description .
        }}"""
        base_res = self.triplestore_client.query(sparql_base)
        base_bindings = base_res.get("results", {}).get("bindings", [])
        if not base_bindings:
            return None
        base = base_bindings[0]

        sensor = CommercialSensorInDB(
            uuid=uuid,
            name=base['name']['value'],
            alias=base['alias']['value'],
            description=base['description']['value'],
            external_props=[],
            sensor_props=[],
            logbook=[]
        )

        # 2) Links abfragen
        sparql_links = f"""
        PREFIX schema: <http://schema.org/>
        PREFIX bfh: <http://data.bfh.ch/>

        SELECT ?linkUrl ?linkName ?linkType
        WHERE {{
          {sensor_uri} schema:hasPart ?link .
          ?link a schema:WebPage ;
                schema:url ?linkUrl ;
                bfh:linkType ?linkType .
          OPTIONAL {{ ?link schema:name ?linkName . }}
        }}"""
        link_res = self.triplestore_client.query(sparql_links)
        for row in link_res.get("results", {}).get("bindings", []):
            sensor.external_props.append(
                CommercialSensorLink(
                    name=row.get('linkName', {}).get('value'),
                    url=row['linkUrl']['value'],
                    type=CommercialSensorLinkEnum.from_rdf_uri(row['linkType']['value'])
                )
            )

        # 3) Sensor-Eigenschaften abfragen
        sparql_props = f"""
        PREFIX bfh: <http://data.bfh.ch/>

        SELECT ?propName ?unit ?precision ?rangeMin ?rangeMax
        WHERE {{
          {sensor_uri} bfh:hasSensorProperty ?prop .
          ?prop a bfh:SensorProperty ;
                bfh:propName ?propName ;
                bfh:unit ?unit ;
                bfh:precision ?precision ;
                bfh:rangeMin ?rangeMin ;
                bfh:rangeMax ?rangeMax .
        }}"""
        prop_res = self.triplestore_client.query(sparql_props)
        for row in prop_res.get("results", {}).get("bindings", []):
            sensor.sensor_props.append(
                CommercialSensorProps(
                    name=row['propName']['value'],
                    unit=row['unit']['value'],
                    precision=row['precision']['value'],
                    range=CommercialSensorRange(
                        min=row['rangeMin']['value'],
                        max=row['rangeMax']['value']
                    )
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
        }}"""
        log_res = self.triplestore_client.query(sparql_logs)
        for row in log_res.get("results", {}).get("bindings", []):
            sensor.logbook.append(
                CommercialSensorLogbookEntry(
                    type=CommercialSensorLogbookEnum(row['logType']['value']),
                    date=datetime.fromisoformat(row['logDate']['value']),
                    user=UserOut(
                        uuid=row['creatorUuid']['value'],
                        full_name=row['creatorFullName']['value'],
                        email=row['creatorEmail']['value'],
                        role=RoleEnum.from_rdf_uri(row['creatorRole']['value'])
                    )
                )
            )

        return sensor

    def delete_commercial_sensor(self, uuid: UUID) -> None:
        sparql_delete = f"""
        PREFIX schema: <http://schema.org/>
        PREFIX bfh: <http://data.bfh.ch/>

        DELETE {{
            ?s ?p ?o
        }}
        WHERE {{
            ?s ?p ?o .
            FILTER (
                STRSTARTS(STR(?s), "http://data.bfh.ch/commercialSensors/{uuid}/link/") ||
                STRSTARTS(STR(?s), "http://data.bfh.ch/commercialSensors/{uuid}/property/") ||
                STRSTARTS(STR(?s), "http://data.bfh.ch/commercialSensors/{uuid}/log/") ||
                STR(?s) = "http://data.bfh.ch/commercialSensors/{uuid}"
            )
        }}
        """
        self.triplestore_client.update(sparql_delete)


    def update_commercial_sensor(self, commercial_sensor: CommercialSensorOutFull) -> CommercialSensorInDB:
        self.delete_commercial_sensor(commercial_sensor.uuid)
        sensor_db = CommercialSensorInDB(**commercial_sensor.model_dump())
        return self.create_commercial_sensor(sensor_db)
