
- while the previous chapter was more of a conceptual overview, this chapter will show the technical detail of the developed system and give a broad overview over all of its components
- a number of microservices was developed and deployed during the process and they interact with each other in specified ways. This makes both the whole system and its component portable, scalable and each component can be developed, tested and deployed independently.
- orange cloud called "Cloud Infrastrcuture" in previous chapter is now displayed in detail in the following visualization.

![System Architecture](../images/system_architecture.png)

- every block within the orange cloud resembles a microservice, more precise a docker container
- whole system is containerized and managed through docker compose to simply development and ensure consistent environemnt setups. This way, local and cloud deployment can be supported, only differentiating by their configuration.
- White blocks symbolize external images, blue ones are self-developed blocks to implement the needed functionality of the system. These blue ones are explained in greater detail in subsequent sections of this chapter.