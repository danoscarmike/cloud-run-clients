FROM python:3.7-slim

# Install system packages.
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    pandoc \
  && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y git

# Add protoc and our common protos.
COPY --from=gcr.io/gapic-images/api-common-protos:0.1.0 /usr/local/bin/protoc /usr/local/bin/protoc
COPY --from=gcr.io/gapic-images/api-common-protos:0.1.0 /protos/ /protos/

# Clone into googleapis/googleapis
RUN git clone https://github.com/googleapis/googleapis.git

# Install the tool within the image.
RUN pip install gapic-generator

# Add our code to the Docker image.
RUN mkdir -p /src/
COPY ./ /src/

# Install flask app requirements
RUN pip install -r /src/requirements.txt
WORKDIR  /src/
ENV FLASK_APP=cloud_run_clients
ENV FLASK_DEBUG=0

# Spin up flask app
ENTRYPOINT ["flask", "run", "--host", "0.0.0.0"]
