# InfrastructureForSensorManagment

## Arbeitsjournal
[Arbeitsjournal](./docs/arbeitsjournal.md)
## Documentation (Draft)
[Documenation](./docs/documentation.md)
## Protocols
Meetings protocols can be found in this [directory](./docs).

## Env Files
The following **.env** files are needed in this directory to populate the compose.yaml with mostly passwords.

Fuseki: **.env-fuseki** to define the admin password of the triplestore
```
ADMIN_PASSWORD=
```

Influxdb: **.env-influxdb** to define the username and password (admin) of the tsdb
```
DOCKER_INFLUXDB_INIT_USERNAME=
DOCKER_INFLUXDB_INIT_PASSWORD=
```

Mosquitto: **.env-mosquitto** to authenticate against the TTN MQTT-broker
```
TTN_USERNAME=
TTN_PASSWORD=

```

## How to merge a feature branch
> **_IMPORTANT:_** The feature branch must be updated with main before merging!
#### Update feature branch with main
![Git rebase](https://microfluidics.utoronto.ca/gitlab/help/topics/git/img/git_rebase_v13_5.png)

How to rebase correctly:
- `git checkout <branch name>`
- `git fetch`
- `git rebase origin/main`
- `git push -f`
#### Merge conflicts
if while rebasing there are conflicts do the following:
- resolve conflicts manually (VS Code has a good conflict solver)
- `git add <files with conflicts>`
- `git commit`
- `git rebase --continue`
- `git push -f`