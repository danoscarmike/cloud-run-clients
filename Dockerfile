FROM python:3.7-slim

# Create user so app isn't run as root
RUN adduser cloudrunclients

# Install system packages
RUN apt-get update \
  && apt-get install -y --no-install-recommends pandoc \
  && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
  && apt-get install -y git

# Add protoc and Google's common protos and API proto repository
COPY --from=gcr.io/gapic-images/api-common-protos:0.1.0 /usr/local/bin/protoc /usr/local/bin/protoc
COPY --from=gcr.io/gapic-images/api-common-protos:0.1.0 /protos/ /protos/
RUN git clone https://github.com/googleapis/googleapis.git

# Install the Python client generator
RUN pip install gapic-generator

# Set default working directory to user's home
WORKDIR /home/cloudrunclients
RUN mkdir upload
RUN mkdir download
RUN mkdir client
RUN mkdir proto

# Install dependencies in python virtual environment
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy over app files
COPY app app
COPY config.py cloud_run_clients.py ./

# Copy over development database
COPY app.db ./

# Install flask app requirements
ENV FLASK_APP=cloud_run_clients
ENV FLASK_ENV=development

# Spin up flask app
ENTRYPOINT ["flask", "run", "--host", "0.0.0.0"]
