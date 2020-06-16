FROM python:3.8
COPY ./automl-consumer/* root/
COPY ./src/auto_mpg.py root/
WORKDIR root/
RUN pip install --no-cache-dir -r requirements.txt
