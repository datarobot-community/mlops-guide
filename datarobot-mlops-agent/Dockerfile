FROM openjdk:7
ARG MLOPS_AGENT_VERSION=$MLOPS_AGENT_VERSION
ARG MLOPS_AGENT_BUILD=$MLOPS_AGENT_BUILD
ADD ./datarobot-mlops-agent-${MLOPS_AGENT_VERSION}-${MLOPS_AGENT_BUILD}.tar.gz /srv
WORKDIR /srv/datarobot-mlops-agent-${MLOPS_AGENT_VERSION}/
#RUN /bin/bash ./bin/start-agent.sh
