# Webapp-Backend







# Outline / Notes

- MVC architecture inspired by spring boot
    - Project overview and mvc-similarieties explained
        - strict separation of concern (http, business logic, data access, also: authentication etc.)
        - explanation of spring architecture **quelle suchen**
            - why spring?
            - already experienced with development
            - clear structure of project which can / must be followed
        - fastapi less structured, only given some broad ideas about architecture (https://fastapi.tiangolo.com/tutorial/bigger-applications/)
    - root folder
        - main.py for Fastapi start, router/endpoint inclution and cors handling
        - config.py for configuring project
            - pip package pydantic_settings (earlier part of pydantic, now excluded)
            - configuration:
                - Init admin
                - JWT-secret key
                - Connection to external services like triplestore, compiler-engine, protobuf service and TTN
            - default values, some optional values and all read from environment variables (docker or directly via cli)
            - can be included and read out in classes
        - constants.py for constants that are used accross several classes
        - dependencies.py for dependency injection pattern (explained later)
    - models
        - different formats for creation, data-fetching and used internally (DB)
            - pydantic models (https://docs.pydantic.dev/latest/concepts/models/#basic-model-usage)
                - besides python datatypes, wide range of predefined BaseModels like HttpUrl, also Optional fields
                - automatic type-validation both on API-level and internally when initialising
            - clear defined API, only needed fields, slim dtos
            - dont expose internal fields
            - often used Enums, should be exposed as types in the API (defined in frontend as well)
        - listing and explanation of all business models
            - users with roles (Researcher, Technician, Admin)
                - roles to limit access/permissions:
                    - Researcher read-only, can only look at created data
                    - Technician write-access, used to provision/flash hardware and manage meta data
                    - Admin used for user handling, creating new users
                - used for authenticating with the application
                - written in logbook whenever an entry gets created/updated
            - projects
            - commercial sensor
            - node templates
            - sensor nodes
    - dependency injection, request based
        - Spring boot (https://docs.spring.io/spring-framework/reference/core/beans/dependencies/factory-collaborators.html)
        - instatiation of objects made by framework and only one instance at the time
        - dependencies.py (repositories, services and utils)
        - Router use fastapi Depends() which instanatiates used objects
        - Fastapi request based, everything needed instantiated per Request **research more**
        - Nested dependency injection, services use repositories with Depends()
    - Routers http-only
        - spring equivalent @RestController
        - define Rest api and handles only request and responses
        - convert internal business exceptions to http status codes
        - generated openapi docs based on endpoints and pydantic models
            - used as a contract to frontend
            - /docs exposed openapi, used for testing and debugging
    - services
        - resembles "controller" or @Service, holds all the business logic
        - TTN-Service
            - Used for provisioning of end devices on TTN
                - needs api key 
            - dependency injection with mock / real service, feature flag for development/prod
            - **Block einfügen von docs**
        - Use custom exceptions defined in utils/ folder.
            - Exceptions are more precise and can directly be translated into http status code
            - **table with exception name, status code and status name**
                - NotFoundException when repository returns None -> 404
                - ExternalServiceError -> 502 Bad gateway
                - AuthenticationError -> 401 UNAUTHORIZED
                - AuthorizationError -> 403 Forbidden
                - EmailAlreadyExists -> 409 Conflict
    - repositories


- Security
    - User handling
        - Users can only be registered via an admin user
        - Password handling via Argon2 Passwordhasher
            - **explain algorithm** (https://www.password-hashing.net/argon2-specs.pdf)
    - Authentication over JWT
        - OAuth2 PasswordRequestForm (username/email, password)
            - **research more**
        - jwt library used which offers .encode() and .decode()
        - expire date can be set in minutes over env variable
        - jwt token includes:
            - uuid (for fetching more infos)
            - role (to lock certain functionality in the frontend)
            - email, full_name to display
        - env JWT secret used to encode (security critical!)
        - algorithm: HS256 **research more**

    - Role-based-Authorisation per EndpointNotes
        - nothing exposed anonymously except login
        - Alternatively based on user (pw change)
    
- Extra features
    - Init admin when services started
        - checks if already present
        - generated secure password which is logged once to console