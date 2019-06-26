import numpy as np
import pandas as pd
import sqlite3 as db

cnn = db.connect('D:\\Dados\\bstoll\\Documents\\SuperOneNotes\Estudo Dirigido\\Data Set\\Open University Learning Analytics Data Set\\OULAD.db')

df = pd.read_sql('SELECT code_module, code_presentation, id_student, SUM(sum_click) AS clicks FROM studentVle GROUP BY code_module, code_presentation, id_student', cnn)

df.to_csv('C:\\temp\\studentVle2.csv')