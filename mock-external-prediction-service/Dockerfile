FROM centos:7

ARG ARG_MLOPS_AGENT_VERSION
ARG ARG_MLOPS_AGENT_BUILD
ARG ARG_AGENT_HOST_DIR
ARG PY_LIB_DIR=${ARG_AGENT_HOST_DIR}/datarobot-mlops-agent-${ARG_MLOPS_AGENT_VERSION}/lib/

RUN yum update -y \
&& yum makecache \
&& yum install -y \
    java-1.8.0-openjdk \
    java-1.8.0-openjdk-devel \
    python3 \
    python3-pip \
    python3-setuptools \
    which \
&& yum clean all \
&& rm -rf /root/.cache

ENV JAVA_HOME /etc/alternatives/jre
ENV PATH=$PATH:$JAVA_HOME/bin

ADD datarobot-mlops-agent-${ARG_MLOPS_AGENT_VERSION}-${ARG_MLOPS_AGENT_BUILD}.tar.gz  /opt/datarobot/mlops/
COPY ./mock-external-prediction-service/ /root/
COPY ./src/auto_mpg.py /root/
WORKDIR /root/
RUN pip3 install --no-cache-dir -r requirements.txt \
    && pip3 install ${PY_LIB_DIR}/datarobot_mlops-${ARG_MLOPS_AGENT_VERSION}-py2.py3-none-any.whl

CMD ["bash"]
