import pandas as pd
import numpy as np
from sklearn import tree
import warnings 



train_path = 'C:/Users/Bruno Stoll/OneDrive/Mestrado/DataSets/Student Performance Data Set/student/student-mat-tst.csv'
train  = pd.read_csv(train_path)
colResultado = 'Nivel'


train[colResultado] = 0
train[colResultado][train['G3'] > 12] = 1


target = np.array(train[colResultado].values)
del train[colResultado]

#train.head()
#print "Shape: " + train.shape
#train.head()
#train.describe()

cols = []
pesos = {}
for col in list(train.columns.values):
    cols.append(col)
    pesos[col] = ''
    identif = 0
    for val in train[col].unique():
        identif +=1
        train[col][train[col] == val] = int(identif)

features = train.values

clf = tree.DecisionTreeClassifier()
clf = clf.fit(features, target)

importances = clf.feature_importances_
for k in range(0, len(importances)):
    print ('Importância ' + str(importances[k]))
    pesos[cols[k]] = importances[k]


score = clf.score(features, target)

print(str(score))
