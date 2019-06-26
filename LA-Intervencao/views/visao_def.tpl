% rebase('layout.tpl', title='Definir Visão', scriptGrafico='<script>ReconstruirGrid();</script>')

<a href="/visao?id={{idTabela}}">Voltar</a>
<form action="/do_visao_def" method="post">
    <input type="hidden" name="id" value="{{id}}" />
    <input type="hidden" name="id_tabela" value="{{idTabela}}" />
    <div class="row">
        <div class="col-lg-5">
            <div class="card card-register mx-auto mb-3 ">
                <!--mt-5-->
                <div class="card-body">
                    <div class="form-group">
                        <label for="nome">Tabela</label>
                        <input type="text" class="form-control" readonly value="{{nomeTabela}}" />
                    </div>
%for col in listaColunas:
                    <div class="checkbox">
%if col.selecionado == True:
                        <label><input type="checkbox" name="coluna_{{col.id}}" onclick="fnAdicionar(this, '{{col.id}}', '{{col.nome}}')" checked> {{col.titulo}}</label>
%else:
                        <label><input type="checkbox" name="coluna_{{col.id}}" onclick="fnAdicionar(this, '{{col.id}}', '{{col.nome}}')"> {{col.titulo}}</label>
%end
                    </div>
%end
                </div>
            </div>
        </div>
        <div class="col-lg-7">
            <div class="card card-register mx-auto mb-3 ">
                <!--mt-5-->
                <div class="card-body">
                    <div class="form-group">
                        <label for="nome">Nome</label>
                        <input class="form-control" name="nome" id="nome" type="text" placeholder="Informe o nome" value="{{nome}}">
                    </div>
                    <div class="form-group">
                        <label for="nome">Tipo</label>
                        <select class="form-control" name="tipo" id="tipo">
                            <option value="1" {{tipo['1']}}>Gráfico de Pizza</option>
                            <option value="2" {{tipo['2']}}>Gráfico Barras</option>
                            <option value="3" {{tipo['3']}}>Gráfico Linha</option>
                            <option value="4" {{tipo['4']}}>Informação em Cards</option>
                            <option value="5" {{tipo['5']}}>Informação em Grid</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="obj">Modelo</label>
                        <input type="text" class="form-control" id="modelo" name="modelo" value="{{modelo}}" />
                    </div>
                </div>
                <br />
                <div class="card-body">
                    <div class="table-responsive nowrap">
                        <table class="table table-bordered" id="dataTableSP" cellspacing="0">
                            <thead>
                                <tr>
                                    <th>Campo</th>
                                    <th>Agrupador</th>
                                    <th>Gráfico</th>
                                </tr>
                            </thead>
                            <tbody id="bConfigVisao"></tbody>
                        </table>
                    </div>
                </div>
            </div>

        </div>
    </div>
    <div class="row">
        <div class="col-lg-12">
            <div class="card card-register mx-auto mb-3 ">
                <!--mt-5-->
                <div class="card-body">
                    <div class="text-center">
                        <input type="submit" class="btn btn-primary btn-block" value="Salvar" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</form>
<br>
<script>
    var objConfi = [];

    function fnAdicionar(obj, id, nome) {

        if (obj.checked) {
            objConfi.push({
                "id_coluna": id,
                "nome": nome,
                "agrupador": '',
                "grafico": '',
            });

            fnAdicionarValor(id, nome);
        } else {
            $("#trRow" + id).remove();
            ReconstruirConfig();
        }
    }

    function fnAdicionarValor(id, nome) {
        var agrupador = '<select id="agrupador' + id + '" class="form-control" onchange="ReconstruirConfig()" >' +
            '<option value=""></option>' +
            '<option value="SUM">Soma</option>' +
            '<option value="COUNT">Quantidade</option>' +
            '<option value="AVG">Média</option>' +
            '<option value="MIN">Mínimo</option>' +
            '<option value="MAX">Máximo</option>' +
            '</select>';
        var defGrafico = '<select id="grafico' + id + '" class="form-control" onchange="ReconstruirConfig()" >' +
            '<option value=""></option>' +
            '<option value="S">Serie</option>' +
            '<option value="C">Categoria</option>' +
            '<option value="V">Valor</option>' +
            '</select>';

        var htmlRow = '<tr id="trRow' + id + '" data="' + id + '" nome="' + nome + '">' +
            '<td>' + nome + '</td>' +
            '<td>' + agrupador + '</td>' +
            '<td>' + defGrafico + '</td>' +
            '</tr>'


        var htmlAnt = $('#bConfigVisao').html();
        $('#bConfigVisao').html(htmlAnt + htmlRow);

        $('#modelo').val(JSON.stringify(objConfi));
    }

    function ReconstruirConfig() {
        objConfi = [];
        var i;
        for (i = 0; i < $('#bConfigVisao').children('tr').length; i++) {
            var trRowId = $('#bConfigVisao').children('tr')[i].id;

            var idColuna = $('#' + trRowId).attr('data');
            var nome = $('#' + trRowId).attr('nome');
            var agrupador = $('#agrupador' + idColuna).val();
            var grafico = $('#grafico' + idColuna).val();

            objConfi.push({
                "id_coluna": idColuna,
                "nome": nome,
                "agrupador": agrupador,
                "grafico": grafico,
            });            
        }

        $('#modelo').val(JSON.stringify(objConfi));
    }

    function ReconstruirGrid() {
        $('#bConfigVisao').html('');
        for (var i = 0; i < objConfi.length; i++) {
            var obj = objConfi[i];
            fnAdicionarValor(obj.id_coluna, obj.nome);
        }

        for (var i = 0; i < objConfi.length; i++) {
            var obj = objConfi[i];
            $('#agrupador' + obj.id_coluna).val(obj.agrupador);
            $('#grafico' + obj.id_coluna).val(obj.grafico);
        }
    }

%if modelo != '':
    objConfi = {{!modelo}};
%end
</script>
