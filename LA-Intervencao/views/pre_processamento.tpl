% rebase('layout.tpl', title='Pré-Processamento', scriptGrafico=scriptGrafico)

<div class="row">
	<div class="col-lg-6">
		<div class="card card-register mx-auto mb-3"><!--mt-5-->
			<input type="hidden" value="idColuna" name="idColuna" />
			<div class="card-header">Colunas</div>
			<div class="card-body">
				<div class="form-group">
					<label for="nome">Tabela</label>
			<select id="idTabela" name="idTabela" class="form-control" onchange="SelTabela()">
				<option value="0">Selecione uma tabela</option>
%for tab in listaTabelas:
%if tab.selecionado == True:
				<option value="{{tab.id}}" selected>{{tab.nome}}</option>
%else:
				<option value="{{tab.id}}">{{tab.nome}}</option>
%end
%end
			</select>
				</div>
%for coluna in listaColunas:
				<div class="radio">
%if coluna.selecionado == True:
					<label><input type="radio" name="coluna" onclick="SelColuna(this)" value="{{coluna.id}}" checked> {{coluna.nome}}
%else:
					<label><input type="radio" name="coluna" onclick="SelColuna(this)" value="{{coluna.id}}"> {{coluna.nome}}
%end
%if coluna.desabilitado == True:
*
%end
%if coluna.classe == True:
<b>[ CLS ]</b>
%end
</label>

				</div>
%end
                <hr />
                * Desabilitados para ML
				<div class="text-center">
%if idColuna != 0:
					<!-- <input type="submit" class="btn btn-primary btn-block" value="Visualizar" /> -->
					<input type="button" class="btn" value="Discretização"  data-toggle="modal" data-target="#modalDiscr"/>
					<input type="button" class="btn" value="Valores Nulos" />
%end
				</div>
			</div>
		</div>
	</div>
	<div class="col-lg-6">
		{{!grfPizza}}
	</div>
</div>

<script>

function SelTabela() {
	var idTabela = $('#idTabela').val();
	window.location.href = '/pre_processamento?idTabela=' + idTabela;
}

function SelColuna(obj) {
	var idTabela = $('#idTabela').val();
	var idColuna = obj.value;
	window.location.href = '/pre_processamento?idTabela=' + idTabela + '&idColuna=' + idColuna;
}

function consultarQuartil() {
    var qtExcl = $('#qtDist').prop('checked');
    if (qtExcl) {
        qtExcl = 'E';
    } else {
        qtExcl = 'I';
    }
    
    var url = '/gerar_sql_quartil?tabela={{nomeTabela}}&coluna={{nomeColuna}}&tp=' + qtExcl;

    $.get(url, function (data, status) {
        $('#expressao').val(data);
    });
}

</script>


<div class="modal fade" id="modalDiscr" tabindex="-1" role="dialog" aria-labelledby="modalDiscrLabel" aria-hidden="true">
    <div class="modal-dialog" role="document" >
        <div class="modal-content" style="width: 850px;">
		<form method="POST" action="/do_pre_proc_discr">
			<input type="hidden" id="idColuna" name="idColuna" value="{{idColuna}}" />
			<input type="hidden" id="idTabela" name="idTabela" value="{{idTabela}}" />
            <div class="modal-header">
                <h5 class="modal-title" id="modalDiscrLabel">Deseja Discretizar coluna?</h5>
                <button class="close" type="button" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">x</span>
                </button>
            </div>
            <div class="modal-body">
				<div class="form-group">
					<label for="nome">Nome</label>
					<input type="text" id="nome" name="nome" class="form-control" value="{{nomeColuna}}" readonly  />
				</div>
				<div class="form-group">
					<label for="descricao">Expressão</label>
					<textarea class="form-control" name="expressao" id="expressao" placeholder="Informe a expressão" rows="3">{{sql}}</textarea>
                    <input type="checkbox" id="qtDist" checked />Quartil.Excl [ <a href="#" onclick="consultarQuartil()">Quartil</a> ]
				</div>
			</div>
            <div class="modal-footer">
                <button class="btn btn-secondary" type="button" data-dismiss="modal">Cancel</button>
                <input type="submit" class="btn btn-primary" value="Enviar" />
            </div>
        </form>
        </div>
    </div>
</div>