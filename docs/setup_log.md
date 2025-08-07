# Setup Log for mediNote Project

This document chronicles the setup process for the `mediNote` project, detailing the steps taken and the challenges encountered, along with their resolutions.

## 1. Initial Project Setup

-   **Repository Initialization:** The project was initialized as a Git repository, and a remote was added to GitHub.
-   **Documentation & Structure:**
    -   `README.md` was created to provide an overview of the project, its objectives, and core technologies.
    -   `GEMINI.md` was created to serve as a log of interactions and decisions made with the Gemini AI assistant.
    -   Initial `requirements.txt` was created, and a `generate_fake_data.py` script was added to create sample patient notes.
    -   A `.gitignore` file was added to exclude sensitive files like `.env` and virtual environments.
-   **Version Control:** All initial setup files were committed to a `dev` branch and pushed to the remote repository.

## 2. Docker Compose Setup (Initial Attempts & Challenges)

Our initial approach involved a custom `docker-compose.yml` to manage MongoDB, ClickHouse, and a minimal Airbyte setup. This led to several issues:

-   **Port Conflicts:** Initial attempts resulted in port conflicts (e.g., port 8000 for Airbyte UI, port 9000 for ClickHouse and MinIO). These were resolved by adjusting port mappings in `docker-compose.yml`.
-   **Airbyte Temporal Issues:** The `airbyte-temporal` service, a critical component for Airbyte's orchestration, repeatedly failed to start due to:
    -   Missing `DATABASE_URL` and `airbyte.workspace.root` environment variables.
    -   Incorrect `POSTGRES_SEEDS` configuration.
    -   Misconfigured `command` for the `temporalio/auto-setup` image, leading to invalid database connection strings.
-   **MongoDB Replica Set & Authorization:**
    -   The Airbyte MongoDB connector requires a replica set. Our initial MongoDB setup was standalone.
    -   Attempting to configure MongoDB as a replica set introduced issues with authorization, as a `keyFile` is required for replica sets with authorization enabled. For a local development environment, authorization was disabled to simplify the setup.

## 3. `abctl` Installation and Airbyte Deployment

Due to persistent issues with the custom `docker-compose.yml` for Airbyte, we shifted to using `abctl` (Airbyte Control Tool), the recommended method for local Airbyte deployments.

-   **`abctl` Installation:** `abctl` was successfully installed on the local machine using the `curl` installation script.
-   **Airbyte Deployment with `abctl`:** The `abctl local install` command was executed. This command sets up a Kubernetes cluster (using `kind`) inside Docker and deploys Airbyte onto it using Helm charts.
    -   **Challenge:** Initial `abctl local install` attempts failed with `ImagePullBackOff` errors, indicating issues with the Kubernetes cluster pulling Docker images. This was primarily attributed to resource limitations in Docker Desktop.
    -   **Resolution:** Increasing allocated CPU and RAM for Docker Desktop resolved the `ImagePullBackOff` errors, and `abctl local install` completed successfully. The Airbyte UI became accessible at `http://localhost:8000`.

## 4. Airbyte Source Configuration (Challenges & Solutions)

After successfully deploying Airbyte with `abctl`, we faced challenges configuring the Airbyte source connector.

-   **`FileNotFoundError` with Local File Source:** The Airbyte "File" source connector failed to access `patient_notes.json` from the local filesystem. This is a fundamental limitation of Kubernetes container isolation; containers cannot directly access the host's filesystem.
-   **Networking between `abctl` Kubernetes and Docker Compose:** Attempts to connect the Airbyte MongoDB source to our `docker-compose`-managed MongoDB container failed due to network isolation between the `abctl`-managed Kubernetes cluster's network and our `docker-compose` network.
    -   **Resolution:** The `medinote-mongo` container was explicitly connected to the `kind` Docker network (the network used by `abctl`'s Kubernetes cluster). This allowed the Airbyte connector to resolve `medinote-mongo` by its service name.
-   **MongoDB Replica Set Configuration for Airbyte:** The Airbyte MongoDB connector requires a replica set. After ensuring MongoDB was running as a replica set (even a single-node one) and disabling authorization for simplicity, the Airbyte MongoDB source connection was finally successful.

    -   **ClickHouse Destination Setup:**
        -   **Challenge:** Initial attempts to connect to `medinote-clickhouse` resulted in an "Unknown host" error, similar to MongoDB, due to network isolation.
        -   **Resolution:** The `medinote-clickhouse` container was explicitly connected to the `kind` Docker network, allowing the Airbyte connector to resolve its hostname. The Airbyte ClickHouse destination was successfully configured using `medinote-clickhouse` as the host and `8123` as the port.

## Current Status

All core services (MongoDB, ClickHouse, MinIO) are running via `docker-compose`. The Airbyte platform is running via `abctl`. The Airbyte MongoDB source and ClickHouse destination are successfully connected.

## Next Steps

-   Create the Airbyte connection to sync data from MongoDB to ClickHouse.
-   Develop the Python enrichment service to process data from MongoDB and prepare it for ClickHouse.
-   Set up dbt for data modeling in ClickHouse.
-   Create a main orchestration script to manage the entire pipeline.
