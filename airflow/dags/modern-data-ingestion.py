import os
from datetime import datetime

import pyarrow as pa
import pyarrow.csv as csv
import pyarrow.parquet as pq
import pyarrow.compute as pc

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import (
    LocalFilesystemToGCSOperator,
)
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryCreateExternalTableOperator,
    BigQueryInsertJobOperator,
)

from google.cloud import storage

from collections import namedtuple
from urllib.parse import urljoin, urlencode, urlparse, urlunparse

# import pandas as pd

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME")
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", "police_staging")

DATASET = "modern_police_reports"
OUTPUT_PATH = "raw/"

MODERN_FILENAME_CSV = "2018_2021_police_reports.csv"
MODERN_FILENAME_PARQUET = "2018_2021_police_reports.parquet"

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}


def generate_url(start_year, end_year, limit, ti):

    Components = namedtuple(
        typename="Components",
        field_names=["scheme", "netloc", "url", "path", "query", "fragment"],
    )

    query_params = {
        "$limit": limit,
        "$select": "*",
        "$where": f"incident_year::number between {start_year} and {end_year}",
    }

    url = urlunparse(
        Components(
            scheme="https",
            netloc="data.sfgov.org",
            query=urlencode(query_params),
            path="",
            url="resource/wg3w-h783.csv",
            fragment="",
        )
    )

    ti.xcom_push(key="url_dset", value=url)


def transform_to_parquet(src_file, output_file):

    table = csv.read_csv(src_file)

    pq.write_table(table, output_file)


with DAG(
    dag_id="modern-data-ingestion",
    schedule_interval="@once",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=["police_reports"],
) as dag:

    get_url = PythonOperator(
        task_id="generate_url_task",
        python_callable=generate_url,
        op_kwargs={
            "limit": 100,
            "start_year": "2018",
            "end_year": "2021",
        },
    )

    download_dataset = BashOperator(
        task_id="download_dataset_task",
        bash_command=rf"curl -sSL '{{{{ti.xcom_pull(key='url_dset', task_ids='generate_url_task')}}}}' > $AIRFLOW_HOME/{MODERN_FILENAME_CSV}",
    )

    transform_2_parquet = PythonOperator(
        task_id="format_datetime_pyarrow_task",
        python_callable=transform_to_parquet,
        op_kwargs={
            "src_file": f"{AIRFLOW_HOME}/{MODERN_FILENAME_CSV}",
            "output_file": f"{AIRFLOW_HOME}/{MODERN_FILENAME_PARQUET}",
        },
    )

    local_to_gcs = LocalFilesystemToGCSOperator(
        task_id="local_to_gcs_task",
        src=f"./{MODERN_FILENAME_PARQUET}",
        dst=OUTPUT_PATH,
        bucket=BUCKET,
    )

    bigquery_external_table = BigQueryCreateExternalTableOperator(
        task_id=f"bq_{DATASET}_external_table_task",
        table_resource={
            "tableReference": {
                "projectId": PROJECT_ID,
                "datasetId": BIGQUERY_DATASET,
                "tableId": f"raw_{DATASET}",
            },
            "externalDataConfiguration": {
                "autodetect": "True",
                "sourceFormat": "PARQUET",
                "sourceUris": [f"gs://{BUCKET}/{OUTPUT_PATH}{MODERN_FILENAME_PARQUET}"],
                "ignoreUnknownValues": "True",
            },
        },
    )

    # TO-DO: add sensors to check for files existence (for ex. GCSObjectExistenceSensor)

    (
        get_url
        >> download_dataset
        >> transform_2_parquet
        >> local_to_gcs
        >> bigquery_external_table
    )
