from typing import List
from uuid import UUID

from rdflib import Graph, Namespace, URIRef, BNode, Literal
from rdflib.namespace import RDF

from app.utils.triplestore_client import TripleStoreClient
from app.models.commercial_sensor import (
    CommercialSensorInDB,
    CommercialSensorLink,
    CommercialSensorLinkEnum,
    CommercialSensorProps,
    CommercialSensorOutSlim,
    CommercialSensorOutFull,
    CommercialSensorRange
)
from collections import defaultdict


SCHEMA = Namespace("http://schema.org/")
BFH = Namespace("http://data.bfh.ch/")

class CommercialSensorRepository:
    def __init__(self, triplestore_client: TripleStoreClient):
        self.triplestore_client = triplestore_client

    def create_commercial_sensor(self, commercial_sensor: CommercialSensorInDB) -> CommercialSensorInDB:
        g = Graph()
        g.bind('schema', SCHEMA)
        g.bind('bfh', BFH)

        subj = URIRef(f"http://data.bfh.ch/commercial_sensors/{commercial_sensor.uuid}")
        # Core triples
        g.add((subj, RDF.type, BFH.CommercialSensor))
        g.add((subj, BFH.identifier, Literal(str(commercial_sensor.uuid))))
        g.add((subj, SCHEMA.name, Literal(commercial_sensor.name)))
        g.add((subj, SCHEMA.alternateName, Literal(commercial_sensor.alias)))
        g.add((subj, SCHEMA.description, Literal(commercial_sensor.description)))

        # External links
        for link in commercial_sensor.external_props or []:
            bn = BNode()
            g.add((subj, SCHEMA.hasPart, bn))
            g.add((bn, RDF.type, SCHEMA.WebPage))
            if link.name:
                g.add((bn, SCHEMA.name, Literal(link.name)))
            g.add((bn, SCHEMA.url, Literal(link.url)))
            g.add((bn, BFH.linkType, Literal(link.type.value)))

        # Sensor properties
        for prop in commercial_sensor.sensor_props or []:
            bn = BNode()
            g.add((subj, BFH.hasSensorProperty, bn))
            g.add((bn, RDF.type, BFH.SensorProperty))
            g.add((bn, BFH.propName, Literal(prop.name)))
            g.add((bn, BFH.unit, Literal(prop.unit)))
            g.add((bn, BFH.precision, Literal(prop.precision)))
            g.add((bn, BFH.rangeMin, Literal(prop.range.min)))
            g.add((bn, BFH.rangeMax, Literal(prop.range.max)))

        # Persist graph
        query = f"""INSERT DATA {{ {g.serialize(format="nt")} }}"""
        self.triplestore_client.update(query)

        return self.find_commercial_sensor_by_uuid(commercial_sensor.uuid)

    def find_all_commercial_sensors(self) -> List[CommercialSensorOutSlim]:
        # Using SPARQL SELECT via triplestore
        sparql = f"""
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
        res = self.triplestore_client.query(sparql)
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
            sensor_props=[]
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

        return sensor

    def delete_commercial_sensor(self, uuid: UUID) -> None:
        sparql = f"""
        PREFIX bfh: <http://data.bfh.ch/>
        DELETE WHERE {{
          <http://data.bfh.ch/commercial_sensors/{uuid}> ?p ?o .
        }}
        """
        self.triplestore_client.update(sparql)

    def update_commercial_sensor(self, commercial_sensor: CommercialSensorOutFull) -> CommercialSensorInDB:
        self.delete_commercial_sensor(commercial_sensor.uuid)
        sensor_db = CommercialSensorInDB(**commercial_sensor.model_dump())
        return self.create_commercial_sensor(sensor_db)
