# Zach Chase

# Databricks notebook source

file_master = "dbfs:///FileStore/tables/Master.csv"
file_team = "dbfs:///FileStore/tables/Teams.csv"
file_allStar = "dbfs:///FileStore/tables/AllstarFull.csv"
master_df = spark.read.format("csv").option("header", True).option("inferSchema", True).load(file_master).select("playerID", "nameFirst", "nameLast")
team_df = spark.read.format("csv").option("header", True).option("inferSchema", True).load(file_team).select("teamID", "name").withColumnRenamed("name","team")
allstar_df = spark.read.format("csv").option("header", True).option("inferSchema", True).load(file_allStar).select("playerID", "teamID")

# COMMAND ----------

lab6DF = master_df.alias("m").join(allstar_df.alias("a"), allstar_df['playerID'] == master_df['playerID']).select("m.playerID", "a.teamID", "m.nameFirst", "m.nameLast").distinct()

lab6DF = lab6DF.alias("l").join(team_df.alias("t"), lab6DF['teamID'] == team_df['teamID']).select("l.playerID", "t.team", "l.nameFirst", "l.nameLast").distinct()

lab6DF.write.format("parquet").partitionBy("team").save("lab_6_stats")

# COMMAND ----------

import pyspark.sql.functions as f

file_load = "dbfs:///lab_6_stats"
df = spark.read.format("parquet").option("header", True).option("inferSchema", True).load(file_load)
df.select("nameFirst", "nameLast").filter(f.col("team") == "Colorado Rockies").show(50)
df.select("nameFirst", "nameLast").filter(f.col("team") == "Colorado Rockies").count()

# COMMAND ----------


