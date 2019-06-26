% rebase('layout.tpl', title='Machine Learning - Outliers', scriptGrafico=jsGrf)

<a href="/mineracao_dados?id={{tabela.id}}">Voltar</a>
<div class="card card-register mx-auto mt-5">
    <div class="card-header">Detecção de desvios ( Outliers )</div>
    <div class="card-body">
        <div class="form-group">
            <label for="tamTst">Tabela</label>
            <input class="form-control" value="{{tabela.nome}}" readonly>
        </div>
    </div>
</div>
<br />
<div class="row">
    <div class="col-lg-12">
        {{!htmlGrf}}
    </div>
</div>
