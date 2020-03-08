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

# Add our code to the Docker image.
RUN git clone https://github.com/googleapis/gapic-generator-python.git

# Install the tool within the image.
RUN pip install ./gapic-generator-python

# Add our code to the Docker image.
RUN mkdir -p /usr/src/cloud-run-clients/
COPY ./* /usr/src/cloud-run-clients/

# Install flask app requirements
RUN pip install -r /usr/src/cloud-run-clients/requirements.txt

# Spin up flask app
CMD ["python3", "/usr/src/cloud-run-clients/main.py"]
