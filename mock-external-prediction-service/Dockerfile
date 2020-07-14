FROM ubuntu:18.04

ARG ARG_MLOPS_AGENT_VERSION
ARG ARG_MLOPS_AGENT_BUILD
ARG ARG_AGENT_HOST_DIR
ARG PY_LIB_DIR=${ARG_AGENT_HOST_DIR}/datarobot-mlops-agent-${ARG_MLOPS_AGENT_VERSION}/lib/

ENV DEBIAN_FRONTEND noninteractive
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV PATH=$PATH:$JAVA_HOME/bin

RUN apt update \
    && apt install -y --no-install-recommends \
    openjdk-8-jre \
    python3 \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    && apt -y autoclean \
    && rm -rf /var/lib/apt-get/lists/*

ADD datarobot-mlops-agent-${ARG_MLOPS_AGENT_VERSION}-${ARG_MLOPS_AGENT_BUILD}.tar.gz  /opt/datarobot/mlops/
COPY ./mock-external-prediction-service/ /root/
COPY ./src/auto_mpg.py /root/
WORKDIR /root/
RUN pip3 install --no-cache-dir -r requirements.txt \
    && pip3 install ${PY_LIB_DIR}/datarobot_mlops-${ARG_MLOPS_AGENT_VERSION}-py2.py3-none-any.whl

CMD ["bash"]
