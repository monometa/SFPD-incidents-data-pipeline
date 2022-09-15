#!/bin/sh
for (( i=2018; i < 2023; i++ )); do
    # TO-DO set relative path to main-data file for !airflow
    csvgrep \
    -c "Incident Year" \
    -m $i $AIRFLOW_HOME/police_modified.csv > \
        $AIRFLOW_HOME/police_data-$i.csv;
done
