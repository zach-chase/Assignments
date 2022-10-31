# Zach Chase

# Databricks notebook source
import numpy as np

sc = spark.sparkContext

set_cell_size = .75
set_distance = .75

file = "FileStore/tables/assignment1"

loaded_data = sc.textFile(file).map(lambda l: (l.split(",")[0], (float(l.split(",")[1]), float(l.split(",")[2]))))

# COMMAND ----------

# Define functions

def create_grid(x, size = set_cell_size):
    
    return (x[0],(int(x[1][0]/size), int(x[1][1]/size)))

def add_borders(cell):
    
    point = cell[0]
    cord = cell[1]
    
    borders = [str(cord)]
    directions = [[1,0], [0,1], [1,1],
                 [-1,0], [0,-1], [-1,-1],
                 [1,-1], [-1,1]]
    
    for i in directions:
        borders.append(str((cord[0] + i[0], cord[1] + i[1])))
    
    return (point, borders)

def flat(x): 
    return x

def check_distance(x, distance = set_distance):
    p1 = x[1][2][0]
    p2 = x[1][3][0]
    
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]
    
    dist = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    
    if dist < distance:
        
    
        return (x[1][0], x[1][1])

# COMMAND ----------

data_cells = loaded_data.map(lambda x: create_grid(x))
data_cells = data_cells.map(lambda x: add_borders(x))
data_cells = data_cells.flatMapValues(flat)
data_cells = data_cells.map(lambda x: (x[1], x[0]))
data_cells = data_cells.groupByKey().mapValues(list)
data_cells_clean = data_cells.filter(lambda x: len(x[1]) > 1)

values = data_cells_clean.values().collect()
data_no_copies = []
for row in values:
    for p1 in row:
        for p2 in row:
            if p1 != p2 and [p1, p2] not in data_no_copies and [p2, p1] not in data_no_copies:
                data_no_copies.append([p1, p2])

final = []
for counter, i in enumerate(data_no_copies):
    row = (counter, (i[0], i[1], loaded_data.lookup(i[0]), loaded_data.lookup(i[1])))
    final.append(row)

final = sc.parallelize(final)
final = final.map(lambda x: check_distance(x))
final = final.filter(lambda x: x is not None)
print(set_distance, '\n')
str(final.count()) + str(final.collect())

# COMMAND ----------


