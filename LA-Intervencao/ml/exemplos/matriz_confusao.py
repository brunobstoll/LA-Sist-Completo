
from sklearn.metrics import confusion_matrix
y_true = [2, 0, 2, 2, 0, 1]
y_pred = [2, 0, 2, 2, 0, 2]
print(confusion_matrix(y_true, y_pred))