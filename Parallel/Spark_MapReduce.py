# Databricks notebook source

# Zach Chase

dbutils.fs.mkdirs("FileStore/tables/lab3short")
dbutils.fs.mkdirs("FileStore/tables/lab3full")

for i in range(2):
    dbutils.fs.cp("FileStore/tables/shortLab3data{}.txt".format(i), "FileStore/tables/lab3short/shortLab3data{}.txt".format(i))
    
for i in range(4):
    dbutils.fs.cp("FileStore/tables/fullLab3data{}.txt".format(i), "FileStore/tables/lab3full/fullLab3data{}.txt".format(i))

# COMMAND ----------

sc = spark.sparkContext

short = sc.textFile("FileStore/tables/lab3short")

links = short.map(lambda line: line.split(' '))

links = links.map(lambda x: (x[0], sorted(x[1:]))).sortByKey()

links.collect()

# COMMAND ----------

full = sc.textFile("FileStore/tables/lab3full")

links = full.map(lambda line: line.split(' '))

links = links.map(lambda x: (x[0], sorted(x[1:]))).sortByKey()

links.collect()

# COMMAND ----------

links.count()

# COMMAND ----------


