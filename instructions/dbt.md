## dbt configuation

You can choose how to use DBT, using dbt Cloud or dbt Core. [Fast overview presented in this manual](https://docs.getdbt.com/docs/get-started/getting-started/overview)

In case of using dbt Cloud you should:

- Create a new project, choose BigQuery as a database. For exporting the credentials, export google_credentials.json file.
-  Open the project folder in the dbt cloud dev environment 
> Note: it is important to choose the same location in dbt and BigQuery. Otherwise, dbt will not find the location of BigQuery.
- Detailed instructions as an example can be found [here](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_4_analytics_engineering/dbt_cloud_setup.md)
- Run `dbt build` for creating development database tables  
 
 You shuold get a following database:
 
 ![alt](https://i.imgur.com/pwNehNM.png)

- Create production enviroment with `Deployment` type and run following command:


`dbt run`

`dbt test`

`dbt docs generate`


- In filed Triggers activate **Run on schedule** 
- Set Custom Cron Schedule ` 0 5 2 * * `

As a result will be created a database with production tables for use in visualization

![prod table](https://i.imgur.com/zL7pTgQ.png)

---

[Previous Step](airflow.md) | [Next Step](visualisation.md)

or

[Back to main README](../README.md)
