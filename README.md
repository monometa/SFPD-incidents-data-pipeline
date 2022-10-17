# San Francisco Police Department incidents

![image](https://user-images.githubusercontent.com/107945681/192318893-a012570b-b172-4aa6-878c-8df37c017b82.png)

**Table of Contents**

* [Project Overview](#project-overview)
* [Dataset](#dataset)
* [Technologies](#technologies)
* [Files and What They Do](#files-and-what-they-do)
* [Improvements to do](#improvements-to-do)

## Project Overview

![Project Overview](https://user-images.githubusercontent.com/107945681/192289946-803d3787-5a84-45d9-8288-bd7e4b479e84.png)

In this project, we first extract by downloading CSVs using SODA API. We then consume and put them into a data lake (Google Cloud Storage). After that we schedule a data pipeline (Airflow) to run montly to load to a data warehouse (Google BigQuery). Later on, we transform the data in the warehouse using dbt. Finally, once the data is cleaned and transformed, we can monitor and analyze the data on a dashboard (Tableau).

## Dataset

[SFPD reports part #1 (2003-2017)](https://data.sfgov.org/Public-Safety/Police-Department-Incident-Reports-Historical-2003/tmnf-yvry)

[SFPD reports part #2 (2018-Present)](https://data.sfgov.org/Public-Safety/Police-Department-Incident-Reports-2018-to-Present/wg3w-h783)

## Technologies

* [Apache Airflow](https://airflow.apache.org/) for orchestrating workflow
* [Google Cloud Storage](https://cloud.google.com/storage/docs) for data lake storage
* [dbt](https://www.getdbt.com/) for data transformation
* [Google BigQuery](https://cloud.google.com/bigquery) for data warehousing and analysis
* [Tableau](https://www.tableau.com/why-tableau/what-is-tableau) for visualization
* [Terraform](https://www.terraform.io/) as a Infrastructure-as-Code (IaC) tool
* [Docker](https://www.docker.com/) to proceed to the containerization of other technologies

## Instruction on Running the Project


## Improvements to do

 - https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/week_7_project#going-the-extra-mile
