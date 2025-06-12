# Infrastructure for Sensor Management

This repository contains the setup instructions for managing and deploying a distributed sensor management system.
## System Deployment

This section guides DevOps engineers through the process of deploying the system to a production environment.
### Prerequisites

- **Server Access**: User has to have SSH access to the production server
- **Docker Installed**: Docker (or an equivalent container runtime) must be installed on the server. More information can be found in the [Docker installation guide](https://docs.docker.com/engine/install/).
- **DNS Configuration**: DNS records for your domain and subdomains point to your server’s IP address. If deploying to a different domain, adjust the [caddyfile](./config/Caddyfile) accordingly.
The following domains are required:
  - `leaflink.ti.bfh.ch` for the web application
  - `triplestore.ti.bfh.ch` for the Fuseki triplestore
  - `influx.ti.bfh.ch` for the InfluxDB time series database
  - `sparql.ti.bfh.ch` for the YASGUI SPARQL editor


### Step-by-Step Deployment

#### 1. Transfer Docker Compose File
Use `scp` or another secure method to copy `compose-prod.yaml` to your production server.
```
scp compose-prod.yaml user@your-server:/path/to/deploy
```

#### 2. Create Environment Files and Populate Secrets
On the production server, create the necessary `.env` files in the same directory as `compose-prod.yaml`. These files will contain sensitive information such as passwords, API keys, and other configuration values. Ensure these files are not publicly accessible.

The following environment files are required:

- **Fuseki: .env-fuseki** – Contains the admin password for the triplestore
```
ADMIN_PASSWORD=<your_secure_password>      # Admin password for accessing the Fuseki triplestore
```

- **Influxdb: .env-influxdb** – Contains the username and password (admin) for the time series database
```
DOCKER_INFLUXDB_INIT_USERNAME=admin         # Username for the InfluxDB admin account
DOCKER_INFLUXDB_INIT_PASSWORD=<admin_password>  # Password for the InfluxDB admin account
```

- **Backend: .env-backend** – Contains authentication and API credentials for the backend service
```
JWT_SECRET=<random_secure_string>           # Secret key used to sign JWTs for user authentication
INIT_ADMIN_MAIL=<admin_email_address>       # Email address of the default admin account
INIT_ADMIN_PW=<admin_password>              # Password for the default admin account
TTN_APP_ID=<the_things_network_app_id>      # Application ID for your TTN integration
TTN_API_KEY=<ttn_api_key>                   # API key for accessing The Things Network
```

- **Compiler Service: .env-compiler** – Contains configuration variables for the Arduino compiler service
```
DEFAULT_GROUP_ACCESS_TOKEN=<gitlab_group_access_token>                   # Access token to pull source code from GitLab
DEFAULT_GROUP_BOT_USERNAME=<bot_username>                                # Username for the GitLab bot used in automation
DEFAULT_GITLAB_API_URL=https://gitlab.ti.bfh.ch/api/v4/projects         # GitLab API endpoint (usually default)
DEFAULT_SOURCE_DIR=/source                                               # Directory where source files are mounted
DEFAULT_OUTPUT_DIR=/output                                               # Directory where compiled binaries are output
DEFAULT_LOG_DIR=/logs                                                    # Directory for build logs
DEFAULT_ARDUINO_DIR=main                                                 # Default directory inside the repo with Arduino source code
DEFAULT_ARDUINO_BINARY=main.ino.merged.bin                               # Expected binary filename after compilation
DEFAULT_COMPILER_REGISTRY_URL=registry.gitlab.ti.bfh.ch/internetofsoils/infrastructureforsensormanagment/arduino-compiler:latest   # Docker image URL for compiler
CLEANING_INTERVAL_HOURS=24                                               # Interval between cleanup runs
DELETE_OLDER_THAN_DAYS=7                                                 # Age threshold to delete binaries/logs
YAML_FILE_NAME=build-requirements.yaml                                   # Expected YAML config file in source repo
```

- **Mosquitto: .env-mosquitto** – Contains MQTT and TTN authentication credentials
```
MQTT_USERNAME=<mqtt_username>              # Username for accessing the MQTT broker (Mosquitto)
MQTT_PASSWORD=<mqtt_password>              # Password for the MQTT broker
TTN_USERNAME=<ttn_mqtt_username>           # Username for TTN MQTT integration
TTN_PASSWORD=<ttn_mqtt_password>           # Password for TTN MQTT integration
```

- **Parser Service: .env-parser** – Contains credentials required by the parser to access various services
```
INFLUX_TOKEN=<influxdb_token>               # Token for writing data to InfluxDB
FUSEKI_USER=<fuseki_username>               # Username for accessing Fuseki
FUSEKI_PASSWORD=<fuseki_password>           # Password for Fuseki user
MQTT_USERNAME=<mqtt_username>               # MQTT username for subscribing to data
MQTT_PASSWORD=<mqtt_password>               # MQTT password for subscribing to data
```
#### 3. Authenticate with GitLab Container Registry
Log in to the GitLab registry to allow Docker to pull required images.
```
docker login registry.gitlab.ti.bfh.ch -u <username> -p <personal_access_token>
```

#### 4. Start Services
Set the desired version tag and start the containers:
```
export TAG=v1.0.0
docker compose -f compose-prod.yaml up -d --pull
```

#### 5. Verify Logg
After deployment, check service logs to confirm successful startup:
```
docker compose logs
```
