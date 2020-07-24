#!/usr/bin/env bash

set -e

MODEL_CONFIG_FILE="./model_config/auto-mpg-regressor.json"
TRAINING_DATA_FILE="./data/auto-mpg.csv"

DEPLOYMENT_NAME="External Python Prediction Service"
MLOPS_SERVICE_URL=${DATAROBOT_SERVICE_URL}
API_TOKEN=${DATAROBOT_API_TOKEN}

TOOLS_DIR=${AGENT_HOST_DIR}/datarobot-mlops-agent-${MLOPS_AGENT_VERSION}/tools

python3 $TOOLS_DIR/mlops_client.py deploy \
    --url "${MLOPS_SERVICE_URL}" \
    --token "${API_TOKEN}" \
    --model-config $MODEL_CONFIG_FILE \
    --training-data $TRAINING_DATA_FILE \
    --label "${DEPLOYMENT_NAME}"