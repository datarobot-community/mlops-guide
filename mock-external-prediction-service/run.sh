#!/usr/bin/env bash

set -e

echo "Starting MLOps-Agent"
echo
echo
echo

cd "${AGENT_HOST_DIR}/datarobot-mlops-agent-${MLOPS_AGENT_VERSION}" || exit

bash ./bin/start-agent.sh
echo "running: $@"
exec "$@"

echo "Starting Prediction Service"
echo
echo
echo

cd "/root"

python3 external_predictions.py
