# Databricks notebook source
# MAGIC %pip install dbt-sl-sdk[sync]

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

from dbtsl import SemanticLayerClient

client = SemanticLayerClient(
    environment_id=xxx,
    auth_token="xxx",
    host="semantic-layer.cloud.getdbt.com",
)

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
        spark_df.write.format("delta").saveAsTable("ka_abe.sample.checking_table")
main()
