import os
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator,  \
    BigQueryInsertJobOperator

from datetime import datetime
from google.cloud import storage

import pyarrow as pa
import pyarrow.csv as csv
import pyarrow.parquet as pq
import pyarrow.compute as pc

# import pandas as pd

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME")
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", 'police_staging')

DATASET = "sfpd_data_2018-to-present"
OUTPUT_PATH = "raw/"
default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}


def cast_datetime_to_timestamp(table, column_name, column_pos):
    new_datetime = pc.strptime(table.column(column_name), format='%Y/%m/%d %H:%M:%S %p', unit='s')
    table = table.set_column(
        column_pos,
        column_name,
        new_datetime
    )
    return table


def transform_to_parquet(src_file):

    table = csv.read_csv(src_file)
    table = cast_datetime_to_timestamp(table, "Incident Datetime", 0)
    table = cast_datetime_to_timestamp(table, "Report Datetime", 5)

    pq.write_table(table, 'police_data__2018-2022.parquet')


with DAG(
    dag_id="modern-data-ingestion",
    schedule_interval="@monthly",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['de_police'],
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
                "tableId": f"{DATASET}_external_table",
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
    download_dataset >> transform_to_parquet >> local_to_gcs >> bigquery_external_table_task