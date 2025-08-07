# Gemini Notes

This file contains notes and context for the Gemini AI assistant to help with the development of the mediNote project.

## Project Overview

**mediNote** is a data engineering project that demonstrates a full-stack workflow for processing and analyzing unstructured healthcare data. The key objectives are to ingest patient notes with Airbyte, enrich them with AI models (NER and summarization), store the data in appropriate databases (MongoDB for unstructured, ClickHouse for structured), and model the final data using dbt.

## Core Technologies

*   **Data Ingestion:** Airbyte
*   **AI Integration:** Hugging Face
*   **Data Storage:** MongoDB, ClickHouse
*   **Data Transformation:** dbt, SQL
*   **Language:** Python

## Development Plan

1.  **Environment Setup:** Create a `docker-compose.yml` for Airbyte, MongoDB, and ClickHouse.
2.  **Ingestion:** Configure an Airbyte pipeline to move data from a source to MongoDB.
3.  **Enrichment:** Develop a Python service to read from MongoDB, apply Hugging Face models, and write to ClickHouse.
4.  **Modeling:** Build dbt models to transform the data in ClickHouse.
5.  **Orchestration:** Create a main pipeline script to run the entire workflow.

## Documentation Resources

*   **Airbyte:** [Docs](https://docs.airbyte.com/), [GitHub](https://github.com/airbytehq)
*   **dbt:** [Docs](https://docs.getdbt.com/), [GitHub](https://github.com/dbt-labs)
*   **ClickHouse:** [Docs](https://clickhouse.com/docs), [GitHub](https://github.com/ClickHouse/ClickHouse)
*   **Hugging Face:** [Docs](https://huggingface.co/docs), [GitHub](https://github.com/huggingface)
*   **MongoDB:** [Docs](https://www.mongodb.com/docs/)
*   **Docker:** [Docs](https://docs.docker.com/)

## Development Notes

*   The user wants to use a full Airbyte instance, not a simulation.
*   The user has provided documentation links for the core technologies.
*   The user has granted autonomy for commit messages.
