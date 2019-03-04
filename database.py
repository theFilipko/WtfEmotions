import sqlite3
import numpy
from scipy.stats import mode
import statsmodels.stats.inter_rater
import os

# # import data from file into database
# connection = sqlite3.connect("wtfemotions.db")
# sql = ''' INSERT INTO faces (name,emotions,count)
#               VALUES(?,?,?) '''
# with connection:
#     cursor = connection.cursor()
#     image_names = os.listdir("data")
#     for image_name in image_names:
#         data = ("data/" + image_name, "", 0)
#         cursor.execute(sql, data)


# analyse results using Fleiss' kappa
# here I want to get the coefficient for each image how good, how well did they agree on the emotion
# so for this I will compute only the Pi value from the Fleiss' kappa algorithm
connection = sqlite3.connect("wtfemotions.db")
sql = ''' SELECT * FROM faces '''
with connection:
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()

A = numpy.zeros((1377, 31))
B = numpy.zeros((1377, 9))  # grouped by categories
f = "id,emotion\n"
Pis = []
bad = 0
i = 0
for row in rows:
    cat = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    j = 0
    while j < 31:
        c = int(row[2][j])
        cat[c - 1] += 1
        A[i, j] = c
        j += 1

    j = 0
    while j < 9:
        B[i, j] = cat[j]
        j += 1

    # compute Pi
    Pi = sum(map(lambda x: x*x, B[i])) / (31 * (31 - 1))
    Pis.append(Pi)
    if Pi < 0.2:
        print("{},{},{},{},{}".format(row[0], row[1], row[2], mode(A[i])[0][0], Pi))
        # Pis.append(Pi)
    if mode(A[i])[0][0] == 9:
        print("  {},{},{},{},{}".format(row[0], row[1], row[2], mode(A[i])[0][0], Pi))
        # Pis.append(Pi)

    file_name = row[1][5:]
    if file_name[0] == 'x':
        if Pi > 0.2 and mode(A[i])[0][0] != 9:
            f += "{},{}\n".format(file_name, mode(A[i])[0][0])
        else:
            bad += 1
    i += 1

with open("dataset_x.csv", "w+") as file:
    file.write(f[:-1])

print(bad)
