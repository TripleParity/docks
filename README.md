# docks-demo

Docks provides a web interface for managing a [Docker Swarm](https://docs.docker.com/engine/swarm/key-concepts/).


Docks consists of two main components:
- [docks](https://github.com/TripleParity/docks) - REST API to communicate with Docker running on the Swarm Manager
- [docks-ui](https://github.com/TripleParity/docks-ui) - Web interface which communicates with the Docks API to manage the Swarm

## Usage Instructions
1. [Install Docker](https://docs.docker.com/install/)
2. [Install Docker Compose](https://docs.docker.com/compose/install/)
3. Run `sudo docker-compose up` in the docks-demo git directory
  - **Note**: Docker has to download a large amount of data. The process can take up to 30 minutes depending on your internet speed.
  - `sudo docker-compose up -d` can be used to run the containers in the background
4. Browse to http://127.0.0.1:4200 to access the web interface. The API will be running on port `8080`
5. Run `sudo docker-compose down` to stop the running containers

## Warning
The API currently exposes the Docker API without authentication.
Whoever has access to port `8080` or `4200` will effectively have root access.

This will change in the future.
