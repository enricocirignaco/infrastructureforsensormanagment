# Retrospective: "Internet of Soils - Revised"

# Linked Data

The term Linked Data denotes a set of best practices for publishing and interconnecting structured data on the Web. According to Bizer et al., these practices have led in the past three years to the emergence of a global data space containing billions of assertions, commonly referred to as the Web of Data [1, p. 1].

At its core, Linked Data uses four principles—originally formulated by Tim Berners‑Lee—as a basic recipe for exposing and linking data using existing Web infrastructure [1, p. 2]:

1. **Use URIs to identify resources**. Every entity, such as a sensor, a location, or a measurement, is assigned a globally unique and persistent URI.

2. **Use HTTP URIs**. These URIs should be dereferenceable, meaning that they can be accessed via the HTTP protocol.

3. **Provide structured data**. When a URI is dereferenced, it should return useful information in standardized, machine-readable formats such as RDF or JSON-LD.

4. **Include links to other URIs**. This enables discovery of related data and supports the construction of a broader knowledge graph.

These simple yet powerful guidelines enable data providers to publish information in a way that is not only accessible but also inherently linkable. This emphasis on interlinking is what fundamentally sets Linked Data apart from earlier approaches to Web-based data sharing, such as static data dumps or traditional web services. By extending the Web’s hyperlink architecture to structured data through the use of URIs, HTTP, RDF, and semantic links between resources, Linked Data facilitates the construction of a decentralized, scalable, and machine-readable knowledge graph. This graph-based structure supports advanced data integration, semantic interoperability and exploratory analysis across diverse domains. At the core of this approach lies the *Resource Description Framework* (RDF), which serves as the fundamental data model for Linked Data applications.

RDF is a standard for representing structured information in a formal and machine-readable way. It organizes data as triples, each consisting of a subject, predicate and object. This structure allows for the expression of simple statements about resources. Each element of a triple is typically identified by a Uniform Resource Identifier (URI) or a literal value, making the data unambiguous and interoperable. RDF supports multiple serialization formats such as Turtle, RDF/XML and JSON-LD, which offer flexibility for different systems and integration needs. The underlying concepts and structure of RDF are formally defined in the W3C RDF 1.1 specification [2].

## Justification for Using Linked Data

Our sensor management platform is designed to support a wide range of independent projects, each of which may involve different types and quantities of sensor nodes. These projects often have no shared context, resulting in highly diverse data formats, metadata structures and additional informations. Consequently, the underlying data infrastructure must be capable of handling heterogeneous and evolving datasets in a consistent and interoperable way. Traditional rigid data models quickly reach their limits in such environments.

The use of RDF enables us to describe entities such as sensors, observed phenomena and spatial relationships in a structured and machine-readable way. For instance, a sensor can be represented by a triple stating that it "is located at" a specific place, with both the sensor and the location identified by URIs. This model not only facilitates semantic querying but also allows the system to evolve dynamically as new types of metadata or sensors are introduced. Through SPARQL, complex queries can be performed without needing to redesign the data schema.

A further advantage of Linked Data is its ability to seamlessly integrate distributed knowledge sources. In our platform, relevant metadata such as data sheets, calibration data or manufacturer specifications are often stored externally and exist in a variety of formats. Rather than importing and replicating these documents, Linked Data enables us to reference them directly via persistent URIs. This avoids duplication and enables scalable metadata enrichment.

In contrast to relational databases such as InfluxDB or PostgreSQL, which rely on fixed schemas and lack native support for semantic relationships, RDF-based triple stores offer a more adaptable solution. They are inherently suited to scenarios where data structures are not known in advance or change frequently over time. The ability to link internal datasets with external ontologies further enhances interoperability and long-term maintainability.

**noch nicht zufrieden:** \
Given these requirements—heterogeneous data, flexible schemas, and the need for distributed metadata integration—Linked Data provides an ideal foundation for our sensor infrastructure. It supports modularity, interoperability and the integration of semantically rich metadata across projects and domains.

## Usage of existing Schemas and Ontologies

In the context of Linked Data, schemas and ontologies are essential tools for adding semantic structure and meaning to data. While these terms are often used interchangeably, they differ in scope and expressiveness. A schema typically defines the structure and types of data entities—comparable to a data model—whereas an ontology provides a richer semantic framework, including relationships, constraints and inference rules. Ontologies can express not only what data exists, but also how entities relate to one another and what logical conclusions can be derived from the data.

The W3C has established standards for semantic modeling with RDF Schema (RDFS) and the Web Ontology Language (OWL). RDFS extends RDF by introducing basic vocabulary for defining classes, properties and hierarchies. OWL goes further by supporting more complex constructs such as class equivalence, property restrictions and logical axioms. These features enable semantic reasoning and consistency checking across datasets. Semantic reasoning allows new knowledge to be inferred from existing data, while validation mechanisms can help ensure data integrity and coherence [3].

A domain-specific example of such an ontology is the SOSA (Sensor, Observation, Sample, and Actuator) ontology, developed by the W3C Spatial Data on the Web Working Group [4]. SOSA is specifically designed to describe sensors, the observations they make, and the processes and platforms involved. It is well-aligned with the needs of Internet of Things (IoT) applications, where metadata about sensor deployments, measurement procedures and observed properties must be consistently modeled. In our platform, SOSA concepts are used to represent sensor nodes, their deployments in the field and the observations they produce. This enables consistent semantic annotation of sensor metadata and supports data integration across different types of sensing systems.

In addition to SOSA, general-purpose vocabularies such as Schema.org are useful for modeling contextual metadata. Schema.org is widely used to describe common entities like people, places, organizations and events [5]. While SOSA captures the technical aspects of sensing, Schema.org can provide additional descriptive context, such as the institution operating a sensor or the geographic location where it is deployed. These complementary vocabularies allow for both domain-specific precision and broader semantic interoperability.

Using well-established ontologies provides several concrete advantages. First, they are typically developed and maintained by expert communities, ensuring conceptual clarity and practical relevance. Second, they enable semantic alignment across datasets, allowing data to be linked meaningfully across systems that follow the same ontological models. This is a core strength of Linked Data: enabling the integration of decentralized data sources through shared semantic structures. Furthermore, leveraging existing ontologies accelerates development, reduces modeling errors and supports long-term maintainability of data systems.


Advantages of Linked Data in Sensor Infrastructure

    Interoperability across systems and disciplines

    Linking internal and external data sources (e.g., weather data)

    Supports semantic queries (SPARQL)

    Long-term maintainability and extensibility

Triple Stores and Querying

    Introduction to RDF triple stores (e.g., Apache Jena Fuseki)

    How SPARQL endpoints work
     
    sparql abfrage zeigen

    Benefits over traditional relational databases for semantic data access

Summary

    Linked Data as a core design principle for sensor infrastructure

    Enables automation, integration, and future-proof data architecture






[1] C. Bizer, T. Heath, and T. Berners-Lee, “Linked Data – The Story So Far,” International Journal on Semantic Web and Information Systems, vol. 5, no. 3, pp. 1–22, 2009.
[2] W3C, “RDF 1.1 Concepts and Abstract Syntax,” 2014. [Online]. Available: https://www.w3.org/TR/rdf11-concepts/
[3] W3C, "RDF Schema 1.1," Feb. 2014. [Online]. Available: https://www.w3.org/TR/rdf-schema/
[4] K. Janowicz, A. Haller, S. J. D. Cox, M. Lefrançois, and K. Taylor, "SOSA: A lightweight ontology for sensors, observations, samples, and actuators," Journal of Web Semantics, vol. 56, 2019. [Online]. Available: https://doi.org/10.1016/j.websem.2019.100378
[5] Schema.org, "Schema.org vocabulary." [Online]. Available: https://schema.org/






# Protobuf

- What even is the idea of dataformats?
    - transfered data needs to be in a specified format so that it can be translated into bytes and back into the original data
- Protobuf is binary JSON but with a schema
- different revisions and editions, thesis will use edition 2023 (still very new)
- protoc compiler





https://protobuf.dev/programming-guides/editions/