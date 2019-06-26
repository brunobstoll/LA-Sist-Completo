#import csv
import pandas as pd
import glob
import os
import model.dataBase as db
from sqlalchemy import text

def do_directory(dirname, db):
    for filename in glob.glob(os.path.join(dirname, '*.csv')):
        do_file(filename, db)

def do_file(filename, db):
    df = pd.read_csv(filename)
    table=os.path.splitext(os.path.basename(filename))[0]
    cols = df.columns

    sql = 'drop table if exists "__{}"'.format(table)
    db.execute(sql)

    sql = 'create table "__{table}" ( {cols} )'.format(
        table=table,
        cols=','.join('"{}"'.format(col) for col in cols))
    db.execute(sql)

    db.commit()

    #dados = list(df.T.to_dict().values())

    i_qtd_commited = 0
    i_conta_commit = 0
    i_conta = i_qtd_commited
    i_qtd = len(df)

    for index, row in df[i_qtd_commited:].iterrows():


        #for col in cols:
        #    row[col] = str(row[col])
        #    if type(row[col]) == list:
        #        row[col] = ''

        sql = 'insert into "__{table}" values ( {vals} )'.format(
        table=table,
        vals=','.join(':' + col for col in cols))

        db.execute(text(sql), dict(row))

        i_conta += 1
        i_conta_commit+= 1
        print(str(i_conta) + ' / ' + str(i_qtd) + ' >>   ' + str(round((i_conta / i_qtd) * 100, 2)) + '%')
        print(sql)

        if i_conta_commit == 1000:
            db.commit()
            i_conta_commit = 0

    db.commit()


def executar(arquivo):
    conn = db.getSession()
    do_file(arquivo, conn)