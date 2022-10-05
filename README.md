# Humanitec Custom Resource Driver - Reference implementation

This is a **reference** implementation of a custom *Driver* for Humanitec.
It operates similarly to the Built-in AWS driver, deploying new S3 buckets on-demand.

To test it out, you'll need to deploy it as a public facing webserver, and then register it via the Humanitec API.
To learn more about registering drivers checkout the [documentation](https://docs.humanitec.com/integrations/create-own-resource-driver).


## Endpoints

### Public

| Method   | Path Template | Description                |
|----------|---------------|----------------------------|
| `PUT`    | `/s3/{id}`    | Upsert a bucket on AWS S3. |
| `DELETE` | `/s3/{id}`    | Delete a bucket on AWS S3. |


### Service

| Method | Path Template     | Description                         |
|--------|-------------------|-------------------------------------|
| `GET`  | `/docs/spec.json` | OpenAPI v3 specification.           |
| `GET`  | `/alive`          | Should be used for liveness probe.  |
| `GET`  | `/health`         | Should be used for readiness probe. |


## Installing the requirements
```bash
pip3 install poetry
poetry install
```

## Running the server

```bash
poetry run uvicorn main:app --host 0.0.0.0 --port 8080
```

