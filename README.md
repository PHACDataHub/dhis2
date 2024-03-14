# DHIS2 Demo

This captures the steps required to run a local copy of DHIS2.
k8s set up -> https://github.com/PHACDataHub/dhis-2

## empty the database with out deleting it
```bash
# If all of your tables are in a single schema, this approach could work (below code assumes that the name of your schema is public)
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

# If you are using PostgreSQL 9.3 or later, you may also need to restore the default grants.

GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;
```

## access postgres in docker container

```bash
docker exec -it compose-db-1 /bin/bash
psql -d dhis -U dhis
```
  
## Local docker-compose

```bash
# use compose files from ./compose 
# if you are in the VM:
git clone https://github.com/PHACDataHub/dhis2.git && cd phac-dhis2

cd compose
# stop the app and delete the db-dump volume
docker compose down --volumes

# If you want to start DHIS2 with a specific demo DB you can pass a URL like
# DHIS2_DB_DUMP_URL=https://databases.dhis2.org/sierra-leone/2.39/dhis2-db-sierra-leone.sql.gz 
# which is the default in our compose file
docker compose up -d
docker compose logs -f

open http://localhost:8080
```

## Pulumi

Select the backend and setup gcloud auth

```bash
# Select the state backend (local)

# From repo top level - until we start using a GCP bucket for state
mkdir PulumiState && pulumi login "file:$PWD/PulumiState"
pulumi login file:/Users/daniel/Code/PHAC/phac-dhis2/PulumiState
# required to operate on GCP
gcloud auth application-default login
```

#### Bring up the existing stack

```bash
# From repo top level
cd docker-vm
gcloud auth login
gcloud auth application-default login
pulumi up
```

#### GCP-VM-Docker - GCP - intial setup

```bash
mkdir docker-vm && cd docker-vm
pulumi new gcp-typescript
# set the project scope, customizedable
pulumi config set gcp:project pdcp-cloud-009-danl
pulumi up
```

#### Finalize inside the VM

```bash
# Show all the outputs
pulumi stack output
# get the external ip
pulumi stack output externalIP

# add user to docker group: 'till I figure out how to get the $USER in the init script
gcloud compute ssh --zone "$(pulumi stack output instanceZone)" "$(pulumi stack output instanceName)" --command 'sudo usermod -aG docker $USER'

# ssh into the machine
gcloud compute ssh --zone "$(pulumi stack output instanceZone)" "$(pulumi stack output instanceName)" 

# smoke test
docker run --rm hello-world

# git clone; docker compose...
# from https://github.com/dhis2/dhis2-core/blob/master/docker-compose.yml
```

#### Cleanup

```bash
# clean up resources
pulumi destroy
# remove 'dev' stack and history
pulumi stack rm dev
```

### QuickStart - WebBucket

Start a GCP typescript pulumi project with local state

```bash
mkdir quickstart && cd quickstart
pulumi new gcp-typescript
# set the project scope
pulumi config set gcp:project pdcp-cloud-009-danl
pulumi up
# clean up resources
pulumi destroy
# remove 'dev' stack and history
pulumi stack rm dev
```

## Org

- Sujani, Lisa, Elizaveta are intake team - DST Team - Data Science Team
- Diana, Jenny, Amanda SRHD - Substance Realated Harms Division

## References

- [DHIS2 Core Repo](https://github.com/dhis2/dhis2-core)
- [DHIS2 Implementation Guide](https://docs.dhis2.org/en/implement/implement.html)
- [DHIS2 Developer Portal](https://developers.dhis2.org/)
- [Developer Portal Repo](https://github.com/dhis2/developer-portal)
- [Code Repo](https://github.com/dhis2/dhis2-core#run-dhis2-in-docker)
- [Pulumi AI](https://www.pulumi.com/ai/)
