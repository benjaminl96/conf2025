# conf2025 Demo: Splunk Ecommerce Transactions Summary Index and KV Store performance

This demo provides visualizations to compare performance between searching raw event data compared to using a summary index and KV Store lookups.
It simulates customer purchase and order fulfillment logs for Splunk using a Python script and configuration files. You can run the demo using Docker Compose or a standalone Docker container.

## Prerequisites
- Docker and Docker Compose installed on your machine

## Files
- `app/bin/make_logs.py`: Python script to generate fake ecommerce transaction logs
- `app/default/inputs.conf`: Splunk configuration for ingesting logs
- `app/bin/customers.json`: Persistent customer data
- `demo.yaml`: Docker Compose configuration for the demo

## Run the Demo with Docker Compose
The recommended way to run the demo is with Docker Compose:

```sh
docker-compose -f demo.yaml up -d
```

This will start all services defined in `demo.yaml` in detached mode. The log generator will run automatically, and you can configure Splunk ingestion as needed.

To stop the demo:
```sh
docker-compose -f demo.yaml down
```

## Customization
- Edit `app/bin/make_logs.py` to change log generation logic or product list.
- Update `app/default/inputs.conf` for Splunk source/index settings.
- Modify `demo.yaml` to adjust service configuration, volumes, or environment variables.

## Notes
- The `customers.json` file persists customer state between runs.

