# Databricks notebook source

# Zach Chase

sc = spark.sparkContext

l = [x for x in range(100, 10001)]

rdd1 = sc.parallelize(l)

def check_prime(n):
            
    if n > 1:
        for i in range(2, int(n/2)+1):
            if (n % i) == 0:
                return False
    return True

print(rdd1.filter(check_prime).count())

# COMMAND ----------

import random
l2 = []

n = 1000

for i in range(n):
    l2.append(random.randint(1,101))
    

rdd2 = sc.parallelize(l2)
cel = rdd2.map(lambda x: (x-32)*(5/9))
total = cel.reduce(lambda x,y: x+y)
avg = total/n
print(avg)

# COMMAND ----------


