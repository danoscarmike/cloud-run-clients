Demo of Google client library generators on Cloud Run

To run locally:
1. fork and/or clone this repository
1. cd into `cloud_run_clients` directory
1. `pip3 install -r requirements.txt`
1. `python3 main.py local`
1. browse to `https://localhost:8080`

To run using Docker:
1. fork and/or clone this repository
1. cd into `cloud_run_clients` directory
1. `docker build -t danoscarmike/cloud-run-clients .`
1. `docker run -d -p 5000:5000 danoscarmike/cloud-run-clients`
1. browse to `https://localhost:5000`
