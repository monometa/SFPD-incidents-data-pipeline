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
from scripts import cast_column_datetime_2_timestamp

from google.cloud import storage

# import pandas as pd

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME")
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", "police_staging")

DATASET = "modern_data"
OUTPUT_PATH = "raw/"
default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}

# TO-DO: split transform_to_parquet func and put in a ./scripts

def transform_to_parquet(src_file):

    table = csv.read_csv(src_file)
    table = cast_column_datetime_2_timestamp(table, "Incident Datetime", 0)
    table = cast_column_datetime_2_timestamp(table, "Report Datetime", 5)

    pq.write_table(table, "police_data__2018-2022.parquet")


with DAG(
    dag_id="modern-data-ingestion",
    schedule_interval="@monthly",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=["de_police"],
) as dag:

    download_dataset = BashOperator(
        task_id="download_dataset_task",
        # TO-DO: download up-to-date data from data.sfgov.org via SODA API
        bash_command="scripts/download_datasets.sh",
    )

    transform_to_parquet = PythonOperator(
        task_id="format_datetime_pyarrow_task",
        python_callable=transform_to_parquet,
        op_kwargs={
            "src_file": f"{AIRFLOW_HOME}/police_data__2018-2022.csv",
        },
    )

    local_to_gcs = LocalFilesystemToGCSOperator(
        task_id="local_to_gcs_task",
        src="./police_data__2018-2022.parquet",
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
                "sourceUris": [f"gs://{BUCKET}/raw/police_data__2018-2022.parquet"],
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
