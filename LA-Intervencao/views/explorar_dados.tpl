% rebase('layout.tpl', title='Transformação', scriptGrafico='')

<div class="card mb-3">
        <!-- <i class="fa fa-table"></i> Data Table Example</div> -->
    <div class="card-body">
		<form method="POST" action="/do_explorar_dados">
		<div class="form-group">
            <input type="hidden" id="idTabela" name="idTabela" value="{{idTabela}}" />
			<label for="nome">Tabela</label>
			<select id="id" class="form-control" onchange="sel(this)">
				<option value="0">Selecione uma tabela</option>
%for tab in listaTabelas:
%if tab.selecionado == True:
				<option value="{{tab.id}}" selected>{{tab.nome}}</option>
%else:
				<option value="{{tab.id}}">{{tab.nome}}</option>
%end
%end
			</select>
            <input type="hidden" id="colunas" name="colunas" value="{{idColunas}}" />
		</div>
            <div class="form-group">
                <label>Tipo</label>
                <div class="form-group row">
                    <div class="radio">
%if tipo == 'I':
                        &nbsp;&nbsp;<label><input type="radio" name="tipo" value="I" checked> Informações&nbsp;&nbsp;</label>
%else:
                        &nbsp;&nbsp;<label><input type="radio" name="tipo" value="I"> Informações&nbsp;&nbsp;</label>
%end
                    </div>
                    <div class="radio">
%if tipo == 'D':
                        &nbsp;&nbsp;<label><input type="radio" name="tipo" value="D" checked> Dados&nbsp;&nbsp;</label>
%else:
                        &nbsp;&nbsp;<label><input type="radio" name="tipo" value="D" > Dados&nbsp;&nbsp;</label>
%end
                    </div>
                </div>
            </div>
        <div class="text-center">
            <input type="submit" class="btn btn-primary" value="Listar Dados" />
        </div>
        </form>
    </div>
</div>
<br>
<script>

    function sel() {
        var id = $('#id').val();
        window.location.href = '/explorar_dados?id=' + id;
    }

    function SelCol() {
        var colunas = '';
        var chks = document.getElementsByName('col');
        for (var i = 0; i < chks.length; i++) {
            if (chks[i].checked == true) {
                if (colunas == '')
                    colunas = chks[i].value;
                else 
                    colunas = colunas + ',' + chks[i].value;
            }
        }
        document.getElementById('colunas').value = colunas;
    }

</script>
%if int(idTabela) != 0:
<div class="row">
    <div class="col-lg-3 ">
        <div class="form-group">
            <div class="checkbox">
%for col in listaColunas:
                <div class="checkbox">
%if col.selecionado == False:
                    <label data-toggle="tooltip" title="{{col.descricao}}"><input type="checkbox" name="col" value="{{col.id}}" onclick="SelCol()"> {{col.titulo}}</label>
%else:
                    <label data-toggle="tooltip" title="{{col.descricao}}"><input type="checkbox" name="col" value="{{col.id}}" onclick="SelCol()" checked> {{col.titulo}}</label>
%end
                </div>
%end
            </div>
        </div>
    </div>
    <div class="col-lg-9">
        {{!grid}}
    </div>
</div>
%end