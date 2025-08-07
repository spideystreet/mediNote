# Setup Log for mediNote Project

This document chronicles the setup process for the `mediNote` project, detailing various approaches explored and challenges encountered during development, along with their resolutions. It serves as a historical record of architectural decisions and their evolution.

## 1. Initial Project Setup

-   **Repository Initialization:** The project was initialized as a Git repository, and a remote was added to GitHub.
-   **Documentation & Structure:**
    -   `README.md` was created to provide an overview of the project, its objectives, and core technologies.
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

## 4. Airbyte Source/Destination Configuration (Challenges & Solutions)

After successfully deploying Airbyte with `abctl`, we faced challenges configuring Airbyte connectors to interact with our `docker-compose` services.

-   **`FileNotFoundError` with Local File Source:** The Airbyte "File" source connector failed to access `patient_notes.json` from the local filesystem. This is a fundamental limitation of Kubernetes container isolation; containers cannot directly access the host's filesystem.
-   **Networking between `abctl` Kubernetes and Docker Compose:** Attempts to connect Airbyte connectors to our `docker-compose`-managed services (MongoDB, ClickHouse) failed due to network isolation between the `abctl`-managed Kubernetes cluster's network and our `docker-compose` network.
    -   **Resolution:** The `medinote-mongo` and `medinote-clickhouse` containers were explicitly connected to the `kind` Docker network (the network used by `abctl`'s Kubernetes cluster). This allowed the Airbyte connectors to resolve these services by their hostnames.
-   **MongoDB Replica Set Configuration for Airbyte:** The Airbyte MongoDB connector requires a replica set. After ensuring MongoDB was running as a replica set (even a single-node one) and disabling authorization for simplicity, the Airbyte MongoDB source connection was finally successful.

## 5. Data Verification (During Setup)

-   **MongoDB Data Verification:**
    -   Accessed the MongoDB shell: `docker exec -it medinote-mongo mongosh`
    -   Switched to the database: `use medinote_db`
    -   Listed collections: `show collections`
    -   Queried the `patient_notes` collection: `db.patient_notes.find().pretty()`
    -   Confirmed the presence of 3 patient note records.

## Current Project State

This project demonstrates a direct Python-based data pipeline for ingestion and enrichment, leveraging Docker-Compose for core data services (MongoDB, ClickHouse, MinIO). Airbyte was explored during setup but is not part of the final, streamlined pipeline.

## Future Enhancements

-   Implement a more robust orchestration layer (e.g., Apache Airflow) for scheduling and monitoring.
-   Explore advanced dbt transformations for deeper analytical insights.
-   Integrate a UI for data visualization and interaction.
-   Expand AI models for more diverse medical NLP tasks.