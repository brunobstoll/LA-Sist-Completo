% rebase('layout.tpl', title='Colunas', listaTabelas=listaTabelas, coluna=coluna, scriptGrafico='')

<div class="card card-register mx-auto mt-5">
    <div class="card-header">Colunas</div>
    <div class="card-body">
	
		<form method="POST" action="/do_md_coluna_def">
			<input type="hidden" name="id" value="{{coluna.id}}">
			<div class="form-group">
				<label for="id_tabela">Tabela</label>
				<select class="form-control" name="id_tabela">
%for tab in listaTabelas:
%if coluna.id_tabela == tab.id:
				<option value="{{tab.id}}" selected>{{tab.nome}}</option>
%else:
				<option value="{{tab.id}}">{{tab.nome}}</option>
%end
%end
				</select>
			</div>
			<div class="form-group">
				<label for="nome">Nome</label>
%if int(coluna.id) != 0:
				<input class="form-control" name="nome" id="nome" type="text" placeholder="Informe o nome" value="{{coluna.nome}}" readonly>
%else:
                <input class="form-control" name="nome" id="nome" type="text" placeholder="Informe o nome" value="{{coluna.nome}}">
%end
			</div>
            <div class="form-group">
                <label for="nome">Tipo</label>
                <select class="form-control" name="tipo">
%for tp in coluna.lstTipos:
%if tp['selecionado'] == True:
                    <option value="{{tp['id']}}" selected>{{tp['nome']}}</option>
%else:
                    <option value="{{tp['id']}}">{{tp['nome']}}</option>
%end
%end
                </select>                
            </div>
			<div class="form-group" >
				<label for="sql">SQL</label>
				<textarea class="form-control" name="sql" id="sql">{{coluna.sql}}</textarea>
			</div>
			<div class="checkbox">
%if coluna.desabilitado == True:
				<label><input type="checkbox" name="desabilitado" checked value="true"> Desabilitar</label>
%else:
				<label><input type="checkbox" name="desabilitado"  value="true"> Desabilitar</label>
%end
			</div>
			<div class="form-group">
				<label for="titulo">Título</label>
				<input class="form-control" name="titulo" id="titulo" type="text" placeholder="Informe o Título" value="{{coluna.titulo}}">
			</div>
			<div class="form-group">
				<label for="descricao">Descrição</label>
				<textarea class="form-control" name="descricao" id="descricao" placeholder="Informe a descrição do campo" rows="3">{{coluna.descricao}}</textarea>
			</div>
            <div class="form-group">
                <label for="sinonimos">Sinonimos</label>
                <textarea class="form-control" name="sinonimos" id="sinonimos" placeholder="Sinonimos separados por vículas" rows="3">{{coluna.sinonimos}}</textarea>
            </div>
			<div class="checkbox">
%if coluna.classe == True:
				<label><input type="checkbox" name="classe" checked> Classe ( na predição - valores nulos serão previstos )</label>
%else:
				<label><input type="checkbox" name="classe"> Classe ( na predião - valores nulos serão previstos )</label>
%end
			</div>
			<div class="form-group">
				<label for="val_aluno_risco">Valores aluno "em risco"</label>
				<input class="form-control" name="val_aluno_risco" id="val_aluno_risco" placeholder="Informe o valor de detectar alunos 'em risco' " value="{{coluna.val_aluno_risco}}"  />
			</div>
			<div class="checkbox">
				<label><input type="checkbox" name="fl_aluno"> Identificação Aluno</label>
			</div>
			<div class="checkbox">
%if coluna.chave_estrangeira == True:
				<label><input type="checkbox" id="chave_estrangeira" name="chave_estrangeira" checked onchange="ChkChaveEstrangeira();"> Chave Estrangeira</label>
%else:
				<label><input type="checkbox" id="chave_estrangeira" name="chave_estrangeira" onchange="ChkChaveEstrangeira()"> Chave Estrangeira</label>
%end
			</div>
			<div class="form-group">
				<label for="id_tabela_fk">Tabela</label>
%if coluna.chave_estrangeira == True:
				<select class="form-control" id="id_tabela_fk" name="id_tabela_fk" onchange="SelecionarTabela();">

%else:
				<select class="form-control" id="id_tabela_fk" name="id_tabela_fk" onchange="SelecionarTabela();" disabled>
%end
					<option value=""></option>
%for tab in listaTabelas:
%if coluna.id_tabela_fk == tab.id:
					<option value="{{tab.id}}" selected>{{tab.nome}}</option>
%else:
					<option value="{{tab.id}}">{{tab.nome}}</option>
%end
%end
				</select>
			</div>
			<div class="form-group">
				<label for="id_coluna_fk">Coluna</label>
%if coluna.chave_estrangeira == False:
				<select class="form-control" id="id_coluna_fk" name="id_coluna_fk" disabled>
%else:
				<select class="form-control" id="id_coluna_fk" name="id_coluna_fk" >
%for colFk in colunasFk:

%if colFk.id == coluna.id_coluna_fk:
					<option value="{{colFk.id}}" selected>{{colFk.nome}}</option>
%else:
					<option value="{{colFk.id}}">{{colFk.nome}}</option>
%end

%end

%end
					
				</select>
			</div>
			<div class="text-center">
				<input type="submit" class="btn btn-primary" value="Salvar" /> <input type="button" value="Cancelar" onclick="window.location.href='/colunas?id={{tab.id}}'" class="btn btn-secondary" />

			</div>
		</form>
	</div>
</div>

<script>

function ChkChaveEstrangeira() {
	var v = $('#chave_estrangeira').is(":checked");
	if ( v ) {
		$('#id_tabela_fk').removeAttr('disabled', '');
		$('#id_coluna_fk').removeAttr('disabled', '');
	} else {
		$('#id_tabela_fk').attr('disabled', '');
		$('#id_coluna_fk').attr('disabled', '');

		$('#id_coluna_fk').find('option').remove();
	}
}

function SelecionarTabela() {
	var iid = $('#id_tabela_fk').val();

	$.getJSON('/tb_colunas_id', { id: iid }, function(lista) {
		$('#id_coluna_fk').find('option').remove();
		$.each(lista, function(key, value) {
			$('#id_coluna_fk').append($('<option></option>').attr('value', value.id).text(value.nome));
		});
      });
}

</script>