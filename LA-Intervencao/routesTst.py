from bottle import route, view, template, redirect, request, post, response
from datetime import datetime
import os


@route('/teste')
@view('teste')
def Teste():

    return dict()


@route('/teste2')
@view('teste2')
def Teste2():
    tstGrfA = template('grfArea.tpl')
    return dict(
        tstGrfA=tstGrfA)

@route('/')
@route('/testeFormUpload')
@view('testeFormUpload')
def testeFormUpload():

    return dict(
        title='Home Page'
    )

@post('/do_testeFormUpload')
def do_testeFormUpload():
    path = "/home/bstoll/mysite/arquivosUpld"
    arquivo    = request.files.get('arquivo')
    name, ext = os.path.splitext(arquivo.filename)
    if ext != '.csv':
        return 'arquivo inválido'

    path_save = "{path}/{file}".format(path=path, file=name)
    arquivo.save(path_save)

    redirect('/testeFormUpload')