FROM ubuntu:18.04
ARG ARG_MLOPS_AGENT_VERSION
ARG ARG_MLOPS_AGENT_BUILD
ENV DEBIAN_FRONTEND noninteractive
RUN apt update \
    && apt install -y --no-install-recommends \
    openjdk-8-jre \
    python \
    python3 \
    && apt -y autoclean \
    && rm -rf /var/lib/apt-get/lists/*
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV PATH=$PATH:$JAVA_HOME/bin
ADD datarobot-mlops-agent-${ARG_MLOPS_AGENT_VERSION}-${ARG_MLOPS_AGENT_BUILD}.tar.gz  /opt/datarobot/mlops/
COPY datarobot-mlops-agent/mlops-agent-entrypoint.sh /usr/local/bin/
WORKDIR /opt/datarobot/mlops/datarobot-mlops-agent-${ARG_MLOPS_AGENT_VERSION}
ENTRYPOINT ["bash", "/usr/local/bin/mlops-agent-entrypoint.sh"]
CMD ["bash"]
