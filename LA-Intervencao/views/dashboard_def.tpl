% rebase('layout.tpl', title='Definir Visão', scriptGrafico=js)

<form action="/do_painel" method="POST">
    <input type="hidden" name="id" value="{{painel.id}}" />
    <div class="card mb-3">
        <div class="card-body">
            <div class="card-body">
                <div class="form-group">
                    <label for="nome">Nome</label>
                    <input type="text" class="form-control" name="nome" value="{{painel.nome}}" />
                </div>
                <div class="form-group">
                    <label>Tipo</label>
                </div>
                <div class="form-group row">
                    <div class="radio">
                        <label><input type="radio" name="tipo" {{painel.ds_tipo['P']}} value="P"> Professor&nbsp;&nbsp;</label>
                    </div>
                    <div class="radio">
                        <label><input type="radio" name="tipo" {{painel.ds_tipo['A']}} value="A"> Aluno </label>
                    </div>
                </div>
                <hr />
                <div class="form-group row">
                    <label>Tipo</label>
                </div>
                <div class="form-group row">
                    <div class="radio">
                        <label><input type="radio" name="coluna" value="12" checked> <img src="/static/img/col-12.JPG" /></label>
                    </div>
                    <div class="radio">
                        <label><input type="radio" name="coluna" value="4-4-4"> <img src="/static/img/col-4-4-4.JPG" /></label>
                    </div>
                    <div class="radio">
                        <label><input type="radio" name="coluna" value="4-8"> <img src="/static/img/col-4-8.JPG" /></label>
                    </div>
                    <div class="radio">
                        <label><input type="radio" name="coluna" value="8-4"> <img src="/static/img/col-8-4.JPG" /></label>
                    </div>
                    <div class="radio">
                        <label><input type="radio" name="coluna" value="6-6"> <img src="/static/img/col-6-6.JPG" /></label>
                    </div>
                </div>
                <div class="form-group row">
                    <label for="objConfigDashboard">Modelo</label>
                    <input type="text" class="form-control" name="modelo" id="modelo" value="{{painel.modelo}}" />
                </div>
            </div>
        </div>
        <div class="text-center">
            <input type="button" class="btn btn-block" value="Adicionar" onclick="fnAdicionar(false, 0, '')" />
        </div>
    </div>

    <div id="conteudo"></div>
    <br>
    <div class="text-center">
        <input type="submit" class="btn btn-primary btn-block" value="Salvar" />
    </div>
    <br>

</form>
<script>

    var idLinha = 0;
    var idSelVisao = 0;
    var objConfi = [];

    function fnAdicionar(adModelo, iidLinha, o_opcaoLinha) {
        var opcaoLinha = '';
        if (adModelo == false) {
            idLinha = idLinha + 1;
            opcaoLinha = $("input[type='radio'][name='coluna']:checked").val();
        } else {
            idLinha = iidLinha;
            opcaoLinha = o_opcaoLinha;
        }

        var htmlRow = '<div id="dvRow' + idLinha.toString() + '" class="row" style="margin-top: 10px; border: solid 1px #ccc; padding: 5px;">' +
            '  <div class="col-lg-12" style="text-align: rigth;"><button onclick="fnExcluir(this)">Remover (' + idLinha.toString() + ')</button></div>';

        switch (opcaoLinha) {
            case '12':
                htmlRow += fnCell(opcaoLinha, '12', '1', adModelo);
                break;
            case '4-4-4':
                htmlRow += fnCell(opcaoLinha, '4', '1', adModelo);
                htmlRow += fnCell(opcaoLinha, '4', '2', adModelo);
                htmlRow += fnCell(opcaoLinha, '4', '3', adModelo);
                break;
            case '4-8':
                htmlRow += fnCell(opcaoLinha, '4', '1', adModelo);
                htmlRow += fnCell(opcaoLinha, '8', '2', adModelo);
                break;
            case '8-4':
                htmlRow += fnCell(opcaoLinha, '8', '1', adModelo);
                htmlRow += fnCell(opcaoLinha, '4', '2', adModelo);
                break;
            case '6-6':
                htmlRow += fnCell(opcaoLinha, '6', '1', adModelo);
                htmlRow += fnCell(opcaoLinha, '6', '2', adModelo);
                break;
            default:
                break;
        }

        htmlRow += '</div>';

        // var htmlAnt = $('#conteudo').html();
        // $('#conteudo').html(htmlAnt + htmlRow);
        $('#conteudo').append(htmlRow);

        $('#modelo').val(JSON.stringify(objConfi));
    }

    function fnCell(opcaoLinha, opcaoColuna, idColuna, adModelo) {
        if (adModelo == false) {
            var currObjConfig = {
                "idLinha": idLinha,
                "id_visao": 0,
                "opcaoLinha": opcaoLinha,
                "opcaoColuna": opcaoColuna,
                "idColuna": idColuna
            };

            objConfi.push(currObjConfig);
        }

        return '<div class="col-lg-' + opcaoColuna + '">' + fnSelect(opcaoLinha, opcaoColuna, idColuna) + '</div>';
    }

    var visoes = [
%for visao in listaVisao:
            '<option value="{{visao.id}}">{{visao.nome}}</option>',
%end
    ];
    function fnSelect(opcaoLinha, opcaoColuna, idColuna) {
        var iid = fnId();
        return '<select id="' + iid + '" name="selObj" class="form-control" idLinha="' + idLinha + '" opcaoLinha="' + opcaoLinha + '" opcaoColuna="' + opcaoColuna + '" idColuna="' + idColuna + '" onchange="fnMudarVisao(this.id)">' +
            '<option value="0"></option>' +
%for visao in listaVisao:
            '<option value="{{visao.id}}">{{visao.nome}}</option>' +
%end
        '</select>';
    }

    function fnMudarVisao(id) {
        var i;
        var objSel = $('#' + id);
        for (i = 0; i < objConfi.length; i++) {
            var currObjConfig = objConfi[i];
            if (currObjConfig.idLinha == objSel.attr('idLinha') &&
                currObjConfig.opcaoLinha == objSel.attr('opcaoLinha') &&
                currObjConfig.opcaoColuna == objSel.attr('opcaoColuna') &&
                currObjConfig.idColuna == objSel.attr('idColuna')) {

                currObjConfig.id_visao = parseInt(objSel.val());
            }
        }

        $('#modelo').val(JSON.stringify(objConfi));
    }

    function reconstruirConfig() {
        objConfi = [];
        var i;
        for (i = 0; i < document.getElementsByName('selObj').length; i++) {
            var objSel = document.getElementsByName('selObj')[i];
            var currObjConfig = {
                "idLinha": objSel.getAttribute('idLinha'),
                "opcaoLinha": objSel.getAttribute('opcaoLinha'),
                "opcaoColuna": objSel.getAttribute('opcaoColuna'),
                "idColuna": objSel.getAttribute('idColuna')
            };

            objConfi.push(currObjConfig);
        }
    }

    function fnId() {
        idSelVisao++
        return 'selObj' + idSelVisao.toString();
    }
%if painel.modelo != '':
    objConfi = {{!painel.modelo}};
%end

    function ReconstruirGrid() {
        $('#conteudo').html('');

        var ultObjConfig = objConfi[objConfi.length - 1];

        for (var i_idLinha = 1; i_idLinha <= ultObjConfig.idLinha; i_idLinha++) {
            idLinha = i_idLinha;
            var opcaoLinha = '';
            var existe = false;
            for (var i = 0; i < objConfi.length; i++) {
                if (objConfi[i].idLinha == i_idLinha) {
                    opcaoLinha = objConfi[i].opcaoLinha;
                    existe = true;
                    break;
                }
            }

            if (existe == false) {
                continue;
            }

            fnAdicionar(true, i_idLinha, opcaoLinha);
            for (var i = 0; i < objConfi.length; i++) {
                var corrObjConfi = objConfi[i];
                if (corrObjConfi.idLinha.toString() == i_idLinha.toString()) {
                    $("select[idLinha='" + corrObjConfi.idLinha.toString() + "'][idColuna='" + corrObjConfi.idColuna.toString() + "']").val(corrObjConfi.id_visao.toString());
                }
            }
        }
    }

    function fnExcluir(btExcluir) {
        // dvRow + id
        var idEl = btExcluir.parentElement.parentElement.id;
        var idRemove = parseInt(idEl.replace('dvRow', ''));
        //alert(idRemove);
        var idObj = "#" + idEl;
        $(idObj).remove();

        reconstruirConfig();
        $('#modelo').val(JSON.stringify(objConfi));
    }

</script>
