"Interface para processamento das importações"

import model.dataBase as db
import os
import model.ImportarCSV as impCSV
import model.ImportarJSON as impJSON


# ------------------------------------------------------------------------
def ListarFontes():
    session = db.getSession()
    lista = session.query(db.FonteDados).all()
    session.close()

    for item in lista:
        if item.tipo == 'B':
            item.descr_tipo = 'Banco'
        elif item.tipo == 'C':
            item.descr_tipo = 'CSV'
        elif item.tipo == 'T':
            item.descr_tipo = 'Texto'
        elif item.tipo == 'J':
            item.descr_tipo = 'JSON'

        item.nome_edt = '<a href="#" onclick="Editar(' + str(item.id) + ')">' + item.nome + '</a>'
        item.comando_tabelas = '<a href="/seltabelas?id=' + str(item.id) + '">Selecionar</a> | <a href="lsttabelas?id='+ str(item.id) +'" >Editar</a>'

    return lista

def SalvarFonte(fonte):
    session = db.getSession()

    if fonte.id == '0':
        fonte.id = None
        session.add(fonte)
    else:
        iid = fonte.id
        obj2 = session.query(db.FonteDados).filter_by(id=iid).first()
        obj2.nome = fonte.nome
        obj2.tipo = fonte.tipo
        obj2.valor = fonte.valor

    session.commit()
    session.close()

def ObterFonte(iid):
    if iid == '0':
        return db.FonteDados('0', '', '')
    else:
        session = db.getSession()
        obj = session.query(db.FonteDados).filter_by(id=iid).first()
        session.close()

        return obj

def ListarTabelasFonte(iid):
    lista = []
    obj = ObterFonte(iid)
    if obj.tipo == 'C' or obj.tipo == 'J':
        table = '__' + os.path.splitext(os.path.basename(obj.valor))[0]

        lista.append( { 'nome': table, 'tabela': table } )

    return lista

def ExecutarImportacao(iid):
    obj = ObterFonte(iid)
    table = '__' + os.path.splitext(os.path.basename(obj.valor))[0]
    RemoverTabela(table)
    CriarTabelaSeNaoExiste(obj.valor, obj.tipo)

    objTabela = db.Tabela('0', obj.id, table)
    SalvarTabela(objTabela)
    GerarColunas(table)

def GerarColunas(table):
    session = db.getSession()
    obj = session.query(db.Tabela).filter_by(nome=table).first()

    sql = 'pragma table_info([' + table + '])'
    resultado = session.execute(sql).fetchall()

    for row in resultado:
        coluna = db.Coluna(None, int(row['cid']) + 1, obj.id, row['name'], row['name'], 'T', row['name'], '', False, False, False, False, None, None, None)
        session.add(coluna)

    session.commit()

def GerarColunasComSQL(table, sql):
    session = db.getSession()
    obj = session.query(db.Tabela).filter_by(nome=table).first()

    sql = 'SELECT * FROM (' + sql + ') AS T WHERE 0=1'
    df = db.consultarSQLDataFrame(sql)

    i_conta = 0
    for col in df.columns:
        i_conta+=1
        coluna = db.Coluna(None, i_conta, obj.id, col, col, 'T', col, '', False, False, False, False, None, None, None)
        session.add(coluna)

    session.commit()


def CriarTabelaSeNaoExiste(arquivo, tipo):
    table = '__' + os.path.splitext(os.path.basename(arquivo))[0]

    sql = 'SELECT COUNT(name) AS qtd FROM sqlite_master WHERE type=\'table\' AND name = \'' + table + '\''

    session = db.getSession()
    session.execute(sql).fetchall()

    session.close()

#    if resultado[0]['qtd'] == 0:
    if tipo == 'C':
        impCSV.executar(arquivo)
    elif tipo == 'J':
        impJSON.executar(arquivo)

    CriarIndices(table)

def RemoverTabela(table):
    #sql = 'drop table if exists ' + table
    #resultado = session.execute(sql)

    session = db.getSession()

    obj = session.query(db.Tabela).filter_by(nome=table).first()
    if obj != None:
        listaCol = session.query(db.Coluna).filter_by(id_tabela=obj.id)
        for col in listaCol:
            session.delete(col)

        session.delete(obj)

        session.commit()

    session.close()

# ------------------------------------------------------------------------

def ListarTabelas(idFonte=0):
    session = db.getSession()
    if idFonte == 0:
        lista = session.query(db.Tabela).all()
    else:
        lista = session.query(db.Tabela).filter_by(id_fonte_dados=idFonte).all()

    session.close()

    for tab in lista:
        tab.comandoNome = '<a href="/edttabela?id=' + str(tab.id) + '">' + tab.nome + '</a>'

    return lista

def SalvarTabela(tabela):
    session = db.getSession()

    if tabela.id == '0':
        tabela.id = None
        session.add(tabela)
    else:
        iid = tabela.id
        obj2 = session.query(db.Tabela).filter_by(id=iid).first()
        obj2.id_fonte_dados = tabela.id_fonte_dados
        obj2.nome = tabela.nome
        obj2.descricao = tabela.descricao
        obj2.sql_origem = tabela.sql_origem
        obj2.sql_destino = tabela.sql_destino
        obj2.sql_sem_hist = tabela.sql_sem_hist
        obj2.pln = tabela.pln

    session.commit()
    session.close()

    return tabela

def ObterTabela(iid):
    if iid == '0':
        return db.Tabela('0', '', '')
    else:
        session = db.getSession()
        obj = session.query(db.Tabela).filter_by(id=iid).first()
        session.close()

        return obj

def ObterTabelaPorNome(nome):
    session = db.getSession()
    obj = session.query(db.Tabela).filter_by(nome=nome).first()
    session.close()

    return obj

def RecriarCampos(iid):
    session = db.getSession()

    tabela = session.query(db.Tabela).filter_by(id=iid).first()

    listaCol = session.query(db.Coluna).filter_by(id_tabela=iid)
    for col in listaCol:
        session.delete(col)

    sql = 'SELECT * FROM [' + tabela.nome + '] WHERE 0=1'
    if tabela.sql_destino != None and tabela.sql_destino != '':
        sql = 'SELECT * FROM (' + tabela.sql_destino + ') AS T WHERE 0=1'

    df = db.consultarSQLDataFrame(sql)

    i_conta = 0
    for col in df.columns:
        i_conta+= 1
        coluna = db.Coluna(None, i_conta, tabela.id, col, col, 'T', col, '', False, False, False, False, None, None, None)
        session.add(coluna)

    session.commit()
    session.close()
# ------------------------------------------------------------------------

def CriarTabelaDoSql(sql, nome):
    sql_dropTable = 'DROP TABLE IF EXISTS [' + nome + '];'
    sql_createTable = ' CREATE TABLE [' + nome + '] AS ' + sql

    print(sql_dropTable)
    print(sql_createTable)

    session = db.getSession()
    resultado = session.execute(sql_dropTable)
    resultado = session.execute(sql_createTable)

    session.commit()
    session.close()

def CriarIndices(table):
    print('Criando indíces...')
    print('')
    print('Limpando...')
    session = db.getSession()
    dfIdx = db.consultarSQLDataFrame('PRAGMA index_list([' + table + ']);')
    for idx in dfIdx['name']:
        sql = 'DROP INDEX [' + idx + ']'
        print(sql)
        session.execute(sql)

    print('')
    print('')
    sql = 'SELECT * FROM [' + table + '] WHERE 0=1'
    print(sql)
    df = db.consultarSQLDataFrame(sql)
    print('Criando...')

    for col in df.columns:
        sql_create_index = 'CREATE INDEX [idx_' + table + '_' + col + '] ON [' + table + ']([' + col + '])'
        print(sql_create_index)
        session.execute(sql_create_index)

    session.commit()
    session.close()
    print('')
    print('Finalizado!')


