# Rust as the base image
FROM python:3.9.13-slim-buster

# 1. Create a new empty shell project
WORKDIR /app

# 2. Copy our manifests
COPY requirements.txt requirements.txt

#install the requirements
RUN pip3 install -r requirements.txt

#copy files into the enviorement
COPY . .

ENV PYTHON_RUNS_IN_DOCKER=true
CMD [ "python3", "src/__main__.py"]