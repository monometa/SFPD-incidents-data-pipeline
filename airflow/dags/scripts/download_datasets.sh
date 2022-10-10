#!/bin/sh

# TO-DO: create var and give to curl oper. for downloading diff. datasets 
curl -sSL 192.168.208.1:8000/police_data__2018-2022.csv > $AIRFLOW_HOME/police_data__2018-2022.csv