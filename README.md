Demo of Google client library generators on Cloud Run

To run using Docker:
1. fork and/or clone this repository
1. cd into `cloud_run_clients` directory
1. `docker build -t danoscarmike/cloud-run-clients .`
1. `docker run -d -p 5000:5000 danoscarmike/cloud-run-clients`
1. browse to `https://localhost:5000`
