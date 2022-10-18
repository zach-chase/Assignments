# Databricks notebook source

# Zach Chase

sc = spark.sparkContext

from pyspark.sql import Row
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType
from pyspark.sql.functions import desc

file = "FileStore/tables/lab5/Master.csv"
RDD = sc.textFile(file).map(lambda l: l.split(","))
header = RDD.take(1)
RDD = RDD.filter(lambda x: x not in header)
RDD = RDD.filter(lambda l: l[17] != "")




RowsRDD = RDD.map(lambda l: Row(ID=l[0], Country=l[4], State=l[5], Height=int(l[17])))

schema = StructType([
    StructField("ID", StringType(), True),
    StructField("Country", StringType(), True),
    StructField("State", StringType(), True),
    StructField("Height", IntegerType(), False)])

masterDF = spark.createDataFrame(RowsRDD, schema = schema)

#masterDF.printSchema()
#masterDF.show()

# COMMAND ----------

masterDF.createOrReplaceTempView("master")

spark.sql("SELECT COUNT(State) FROM master WHERE State == 'CO'").show()

# COMMAND ----------

len(masterDF[masterDF['State'] == 'CO'].collect())

# COMMAND ----------

result = spark.sql("SELECT AVG(height), Country FROM master GROUP BY Country SORT BY AVG(height) DESC")
result.show(result.count())

# COMMAND ----------

results = masterDF.groupby(['Country']).mean("height").sort(desc("avg(height)"))
results.show(results.count())

# COMMAND ----------


