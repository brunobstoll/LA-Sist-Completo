"""
Mapeamento e centralização de acesso ao banco de dados
"""

from sqlalchemy import create_engine, Table, Column, MetaData, text
from sqlalchemy import Boolean, Integer, Unicode, String, ForeignKey, DateTime, LargeBinary
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker, mapper

import pandas as pd
import numpy as np
import random


print('DEFININDO MODELO...')

#arq_banco = 'LA_oula.db'
#arq_banco = 'LA_kaggle_StudentsAcademicPerformanceDataset.db'
arq_banco = 'intervencao.db'

print(arq_banco)


#-- Rede Gazeta
_url = r'sqlite:///C:\Users\bstoll\source\repos\LA-Intervencao\LA-Intervencao\\' + arq_banco

#-- Casa
#_url = r'sqlite:///C:\Users\Bruno Stoll\source\repos\LA-Intervencao\LA-Intervencao\\' + arq_banco

#-- pythonanywhere
#_url = r'sqlite:////home/bstoll/mysite/' + arq_banco

print(_url)

engine = create_engine(_url)
metadata = MetaData(bind=engine)

# ---------------------------------------------------------------------------------

print('  >> Tabela de Usuários')


tb_usuarios = Table('usuario', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('nome', String(30), nullable=False),
                    Column('login', String(20), nullable=False),
                    Column('senha', String(20), nullable=False),
                    Column('tipo', String(1), nullable=False) # P: professor; E: Estudante; A: Analista
                    )

class Usuario(object):
    def __init__(self, id, nome=None, login=None, senha=None, tipo=None):
        self.id = id
        self.nome = nome
        self.login = login
        self.senha = senha
        self.tipo = tipo

mapper(Usuario, tb_usuarios)

# ---------------------------------------------------------------------------------

print('  >> Tabela de Fonte de Dados')

tb_fonte_dados = Table('fonte_dados', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('tipo', String(1), nullable=True),
                   Column('nome', String(100), nullable=False),
                   Column('valor', String(500), nullable=False),
                   )

class FonteDados(object):
    def __init__(self, id, nome, tipo):
        self.id = id
        self.nome = nome
        self.tipo = tipo

mapper(FonteDados, tb_fonte_dados)

# ---------------------------------------------------------------------------------
print('  >> Tabela de Tabelas')

tb_tabelas = Table('tabela', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('id_fonte_dados', None, ForeignKey('fonte_dados.id')),
                   Column('nome', String(100), nullable=False),
                   Column('descricao', String(100), nullable=True),
                   Column('sql_origem', String(500), nullable=True),
                   Column('sql_destino', String(500), nullable=True),
                   Column('sql_sem_hist', String(500), nullable=True),
                   Column('pln', String(1), nullable=True),
                   )

class Tabela(object):
    def __init__(self, id, id_fonte_dados, nome, descricao = None, sql_origem = None, sql_destino = None, sql_sem_hist=None, pln=None):
        self.id = id
        self.id_fonte_dados = id_fonte_dados
        self.nome = nome
        self.descricao = descricao
        self.sql_origem = sql_origem
        self.sql_sem_hist = sql_sem_hist
        self.pln = pln

mapper(Tabela, tb_tabelas)

# ---------------------------------------------------------------------------------
print('  >> Tabela de Colunas')

tb_colunas = Table('coluna', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('id_coluna_cid', Integer, nullable=False),
                   Column('id_tabela', Integer, ForeignKey('tabela.id')),
                   Column('nome', String(100), nullable=False),
                   Column('sql', String(1000), nullable=True),
                   Column('tipo', String(1), nullable=False), # T: texto; N: números; D: sequências temporais ( dia; mês; ano; manha; tarde; noite; )
                   Column('titulo', String(100), nullable=True),
                   Column('descricao', String(500), nullable=True),
                   Column('desabilitado', Boolean, nullable=False),
                   Column('classe', Boolean, nullable=False),
                   Column('fl_aluno', Boolean, nullable=False),
                   Column('chave_estrangeira', Boolean, nullable=False),
                   Column('id_tabela_fk', None, ForeignKey('tabela.id'), nullable=True),
                   Column('id_coluna_fk', None, ForeignKey('coluna.id'), nullable=True),
                   Column('val_aluno_risco', String(100),nullable=True),
                   Column('sinonimos', String(1000),nullable=True),
                   )

class Coluna(object):
    def __init__(self, id, id_coluna_cid, id_tabela, nome, sql, tipo, titulo, descricao, desabilitado, classe, fl_aluno, chave_estrangeira, id_tabela_fk, id_coluna_fk, val_aluno_risco,sinonimos):
        self.id = id
        self.id_coluna_cid = id_coluna_cid
        self.id_tabela = id_tabela
        self.nome = nome
        self.sql = sql
        self.tipo = tipo
        self.titulo = titulo
        self.descricao = descricao
        self.desabilitado = desabilitado
        self.classe = classe
        self.fl_aluno = fl_aluno
        self.chave_estrangeira = chave_estrangeira
        self.id_tabela_fk = id_tabela_fk
        self.id_coluna_fk = id_coluna_fk
        self.val_aluno_risco = val_aluno_risco
        self.sinonimos = sinonimos

mapper(Coluna, tb_colunas)

# ---------------------------------------------------------------------------------
print('  >> Tabela de Exibição de Colunas')

tb_exibicao_coluna = Table('exibicao_coluna', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('id_tabela', None, ForeignKey('tabela.id')),    # origem  > tabela
                     Column('id_coluna', None, ForeignKey('coluna.id')),    # origem  > coluna
                     Column('id_tabela_fk', None, ForeignKey('tabela.id')), # destino > tabela
                     Column('id_coluna_fk', None, ForeignKey('coluna.id'))  # destino > coluna
                     )

class ExibicaoColuna(object):
    def __init__(self, id, id_tabela, id_coluna, id_tabela_fk, id_coluna_fk):
        self.id = id
        self.id_tabela = id_tabela
        self.id_coluna = id_coluna
        self.id_tabela_fk = id_tabela_fk
        self.id_coluna_fk = id_coluna_fk

mapper(ExibicaoColuna, tb_exibicao_coluna)

# ---------------------------------------------------------------------------------
print('  >> Tabela de Tabela de Predições')

tb_tabela_predicao = Table('tabela_predicao', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('id_tabela', None, ForeignKey('tabela.id')),
                     Column('modelo', String(5000), nullable=False),
                     Column('dt_processo', DateTime, nullable=True),
                     Column('reserva_treino', Integer, nullable=True),
                     Column('pesos', String(5000), nullable=True),
                     Column('id_alg_sel', Integer, nullable=True),
                     )

class TabelaPredicao(object):
    def __init__(self, id, id_tabela, modelo, dt_processo, reserva_treino, pesos, id_alg_sel):
        self.id = id
        self.id_tabela = id_tabela
        self.modelo = modelo
        self.dt_processo = dt_processo
        self.reserva_treino = reserva_treino
        self.pesos = pesos
        self.id_alg_sel = id_alg_sel

mapper(TabelaPredicao, tb_tabela_predicao)

# ---------------------------------------------------------------------------------
print('  >> Tabela de Tabela de Predições x Algoritmos')

tb_tabela_predicao_alg = Table('tabela_predicao_alg', metadata,
                         Column('id', Integer, primary_key=True),
                         Column('id_tabela_predicao', None, ForeignKey('tabela.id')),
                         Column('id_alg', Integer, nullable=False),
                         Column('modelo', LargeBinary, nullable=False),
                         Column('nome', String(100), nullable=False),
                         Column('pontos', String(20), nullable=False),
                         Column('tx_acerto', String(20), nullable=False),
                         Column('matriz_confusao', String(5000), nullable=True),
                         )

class TabelaPredicaoAlg(object):
    def __init__(self, id, id_tabela_predicao, id_alg, modelo, nome, pontos, tx_acerto, matriz_confusao):
        self.id = id
        self.id_tabela_predicao = id_tabela_predicao
        self.id_alg = id_alg
        self.modelo = modelo
        self.nome = nome
        self.pontos = pontos
        self.tx_acerto = tx_acerto
        self.matriz_confusao = matriz_confusao

mapper(TabelaPredicaoAlg, tb_tabela_predicao_alg)

# ---------------------------------------------------------------------------------
print('  >> Tabela de Tabela de Descrição')

tb_tabela_descricao = Table('tabela_descricao', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('id_tabela', None, ForeignKey('tabela.id')),
                      Column('id_alg', Integer, nullable=True), # 1 - Regras de Associação; 2 - Cluster ; 3 - Outliers
                      Column('modelo', String(5000), nullable=True),
                      Column('dt_processo', DateTime, nullable=True),
                      )

class TabelaDescricao(object):
    def __init__(self, id, id_tabela, id_alg, modelo, dt_processo):
        self.id = id
        self.id_tabela = id_tabela
        self.id_alg = id_alg
        self.modelo = modelo
        self.dt_processo = dt_processo


mapper(TabelaDescricao, tb_tabela_descricao)

# ---------------------------------------------------------------------------------
print('  >> Tabela de Visões')

tb_visoes = Table('visao', metadata,
            Column('id', Integer, primary_key=True),
            Column('id_tabela', None, ForeignKey('tabela.id')),
            Column('nome', String(100), nullable=True), # 1 - Regras de Associação; 2 - Cluster ; 3 - Outliers
            Column('tipo', String(1), nullable=True),
            Column('modelo', String(5000), nullable=True),
            )

class Visao(object):
    def __init__(self, id, id_tabela = None, nome = None, tipo = None, modelo = None):
        self.id = id
        self.id_tabela = id_tabela
        self.nome = nome
        self.tipo = tipo
        self.modelo = modelo


mapper(Visao, tb_visoes)

# ---------------------------------------------------------------------------------
print('  >> Tabela de Painel')

tb_painel = Table('painel', metadata,
               Column('id', Integer, primary_key=True),
               Column('nome', String(100), nullable=True),
               Column('tipo', String(1), nullable=True), # P: Professor; A: Aluno
               Column('modelo', String(5000), nullable=True),
               )

class Painel(object):
    def __init__(self, id, nome = None, tipo = None, modelo = None):
        self.id = id
        self.nome = nome
        self.tipo = tipo
        self.modelo = modelo


mapper(Painel, tb_painel)

# ---------------------------------------------------------------------------------
print('  >> Tabela de Mensagem')

tb_mensagem = Table('mensagem', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('id_tabela', None, ForeignKey('tabela.id')),
                    Column('id_coluna', None, ForeignKey('coluna.id')),
                    Column('id_usuario_aluno', None, ForeignKey('usuario.id')),
                    Column('val_atual', String(5000), nullable=True),
                    Column('val_suger', String(5000), nullable=True),
                    Column('descartado', String(1), nullable=True),
                    Column('lido', String(1), nullable=True),
                    Column('dt_gerado', DateTime, nullable=True),
                    Column('descricao', String(5000), nullable=True),
               )

class Mensagem(object):
    def __init__(self, id, id_tabela=None, id_coluna=None, id_usuario_aluno=None, val_atual=None, val_suger=None, descartado=None, lido=None, dt_gerado=None, descricao=None):
        self.id = id
        self.id_tabela = id_tabela
        self.id_coluna = id_coluna
        self.id_usuario_aluno = id_usuario_aluno
        self.val_atual = val_atual
        self.val_suger = val_suger
        self.descartado = descartado
        self.lido = lido
        self.dt_gerado = dt_gerado
        self.descricao = descricao



mapper(Mensagem, tb_mensagem)

# ---------------------------------------------------------------------------------
def getSession():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def consultarSQLDataFrame(sql):
    return pd.read_sql(sql, engine)

def consultarSQL(sql):
    session = getSession()
    return session.execute(sql).fetchall()