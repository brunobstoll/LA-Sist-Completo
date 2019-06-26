% rebase('layout.tpl', title='Importação', scriptGrafico='')

<div class="card card-register mx-auto mt-5">
    <div class="card-header">Data Sources</div>
    <div class="card-body">
		<form method="post" action="/do_importacao" enctype="multipart/form-data">
			<input type="hidden" id="id" name="id" value="0" />
			<div class="form-group">
				<label>Tipo</label>
			</div>
			<div class="form-group row ">
				<div class="radio">
					&nbsp;&nbsp;<label><input type="radio" name="tipo" value="C" onclick="MudarTipo()"> CSV&nbsp;&nbsp;</label>
				</div>
                <div class="radio">
                    <label><input type="radio" name="tipo" value="J"  onclick="MudarTipo()"> JSON&nbsp;&nbsp;</label>
                </div>
				<div class="radio">
					<label><input type="radio" name="tipo" value="B"  onclick="MudarTipo()"> Banco de Dados&nbsp;&nbsp;</label>
				</div>
				<div class="radio">
					<label><input type="radio" name="tipo" value="T"  onclick="MudarTipo()" disable> Texto</label>
				</div>
			</div>
			<div class="form-group">
				<label for="nome">Nome</label>
				<input class="form-control" name="nome" id="nome" type="text" placeholder="Informe o nome">
			</div>
			<div class="form-group" id="dvValorFonteVAL" style="display: none">
				<label for="valor">Valor</label>
				<input class="form-control" name="valor" id="valor" type="text" placeholder="Informe o valor">
			</div>
			<div class="form-group" id="dvValorFonteARQ" style="display: block">
				<label for="valor">Valor</label>
				<input class="form-control" name="arquivo" id="arquivo" type="file" placeholder="Informe o valor">
			</div>
			<div class="text-center">
				<input type="submit" class="btn btn-primary btn-block" value="Salvar" />
			</div>
		</form>
	</div>
</div>
<br>
<script type="text/javascript">
function Editar(iid) {
	$.getJSON('/importacao_id', { id: iid }, function(obj) {
        $("#id").val(obj.id);
        $("input[name='tipo'][value='" + obj.tipo + "']").prop('checked', true);
        $("#nome").val(obj.nome);
        $("#valor").val(obj.valor);
    });

    MudarTipo();
}
function MudarTipo() {
    if ($("input[name='tipo']:checked").val() == 'J' || $("input[name='tipo']:checked").val() == 'C') {
        $("#dvValorFonteARQ").css("display", "block");
        $("#dvValorFonteVAL").css("display", "none");
    } else {
        $("#dvValorFonteARQ").css("display", "none");
        $("#dvValorFonteVAL").css("display", "block");
    }
}
</script>
{{!grid}}
