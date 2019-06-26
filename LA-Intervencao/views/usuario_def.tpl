% rebase('layout.tpl', title='Definir Visão', scriptGrafico='')

<a href="/usuario">Voltar</a>
<form action="/do_usuario_def" method="post">
    <input type="hidden" name="id" value="{{usuario.id}}" />
    <div class="col-lg-12">
        <div class="card card-register mx-auto mb-3 ">
            <div class="card-header">Editar Usuário</div>
            <div class="card-body">
                <div class="form-group">
                    <label for="nome">Nome</label>
                    <input type="text" class="form-control" value="{{usuario.nome}}" name="nome" />
                </div>
                <div class="form-group">
                    <label for="nome">Login</label>
                    <input type="text" class="form-control" value="{{usuario.login}}" name="login" />
                </div>
                <div class="form-group">
                    <label for="nome">Senha</label>
                    <input type="text" class="form-control" value="{{usuario.senha}}" name="senha" />
                </div>
                <div class="form-group">
                    <label for="nome">Tipo</label>
                    <select name="tipo" class="form-control" >
                        <option value="A" {{usuario.ds_tipo['A']}}>Analista</option>
                        <option value="P" {{usuario.ds_tipo['P']}}>Professor</option>
                        <option value="E" {{usuario.ds_tipo['E']}}>Estudante</option>
                    </select>
                </div>
                <div class="text-center">
                    <input type="submit" class="btn btn-primary btn-block" value="Salvar" />
                </div>
            </div>
        </div>
    </div>
</form>
<br>

