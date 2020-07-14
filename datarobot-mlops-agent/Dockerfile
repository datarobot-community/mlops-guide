FROM ubuntu:18.04
ARG ARG_MLOPS_AGENT_VERSION
ARG ARG_MLOPS_AGENT_BUILD
ENV DEBIAN_FRONTEND noninteractive
ARG MLOPS_DIR=/opt/datarobot/mlops
ARG PY_LIB_DIR=${MLOPS_DIR}/datarobot-mlops-agent-${ARG_MLOPS_AGENT_VERSION}/lib
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
#ENTRYPOINT ["bash", "/usr/local/bin/mlops-agent-entrypoint.sh"]
COPY ./mock-external-prediction-service/* /root/
COPY ./src/auto_mpg.py /root/
WORKDIR /root/
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install ${PY_LIB_DIR}/datarobot_mlops-${ARG_MLOPS_AGENT_VERSION}-py2.py3-none-any.whl

CMD ["bash"]
