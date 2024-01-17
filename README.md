# Team Caturanga: Simulation of IDP movement

## Description
Student project as part of a Software Engineering lecture at University of Augsburg.
Collaboration of University Augsburg, Netlight, and the World Food Programme.

## Installation
1. Clone this repository
2. Add MONGO_URI, ACLED_API_KEY & ACLED_API_MAIL in .env file
3. `git submodule update --init` to clone the FLEE submodule

# Deployment
- frontend and backend are deployed as docker containers on AWS ECS
- two API Gateways access the frontend and backend containers via the IP address of the container directly (not via the load balancer for less costs)
- as database, Amazon DocumentDB is used
- the secrets to access the database are stored in AWS Secrets Manager
- push to main branch
- github actions will do the following actions:
  - run tests and build docker image
  - docker image will be pushed to aws ecr
  - aws ecs will pull the image and deploy it to the cluster, by forcing a new deployment of the existing service
  - the Python script `deployment_scripts/restart_service.py <CLUSTER_NAME> <SERVICE_NAME> <API_GATEWAY_ID>` fetches the IP address of the new container and updates the API Gateway with the new IP address
  - the API Gateway will now route all requests to the new container, while the IP address of the frontend and backend API Gateways remain the same

### Requirements
- Docker

## Usage
To run the tool locally, execute
```
docker compose up
```

## Contributing
During frontend development only run backend with docker and then execute the following commands:
```
cd frontend
npm install
npm run dev
```

### Additional Requirements
- node (v20.9.0)

## Authors
- Jonas Maurer
- Klara Cimbalnik
- Miguel Marcano
- Nicolas Schmitt
- Nils Sirrenberg
- Pascal Wackler

## Project status
Developing until the project presentation on 19th January 2024.
