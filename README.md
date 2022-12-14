# San Francisco Police Department incidents

**Table of Contents**

* [Project Overview](#project-overview)
* [Dataset](#dataset)
* [Technologies](#technologies)
* [Instruction on Running the Project](#instruction-on-running-the-project)

## Project Overview

![Project Overview](https://user-images.githubusercontent.com/107945681/192289946-803d3787-5a84-45d9-8288-bd7e4b479e84.png)

In this project, we first extract by downloading CSVs using SODA API. We then consume and put them into a data lake (Google Cloud Storage). After that we schedule a data pipeline (Airflow) to run monthly to load to a data warehouse (Google BigQuery). Later on, we transform the data in the warehouse using dbt. Finally, once the data is cleaned and transformed, we can monitor and analyze the data on a dashboard (Tableau).

The visualization results are two dashboards. On the first of them, you can see the ratio of the number of crimes to the previous year with the possibility of choosing a district. The second is a map crime with additional information regarding the dynamics of the most committed crimes.

## Dataset

[Police Department Incident Reports Historical (2003 - 2017)](https://data.sfgov.org/Public-Safety/Police-Department-Incident-Reports-Historical-2003/tmnf-yvry)

[Police Department Incident Reports (2018 to Present)](https://data.sfgov.org/Public-Safety/Police-Department-Incident-Reports-2018-to-Present/wg3w-h783)

## Technologies

* [Apache Airflow](https://airflow.apache.org/) for orchestrating workflow
* [Google Cloud Storage](https://cloud.google.com/storage/docs) for data lake storage
* [dbt](https://www.getdbt.com/) for data transformation
* [Google BigQuery](https://cloud.google.com/bigquery) for data warehousing and analysis
* [Tableau](https://www.tableau.com/why-tableau/what-is-tableau) for visualization
* [Terraform](https://www.terraform.io/) as an Infrastructure-as-Code (IaC) tool
* [Docker](https://www.docker.com/) to proceed to the containerization of other technologies

## Vizzes 

<div class='tableauPlaceholder' id='viz1671539366046' style='position: relative'><noscript><a href='#'><img alt='SFPD Police data ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;SF&#47;SFPDCrimedashboard&#47;SFPDPolicedata&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='SFPDCrimedashboard&#47;SFPDPolicedata' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;SF&#47;SFPDCrimedashboard&#47;SFPDPolicedata&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /></object></div>

---

![image](https://user-images.githubusercontent.com/107945681/208668453-b0abd7c3-f625-45b9-b4fd-fce0ab00e63b.png)

## Instruction on Running the Project

Follow below steps to set up the project. I've tried to explain steps where I can. Feel free to make improvements/changes.

> **NOTE**: This was developed using a Google VM instance. If you're on Windows or Linux, you may need to amend certain components if issues are encountered.

As Google offers a free trial for 3 months, this shouldn't cost you anything with proper settings (which will be mentioned later). However, please check [Google Free Trial and Free Tier](https://cloud.google.com/free) limits, as this may change.

1. [Prerequisites](instructions/prerequisites.md)
2. [Google Cloud setup](instructions/google-cloud.md)
3. [Infrastructure & Terraform](instructions/infrastructure.md)
4. [Airflow](instructions/airflow.md) 
5. [dbt](instructions/dbt.md)
6. [Dashboard](instructions/visualisation.md)
7. [Improvements](instructions/improvements.md)
