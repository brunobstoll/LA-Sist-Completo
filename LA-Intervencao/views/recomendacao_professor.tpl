% rebase('layoutProfessor.tpl', title='Machine Learning - Recomendações', scriptGrafico='')

<a href="/homeProfessor">Voltar</a>
<h3>Recomendações aos Alunos</h3>
<hr />
<div class="row">
	<div class="col-lg-4">
        <div class="card card-register mx-auto mb-3"><!--mt-5-->
			<div class="card-header">Alunos</div>
			<div class="card-body">
				<div class="form-group">
%for aluno in listaAlunos:
<div class="radio">
%if aluno.selecionado == True:
    <label><input type="radio" name="aluno" onclick="SelAluno(this)" value="{{aluno.id}}" checked> {{aluno.nome}}</label>
%else:
    <label><input type="radio" name="aluno" onclick="SelAluno(this)" value="{{aluno.id}}"> {{aluno.nome}}</label>
%end
</div>
%end
                </div>
            </div>
        </div>
    </div>
    <div class="col-lg-8">
%if nomeAluno != '':
        <div class="card card-register mx-auto mb-3">
%if len(listaMensanges) != 0:
            <form action="\do_recomendacao_professor" method="POST">
            <input type="hidden" name="id_aluno" value="{{id_aluno}}" />
            <div class="card-header">Caro aluno, <b>{{nomeAluno}}</b>. Você foi classificado "em risco" por um sistema de previsão com uma taxa de acerto de <i>{{tx_acerto}}%</i> </div>
            <div class="card-body">
%for msg in listaMensanges:
                <input type="hidden" name="msg_id_{{msg.id}}" value="{{msg.id}}" {{msg.attHtml['checked']}} />
                <p class="form-group">
                    <b><input type="checkbox" onchange="fnIgnorarMsg({{msg.id}}, this)" name="ignorarMsg_{{msg.id}}" /> Ignorar</b>
                    <textarea class="form-control" id="msg_{{msg.id}}" name="msg_{{msg.id}}"  {{msg.attHtml['disabled']}} >{{msg.descricao}}</textarea>
                </p>
                <hr  style="margin: 0px;" />
%end
                <!--
                <p class="form-group">
                    <b>Nota do professor</b><br />
                    <div class="form-control">
A combinação desses comportamentos poderá não 
te levar ao sucesso acadêmico.
</div>
                </p>
                -->
                <div class="text-center">
                    <input type="submit" class="btn btn-primary btn-block" value="Enviar recomendação" /> 
                </div>
            </div>
            </form>
%else:
            <div class="card-header">O aluno <b>{{nomeAluno}}</b> foi classificado "sem risco" acadêmico por um sistema de previsão com uma taxa de acerto de <i>{{tx_acerto}}%</i> </div>
            <div class="card-body">
                Classificação de sucesso acadêmico!
            </div>
%end
        </div>
%end
        
    </div>
</div>

<script>
function SelAluno(obj) {
    var id_aluno = obj.value;
    window.location.href = '/recomendacao_professor?id=' + id_aluno;
}
function fnIgnorarMsg(id, objchk) {
    var idObj = 'msg_' + id.toString();
    if (objchk.checked) {
        $('#' + idObj).attr("disabled", "disabled");
    } else {
        $('#' + idObj).removeAttr("disabled");
    }
}
</script>