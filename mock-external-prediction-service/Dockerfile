FROM python:3.6
ARG ARG_MLOPS_AGENT_VERSION
ARG ARG_MLOPS_AGENT_BUILD
ARG MLOPS_DIR=/opt/datarobot/mlops
ARG PY_LIB_DIR=${MLOPS_DIR}/datarobot-mlops-agent-${ARG_MLOPS_AGENT_VERSION}/lib
COPY ./mock-external-prediction-service/* /root/
COPY ./src/auto_mpg.py /root/
WORKDIR /root/
ADD datarobot-mlops-agent-${ARG_MLOPS_AGENT_VERSION}-${ARG_MLOPS_AGENT_BUILD}.tar.gz  /opt/datarobot/mlops/
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install ${PY_LIB_DIR}/datarobot_mlops-${ARG_MLOPS_AGENT_VERSION}-py2.py3-none-any.whl
CMD ["bash"]
