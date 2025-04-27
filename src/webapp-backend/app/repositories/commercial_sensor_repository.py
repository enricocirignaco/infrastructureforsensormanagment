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
)
from collections import defaultdict


SCHEMA = Namespace("http://schema.org/")
BFH = Namespace("http://data.bfh.ch/")

class CommercialSensorRepository:
    def __init__(self, triplestore_client: TripleStoreClient):
        self.triplestore_client = triplestore_client

    def _serialize_graph_insert(self, graph: Graph) -> None:
        # Serialize graph as N-Triples and wrap in SPARQL INSERT DATA
        nt_data = graph.serialize(format='nt')
        sparql_insert = f"""
        INSERT DATA {{
            {nt_data}
        }}
        """
        self.triplestore_client.update(sparql_insert)

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
            g.add((bn, BFH.range, Literal(prop.range)))

        # Persist graph
        self._serialize_graph_insert(g)
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
        sparql = f"""
        PREFIX schema: <http://schema.org/>
        PREFIX bfh: <http://data.bfh.ch/>

        SELECT ?sensor ?name ?alias ?description ?linkName ?linkUrl ?linkType ?propName ?unit ?precision ?range
        WHERE {{
          ?sensor a bfh:CommercialSensor ;
                  bfh:identifier "{uuid}" ;
                  schema:name ?name ;
                  schema:alternateName ?alias ;
                  schema:description ?description .

          OPTIONAL {{
            ?sensor schema:hasPart ?link .
            ?link a schema:WebPage ;
                  schema:url ?linkUrl ;
                  bfh:linkType ?linkType .
            OPTIONAL {{ ?link schema:name ?linkName. }}
          }}
          OPTIONAL {{
            ?sensor bfh:hasSensorProperty ?prop .
            ?prop a bfh:SensorProperty ;
                  bfh:propName ?propName ;
                  bfh:unit ?unit ;
                  bfh:precision ?precision ;
                  bfh:range ?range .
          }}
        }}
        """
        res = self.triplestore_client.query(sparql)
        bindings = res.get('results', {}).get('bindings', [])
        if not bindings:
            return None
        grouped = defaultdict(list)
        for row in bindings:
            grouped[row['sensor']['value']].append(row)
        _, rows = next(iter(grouped.items()))
        first = rows[0]
        sensor = CommercialSensorInDB(
            uuid=UUID(first['sensor']['value'].split('/')[-1]),
            name=first['name']['value'],
            alias=first['alias']['value'],
            description=first['description']['value'],
            external_props=[],
            sensor_props=[],
        )
        for row in rows:
            if 'linkUrl' in row and 'linkType' in row:
                sensor.external_props.append(
                    CommercialSensorLink(
                        name=row.get('linkName', {}).get('value'),
                        url=row['linkUrl']['value'],
                        type=CommercialSensorLinkEnum(row['linkType']['value']),
                    )
                )
            if 'propName' in row and 'unit' in row:
                sensor.sensor_props.append(
                    CommercialSensorProps(
                        name=row['propName']['value'],
                        unit=row['unit']['value'],
                        precision=row['precision']['value'],
                        range=row['range']['value'],
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

    def update_commercial_sensor(self, uuid: UUID, commercial_sensor: CommercialSensorOutFull) -> CommercialSensorInDB:
        # Delete old
        self.delete_commercial_sensor(uuid)
        # Recreate new via graph
        sensor_db = CommercialSensorInDB(
            uuid=uuid,
            name=commercial_sensor.name,
            alias=commercial_sensor.alias,
            description=commercial_sensor.description,
            external_props=commercial_sensor.external_props,
            sensor_props=commercial_sensor.sensor_props,
        )
        return self.create_commercial_sensor(sensor_db)
