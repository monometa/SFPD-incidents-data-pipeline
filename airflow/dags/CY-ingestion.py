import os
from datetime import datetime
from numpy import column_stack

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

# import pandas as pd

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME")
BIGQUERY_DATASET = "police_staging"

DATASET = "police_reports_CY"


def set_url(limit, year):
    URL_DOMAIN = "https://data.sfgov.org/resource/wg3w-h783.csv"

    # TO-DO: set url by func generate_url without that loooooooooooooooooooong string

    URL_PARAMS = f"?%24limit={limit}&%24select=%2A&%24where=incident_year%3A%3Anumber+%3D+{year}+and+date_extract_m%28incident_datetime%29+%3D+{{{{ execution_date.strftime('%-m') }}}}"
    url_template = URL_DOMAIN + URL_PARAMS
    return url_template


URL_TEMPLATE = set_url(1000000, 2022)

FILENAME_CSV_TEMPLATE = "2022_{{ execution_date.strftime('%-m') }}_police_reports.csv"
FILENAME_PARQUET_TEMPLATE = (
    "2022_{{ execution_date.strftime('%-m') }}_police_reports.parquet"
)

SAVE_PATH_TEMPLATE = f"$AIRFLOW_HOME/{FILENAME_CSV_TEMPLATE}"
OUTPUT_PATH = "raw/"

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
}


def conf_column_types():
    column_types = {"cnn": pa.float64()}
    return column_types


def transform_to_parquet(src_file, output_file):

    column_types = conf_column_types()
    convert_options = csv.ConvertOptions(column_types=column_types)
    table = csv.read_csv(src_file, convert_options=convert_options)

    pq.write_table(table, output_file)


def donwload_upload_dag(
    dag,
    URL_TEMPLATE,
    SAVE_PATH_TEMPLATE,
):
    with dag:
        download_dataset = BashOperator(
            task_id="download_dataset_task",
            bash_command=rf"curl -sSLf '{URL_TEMPLATE}' > {SAVE_PATH_TEMPLATE}",
        )

        transform_2_parquet = PythonOperator(
            task_id="format_datetime_pyarrow_task",
            python_callable=transform_to_parquet,
            op_kwargs={
                "src_file": f"{AIRFLOW_HOME}/{FILENAME_CSV_TEMPLATE}",
                "output_file": f"{AIRFLOW_HOME}/{FILENAME_PARQUET_TEMPLATE}",
            },
        )

        local_to_gcs = LocalFilesystemToGCSOperator(
            task_id="local_to_gcs_task",
            src=f"./{FILENAME_PARQUET_TEMPLATE}",
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
                    "sourceUris": [f"gs://{BUCKET}/raw/2022*_reports.parquet"],
                    "ignoreUnknownValues": "True",
                },
            },
        )

        (
            download_dataset
            >> transform_2_parquet
            >> local_to_gcs
            >> bigquery_external_table
        )


police_reports_monthly = DAG(
    dag_id="CY_police_reports_by_months",
    schedule_interval="@monthly",
    start_date=datetime(2022, 1, 1),
    end_date=datetime(2022, 12, 1),
    default_args=default_args,
    catchup=True,
    max_active_runs=3,
    tags=["police_reports"],
)

donwload_upload_dag(
    dag=police_reports_monthly,
    URL_TEMPLATE=URL_TEMPLATE,
    SAVE_PATH_TEMPLATE=SAVE_PATH_TEMPLATE,
)
