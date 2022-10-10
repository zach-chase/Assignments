# Databricks notebook source

# Zach Chase

sc = spark.sparkContext

test = ["a b c", "b a a", "c b", "d a"]

rdd1 = sc.parallelize(test)

links = rdd1.map(lambda x: (x.split(",")[0].split(" ")[0], list(set(x.split(",")[0].split(" ")[1:]))))

rankings = links.map(lambda x: (x[0], 1/len(test)))

print("Initial links:", links.collect())
print("Initial Rankings:", rankings.collect())

for i in range(10):
    
    print("Iteration:", i)
    
    temp = links.join(rankings)
    print("Joined RDD:", temp.collect())
    
    temp = rankings.join(links).values()
    temp = temp.map(lambda x: (x[0]/len(x[1]), x[1])) # Scale probability
    temp = temp.flatMapValues(lambda x: x).map(lambda x: (x[1], x[0])) # Apply probability to value
    print("Neighbor contributions:", temp.collect())

    temp = temp.reduceByKey(lambda x, y: x+y)
    print("New rankings:", temp.collect())

    rankings = temp
    
temp = temp.sortBy(lambda x: x[1], ascending = False)
print("Final sorted rankings:")

for key, value in zip(temp.keys().collect(), temp.values().collect()):
    print(key + " has rank " + str(value))

# COMMAND ----------

links = sc.textFile("FileStore/tables/lab3short")

links = links.map(lambda line: line.split(' '))

links = links.map(lambda x: (x[0], sorted(x[1:]))).sortByKey()

rankings = links.map(lambda x: (x[0], 1/len(test)))

for i in range(10):
    
    print("Iteration:", i)
    
    temp = links.join(rankings)
    
    temp = rankings.join(links).values()
    temp = temp.map(lambda x: (x[0]/len(x[1]), x[1])) # Scale probability
    temp = temp.flatMapValues(lambda x: x).map(lambda x: (x[1], x[0])) # Apply probability to value

    temp = temp.reduceByKey(lambda x, y: x+y)

    rankings = temp
    
temp = temp.sortBy(lambda x: x[1], ascending = False)
print("Final sorted rankings:")

for key, value in zip(temp.keys().collect(), temp.values().collect()):
    print(key + " has rank " + str(value))

# COMMAND ----------


