# Databricks notebook source
# MAGIC %pip install dbt-sl-sdk[sync]
# MAGIC %pip install --upgrade dbt-sl-sdk

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

import os
os.environ["EVIROMENT_ID"] = dbutils.secrets.get(scope="dbt_demo", key = "eviroment_id")
os.environ["SERVICE_TOKEN"] = dbutils.secrets.get(scope="dbt_demo", key = "service_token")
os.environ["SEMANTIC_LAYER_HOST"] = dbutils.secrets.get(scope="dbt_demo", key = "host_name")

# COMMAND ----------

from dbtsl import SemanticLayerClient

client = SemanticLayerClient(
    environment_id=os.getenv("EVIROMENT_ID"),
    auth_token=os.getenv("SERVICE_TOKEN"),
    host=os.getenv("SEMANTIC_LAYER_HOST")
)
# client.start_session()  # セッションを開始

# COMMAND ----------

from pyspark.sql import SparkSession

def main():
    spark = SparkSession.builder.appName("CreateView").getOrCreate()

    with client.session():
        arrow_table = client.query(
            metrics=["order_total","max_order_amount","min_order_amount","food_order_amount","food_order_pct"],
            group_by=["metric_time__day"],
            filters=[{"field": "metric_time__day", "operator": ">=", "value": "2016-09-01"},{"field": "metric_time__day", "operator": "<=", "value": "2016-09-22"}]
        )

        pandas_df = arrow_table.to_pandas()
        print(pandas_df)

        spark_df = spark.createDataFrame(pandas_df)
        spark_df.write.format("delta").mode("overwrite").saveAsTable("ka_abe.sample.checking_table")
main()
