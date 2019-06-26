% rebase('layout.tpl', title='Visão', scriptGrafico='')
<div class="card mb-3">
    <!-- <i class="fa fa-table"></i> Data Table Example</div> -->
    <div class="card-body">
        <div class="form-group">
            <label for="nome">Tabela</label>
            <select id="id" class="form-control" onchange="sel(this)">
                <option value="">Selecione uma tabela</option>
%for tab in listaTabelas:
%if tab.selecionado == True:
                <option value="{{tab.id}}" selected>{{tab.nome}}</option>
%else:
                <option value="{{tab.id}}">{{tab.nome}}</option>
%end
%end
            </select>
        </div>
        <div class="text-center">
            <input type="button" value="Adicionar" onclick="Adicionar()" class="btn" />
        </div>
    </div>
</div>
<br>
<script>

function Adicionar() {
    var id_tabela = $('#id').val();

    if (id_tabela == '') {
        alert('Informe a tabela');
    } else {
        window.location.href = '/defvisao?id_tabela=' + id_tabela + '&id=0'
    }

}
function sel() {
	var id = $('#id').val();
	window.location.href = '/visao?id=' + id;
}

</script>
{{!grid}}
<br />