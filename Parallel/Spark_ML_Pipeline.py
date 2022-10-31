# Zach Chase

# Databricks notebook source
train_file = "dbfs:///FileStore/tables/heartTraining.csv"
test_file = "dbfs:///FileStore/tables/heartTesting.csv"

# COMMAND ----------

from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import StringIndexer, Bucketizer, VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.sql.types import StructType, StructField, LongType, StringType, DoubleType
from pyspark.ml import Pipeline
from pyspark.sql.functions import col, avg


dataSchema = StructType( \
                           [StructField('id', LongType(), True), \
                            StructField('age', LongType(), True), \
                            StructField('sex', StringType(), True), \
                            StructField('Chol', LongType(), True), \
                            StructField('Pred', StringType(), True)
                           ])

# Load Data
train_df = spark.read.format("csv").option("header", True).schema(dataSchema).load(train_file)
test_df = spark.read.format("csv").option("header", True).schema(dataSchema).load(test_file)

# Start Logistic Regression
lr = LogisticRegression()

# Fit ages into buckets
ageSplits = [-float("inf"), 40, 50, 60, 70, float("inf")]
ageBucketizer = Bucketizer(splits=ageSplits, inputCol='age', outputCol="ageBucket")

# Index Sex and Predictions
sexIndexer = StringIndexer(inputCol='sex', outputCol='sexIndex')
predIndexer = StringIndexer(inputCol='Pred', outputCol='label')

#Assemble model into Pipeline
vecAssem = VectorAssembler(inputCols=['ageBucket', 'sexIndex', 'Chol'], outputCol='features') # Group input into features
myStages =[ageBucketizer, sexIndexer, predIndexer, vecAssem, lr] # Stages for pipeline
p = Pipeline(stages=myStages)
pModel = p.fit(train_df)

# Get predictions for test data
pred = pModel.transform(test_df)

# Display results (id, probability and prediction data (just the first 20 lines are fine).)
pred.select("id", "probability", "prediction").show()

# COMMAND ----------

# Get predictions for training data
train_pred = pModel.transform(train_df)

# Display results on training data
train_pred = train_pred.withColumn("correct", col("label") == col("prediction"))
train_pred.agg(avg(col("correct").cast("double")).alias('Training Accuracy')).show()

# COMMAND ----------


