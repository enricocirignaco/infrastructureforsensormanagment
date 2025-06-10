# Retrospective: "Internet of Soils - Revised"

# Linked Data

Linked Data refers to a set of best practices for publishing and connecting structured data on the Web. The term encompasses both the technical foundation and the social conventions that enable data from heterogeneous sources to be shared and interlinked using Web technologies. As described by Bizer, Heath, and Berners-Lee, the approach builds upon standard Web protocols such as HTTP and URIs, and uses the Resource Description Framework (RDF) to represent data in a machine-readable format [1].

The authors define Linked Data as "a method of exposing, sharing, and connecting data via dereferenceable URIs on the Web" [1, p. 2]. The goal is to create a global data space—the so-called Web of Data—that is open, extensible, and interconnected in the same way the traditional Web links documents. Linked Data makes it possible for applications to follow links between datasets, retrieve structured information, and discover new data sources at runtime.

The core principles of Linked Data, as stated in the article, are as follows [1, p. 4]:

1. Use URIs as names for things.

2. Use HTTP URIs so that people can look up those names.

3. When someone looks up a URI, provide useful information using standards such as RDF.

4. Include links to other URIs to enable discovery of related data.

These simple but powerful guidelines allow data providers to publish data in a way that not only makes it accessible, but also linkable. This linking aspect is what distinguishes Linked Data from earlier approaches to Web-based data sharing, such as web services or static data dumps.

According to the authors, the Linked Data initiative has already led to the emergence of a decentralized network of interlinked datasets—referred to as the Linked Open Data cloud—which includes domains such as life sciences, geographic information, media, and government data [1, p. 5]. The architecture is intentionally decentralized, which encourages diverse data publishers to participate without requiring prior coordination.

In summary, Linked Data represents a scalable and interoperable approach to publishing structured data. By leveraging the existing Web infrastructure and RDF as a common data model, it enables seamless data integration across institutional and domain boundaries.




Justification for Using Linked Data

    Specific challenges in managing heterogeneous metadata and unstructured sensor-related data

    Need for scalable, flexible, and interoperable data structures

    Comparison with relational databases (e.g., InfluxDB or PostgreSQL)

    Argument for choosing a triple store (semantic queries, evolving schemas, linking external datasets)

RDF: Resource Description Framework

    Triples: subject, predicate, object

    Formal and machine-readable structure

    Serialization formats: Turtle, RDF/XML, JSON-LD

    Example from the project: modeling a sensor and its location as RDF triples

Schemas and Ontologies

    Difference between schemas and ontologies

    Introduction to RDFS and OWL

    Semantic reasoning and data validation

    Usefulness in structuring IoT-related metadata

SOSA Ontology (Sensor, Observation, Sample, Actuator)

    Designed for describing sensors and their observations

    Alignment with IoT data modeling needs

    Examples of SOSA in use: describing sensor nodes, observations, deployments

Schema.org Vocabulary

    General-purpose schema for web data

    Complements domain-specific ontologies like SOSA

    Usage examples: locations, persons, organizations

Advantages of Linked Data in Sensor Infrastructure

    Interoperability across systems and disciplines

    Linking internal and external data sources (e.g., weather data)

    Supports semantic queries (SPARQL)

    Long-term maintainability and extensibility

Triple Stores and Querying

    Introduction to RDF triple stores (e.g., Apache Jena Fuseki)

    How SPARQL endpoints work

    Benefits over traditional relational databases for semantic data access

Summary

    Linked Data as a core design principle for sensor infrastructure

    Enables automation, integration, and future-proof data architecture






[1] C. Bizer, T. Heath, and T. Berners-Lee, “Linked Data – The Story So Far,” International Journal on Semantic Web and Information Systems, vol. 5, no. 3, pp. 1–22, 2009.
[2] W3C, “RDF 1.1 Concepts and Abstract Syntax,” 2014. [Online]. Available: https://www.w3.org/TR/rdf11-concepts/






# Protobuf

- What even is the idea of dataformats?
    - transfered data needs to be in a specified format so that it can be translated into bytes and back into the original data
- Protobuf is binary JSON but with a schema
- different revisions and editions, thesis will use edition 2023 (still very new)
- protoc compiler





https://protobuf.dev/programming-guides/editions/