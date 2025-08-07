# mediNote

<pre>
  __  __          _   _       _
 |  \/  |        | \ | |     | |
 | \  / | ___  __|  \| | ___ | |_
 | |\/| |/ _ \/ _` | . ` |/ _ \| __|
 | |  | |  __/ (_| | |\  | (_) | |_
 |_|  |_|\___|\__,_|_| \_|\___/ \__|
</pre>

A modern data engineering project demonstrating a full-stack workflow for processing and analyzing unstructured healthcare data.

## Key Objectives

-   **Ingest:** Process simulated unstructured patient notes (free-text).
-   **Enrich:** Use Hugging Face AI models for Named Entity Recognition (NER) and summarization.
-   **Store:** Keep original data in MongoDB (NoSQL) and store structured, enriched data in ClickHouse (analytical).
-   **Model:** Use dbt (Data Build Tool) for data modeling and transformation.

## Core Technologies

-   **Data Ingestion:** Airbyte
-   **AI Integration:** Hugging Face
-   **Data Storage:**
    -   MongoDB (Unstructured Data)
    -   ClickHouse (Structured/Analytical Data)
-   **Data Transformation:** dbt, SQL
-   **Orchestration:** Python
-   **Language:** Python

## Project Workflow

```
[Local Text File] -> [Airbyte] -> [MongoDB]
                              |
                              v
                [Python Enrichment Service]
                  (Hugging Face NER & Sum.)
                              |
                              v
                         [ClickHouse]
                              |
                              v
                            [dbt]
                              |
                              v
                  [Analytics / Dashboards]
```

## Getting Started

### Prerequisites

-   Python 3.9+
-   Docker
-   dbt Core

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/spideystreet/mediNote.git
    cd mediNote
    ```

2.  **Set up Python environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Start services (MongoDB & ClickHouse):**
    ```bash
    # (Instructions to be added for docker-compose.yml)
    docker-compose up -d
    ```

4.  **Configure dbt:**
    -   Set up your `profiles.yml` to connect to ClickHouse.

## Usage

1.  **Run the ingestion script:**
    ```bash
    # (Command to run the ingestion script)
    ```

2.  **Run dbt models:**
    ```bash
    dbt run
    ```

---
*This project is for training and demonstration purposes.*
