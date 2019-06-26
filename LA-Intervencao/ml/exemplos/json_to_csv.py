import pandas as pd
import numpy as np


lista = pd.read_json(r'D:\Dados\bstoll\Documents\SuperOneNotes\Estudo Dirigido\Data Set\University of Jisc Learning Analytics Data Set\uoj-master\studentmoduleinstance.json')

lista.to_csv(r'D:\Dados\bstoll\Documents\SuperOneNotes\Estudo Dirigido\Data Set\University of Jisc Learning Analytics Data Set\uoj-master\csv\studentmoduleinstance.csv')
