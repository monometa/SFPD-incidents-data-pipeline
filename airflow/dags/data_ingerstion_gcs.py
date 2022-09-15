import os
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator,  BigQueryInsertJobOperator

from datetime import datetime
from google.cloud import storage

import pyarrow.csv as pv
import pyarrow.compute as pc

import pandas as pd

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME")
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", 'police_data')
DATASET = "sfpd_police_data"
# FILENAME = 'subreddit_posts_data_{{ execution_date.strftime(\'%Y%m%d\') }}.csv'
OUTPUT_PATH = "raw/" 
default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}

def transform_datetime(src_file):
    df = pd.read_csv(src_file)
    # _format = "%Y/%m/%d %H:%M:%S %p"
    df["Incident Datetime"] = pd.to_datetime(df["Incident Datetime"])
    df["Report Datetime"] = pd.to_datetime(df["Report Datetime"])
    df.to_csv("police_modified.csv", index=False)


with DAG(
    dag_id="data_ingestion_to_gcs",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['de_police'],
    # template_searchpath="/opt/airflow/scripts"
) as dag:

    download_dataset = BashOperator(
        task_id="download_dataset_task",
        # bash_command="wget -O police_data-p-2018-2022.csv https://data.sfgov.org/api/views/wg3w-h783/rows.csv", # TO-DO start load_data script
        bash_command="curl -sSL 192.168.192.1:8000/sfpd_data.csv > $AIRFLOW_HOME/police_data_f-2018-2022.csv", # TO-DO start load_data script
    )

    format_datetime = PythonOperator(
        task_id="format_datetime_task",
        python_callable=transform_datetime,
        op_kwargs={
            "src_file": f"{AIRFLOW_HOME}/police_data_f-2018-2022.csv",
        },
    ) 

    split_dataset_file = BashOperator(
        task_id="split_dataset_file_task",
        bash_command="scripts/split_data_by-years.sh", # TO-DO start split_data... script
    )

    local_to_gcs = LocalFilesystemToGCSOperator(
        task_id="local_to_gcs_task",
        src="./police_data-*.csv",
        dst=OUTPUT_PATH,
        bucket=BUCKET,
    )

    # move_files_gcs_task = GCSToGCSOperator(
    #     task_id=f'move_subreddit_data_files_task',
    #     source_bucket=BUCKET,
    #     source_object=f'raw/*.csv',
    #     destination_bucket=BUCKET,
    #     destination_object=f'reddit/raw',
    #     move_object=True
    # )

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
                "sourceFormat": "CSV",
                "sourceUris": [f"gs://{BUCKET}/raw/*"],
                "ignoreUnknownValues": "True",
            },
        },
    )

    # CREATE_BQ_TBL_QUERY = (
    #     f"CREATE OR REPLACE TABLE {BIGQUERY_DATASET}.{DATASET} \
    #     PARTITION BY DATE(tpep_pickup_datetime) \
    #     AS \
    #     SELECT * FROM {BIGQUERY_DATASET}.{DATASET}_external_table;"
    # )

    # # Create a partitioned table from external table
    # bq_create_partitioned_table_job = BigQueryInsertJobOperator(
    #     task_id=f"bq_create_{DATASET}_partitioned_table_task",
    #     configuration={
    #         "query": {
    #             "query": CREATE_BQ_TBL_QUERY,
    #             "useLegacySql": False,
    #         }
    #     }
    # )


    download_dataset >> format_datetime >> split_dataset_file  >> local_to_gcs >> bigquery_external_table_task
    # move_files... >> bq_create_partitioned_table_job
