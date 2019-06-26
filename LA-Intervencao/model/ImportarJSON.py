import csv
import sqlite3
import glob
import os
import model.dataBase as db
from sqlalchemy import text
import pandas as pd
import numpy as np

def do_directory(dirname, db):
    for filename in glob.glob(os.path.join(dirname, '*.csv')):
        do_file(filename, db)

def do_file(filename, db):
    df = pd.read_json(filename)

    table=os.path.splitext(os.path.basename(filename))[0]
    cols = df.columns

    sql = 'drop table if exists "__{}"'.format(table)
    db.execute(sql)

    sql = 'create table "__{table}" ( {cols} )'.format(
        table=table,
        cols=','.join('"{}"'.format(col) for col in cols))
    db.execute(sql)

    i_conta = 0
    i_qtd = len(df)
    for index, row in df.iterrows():
        for col in cols:
            row[col] = str(row[col])
            if type(row[col]) == list:
                row[col] = ''

        sql = 'insert into "__{table}" values ( {vals} )'.format(
        table=table,
        vals=','.join(':' + col for col in cols))

        db.execute(text(sql), dict(row))
        i_conta += 1
        print(str(i_conta) + '/' + str(i_qtd))
        print(sql)

    db.commit()



def executar(arquivo):
    conn = db.getSession()
    do_file(arquivo, conn)