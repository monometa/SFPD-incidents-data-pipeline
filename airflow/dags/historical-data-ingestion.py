import os
from datetime import datetime

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.csv as csv
import pyarrow.parquet as pq

from airflow import DAG
from airflow.models import Variable
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryCreateExternalTableOperator,
    BigQueryInsertJobOperator,
)
from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import (
    LocalFilesystemToGCSOperator,
)
from airflow.utils.dates import days_ago
from google.cloud import storage

# import pandas as pd

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME")
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", "police_staging")

DATASET = "historical_data"
OUTPUT_PATH = "raw/"

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}

# TO-DO: put in ./scripts and do the same in modern-data-ing.py

def transform_to_parquet(src_file):

    table = csv.read_csv(src_file)

    pq.write_table(table, "police_data__2003-2017.parquet")


with DAG(
    dag_id="historical-data-ingestion",
    schedule_interval="@once",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=["de_police"],
) as dag:

    download_dataset = BashOperator(
        task_id="download_dataset_task",
        bash_command="curl -sSL 192.168.208.1:8000/police_data__2003-2017.csv > \
            $AIRFLOW_HOME/police_data__2003-2017.csv",
    )

    transform_to_parquet = PythonOperator(
        task_id="format_datetime_pyarrow_task",
        python_callable=transform_to_parquet,
        op_kwargs={
            "src_file": f"{AIRFLOW_HOME}/police_data__2003-2017.csv",
        },
    )

    local_to_gcs = LocalFilesystemToGCSOperator(
        task_id="local_to_gcs_task",
        src="./police_data__2003-2017.parquet",
        dst=OUTPUT_PATH,
        bucket=BUCKET,
    )

    bigquery_external_table_task = BigQueryCreateExternalTableOperator(
        task_id=f"bq_{DATASET}_external_table_task",
        table_resource={
            "tableReference": {
                "projectId": PROJECT_ID,
                "datasetId": BIGQUERY_DATASET,
                "tableId": f"{DATASET}_raw_dataset",
            },
            "externalDataConfiguration": {
                "autodetect": "True",
                "sourceFormat": "PARQUET",
                "sourceUris": [f"gs://{BUCKET}/raw/police_data__2003-2017.parquet"],
                "ignoreUnknownValues": "True",
            },
        },
    )

    # TO-DO: add sensors to check for files existence (for ex. GCSObjectExistenceSensor)
    (
        download_dataset
        >> transform_to_parquet
        >> local_to_gcs
        >> bigquery_external_table_task
    )
