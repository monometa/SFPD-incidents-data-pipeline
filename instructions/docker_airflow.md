## Set up data ingestion with Airflow

1. Go to the `airflow` folder.
1. Run the following command and write down the output:
    ```sh
    echo -e "AIRFLOW_UID=$(id -u)"
    ```
1. Edit the `.env` file with the following data:
```sh
GCP_PROJECT_ID=<your-gcp-project-id>
GCP_GCS_BUCKET=<your-gcp-bucket-name>

AIRFLOW_UID=<your-airflow-uid>
```
   Change the value of `AIRFLOW_UID`, `GCP_PROJECT_ID` and `GCP_GCS_BUCKET` for the value of the previous command.
1. Build the custom Airflow Docker image:
    ```sh
    docker-compose build
    ```
1. Initialize the Airflow configs:
    ```sh
    docker-compose up airflow-init
    ```
1. Run Airflow
    ```sh
    docker-compose up -d 
    
You may now access the Airflow GUI by browsing to `localhost:8080`. Username and password are both `airflow` .
>***IMPORTANT***: this is ***NOT*** a production-ready setup! The username and password for Airflow have not been modified in any way; you can find them by searching for `_AIRFLOW_WWW_USER_USERNAME` and `_AIRFLOW_WWW_USER_PASSWORD` inside the `docker-compose.yaml` file.
- If you can't connect to Airflow you need to forward 8080 port to your local machine. You can this on VSCode following these steps:
   - Open terminal
   - Click on Ports
   - Select the option Forward a port and select port 8080
   
 ### Perform the data ingestion

If you performed all the steps of the previous section, you should now have a web browser with the Airflow dashboard.

![alt t](https://i.imgur.com/Qtnb53c.png)

After successfully running the Airflow workflow you should get the following folders and respective parquet files created on GCP bucket:

![alt t](https://i.imgur.com/wBp8zMo.png)


After the data ingestion, you may shut down Airflow by running `docker-compose down`, or you may keep Airflow running if you want to update the dataset every month.


---

[Previous Step](infrastructure.md) | [Next Step](dbt.md)

or

[Back to main README](../README.md)
