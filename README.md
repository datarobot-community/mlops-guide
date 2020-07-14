# MLOps Guide

This is example code not meant for production. 

This repo contains example code for learning and understanding MLOps
in DataRobot. In this example we use `docker-compose.yml` to illustrate a
reference architecture. The goal of this project is to make it easy to
understand how to use and instrument MLOps using both DataRobot natively hosted
models and prediction services as well as those not hosted in DataRobot.

**Dependencies**
* Auto MPG model deployed. See [Quickstart Guide](https://api-docs.datarobot.com/docs/quickstart-guide)
* [Docker](https://docs.docker.com/get-docker/)
* [Docker-compose](https://docs.docker.com/compose/install/)
* mlops-agent
  1. Download from [DataRobot](https://app2.datarobot.com)>User Menu> Developer Tools
  1. Move `tar.gz` file to the root of this project


## Usage
Copy and configure `example.env` and `example.mlops.conf.yaml` e.g.:
  * `cp example.env .env`
  * Populate with relevant values e.g.:
    * DATAROBOT_API_TOKEN [instructions](https://api-docs.datarobot.com/docs/api-access-guide)
    * DATAROBOT_ENDPOINT [instructions](https://api-docs.datarobot.com/docs/guide-to-different-datarobot-endpoints)
    * KEEP_ALIVE=600
    * ENV_MLOPS_AGENT_VERSION=6.1.5
    * ENV_MLOPS_AGENT_BUILD=325
    * ENV_MLOPS_DEPLOYMENT_ID & ENV_MLOPS_MODEL_ID [instructions](https://community.datarobot.com/t5/support-knowledge-base/what-are-project-id-model-id-and-deployment-id-where-to-find/ta-p/4643)
  * `cd .docker/mlops-agent/etc`
  * `cp example.mlops.conf.yaml mlops.conf.yaml`
  * Populate `apiToken` in `mlops.conf.yaml` [instructions](https://api-docs.datarobot.com/docs/api-access-guide)

Create a deployment reference to your external prediction service:
```shell script
docker-compose run --rm --entrypoint="/bin/bash register_deployment.sh" mock-external-prediction-service
```
This will produce something like:
```shell script
WARNING: The ENV_MLOPS_DEPLOYMENT_ID variable is not set. Defaulting to a blank string.
WARNING: The ENV_MLOPS_MODEL_ID variable is not set. Defaulting to a blank string.
Uploading training data - /root/data/auto-mpg.csv. This may take some time...
Training dataset uploaded. Catalog ID <catalog id>.

======== DEPLOYMENT CONFIGURATION SUMMARY ========
export MLOPS_DEPLOYMENT_ID=<deployment id>; export MLOPS_MODEL_ID=<model id>
```

Run examples:
```shell script
docker-compose up
```

Stop with: `ctl-d`

## Development and Contributing

If you'd like to report an issue or bug, suggest improvements, or contribute code to this project, please refer to [CONTRIBUTING.md](CONTRIBUTING.md).


# Code of Conduct

This project has adopted the Contributor Covenant for its Code of Conduct. 
See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) to read it in full.

# License

Licensed under the Apache License 2.0. 
See [LICENSE](LICENSE) to read it in full.


