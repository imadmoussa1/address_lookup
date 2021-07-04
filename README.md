# address_lookup

## installation
Add the csv of data files to `address_lookup/backend/app/app/address_data`

```
mkdir data
sudo cmhod /data
docker build -f backend/backend_base.dockerfile -t address:latest backend
docker-compose -f "docker-compose.yml" up -d --build
```

## Project details
I am using fastAPI template with celery.

The ETL pipeline celery Task in `address_lookup/backend/app/app/worker.py`, this pipeline can start Automatically (Scheduled Task) or using the API.

This pipeline save data to MongoDB and elasticsearch, (details of mongodb and elastic session are under `address_lookup/backend/app/app/db`)

The search query for elastic to find the address we looking for, can be called using the API in
`address_lookup/backend/app/app/api/api_v1/endpoints\utils.py`

## User for login for testing
user=imad@admin.com
password=admin123

## Run the project
Open the url `http://localhost:8080/docs` after that:
1) Authorize the app using the username and password

2) Execute the `/api/v1/utils/address/etl` to run the pipeline.

3) Search for address using `/api/v1/utils/address/`