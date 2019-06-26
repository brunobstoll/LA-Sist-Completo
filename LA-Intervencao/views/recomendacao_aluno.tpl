% rebase('layoutEstudante.tpl', title='Machine Learning - Recomendações', scriptGrafico='')

<a href="/homeEstudante">Voltar</a>
<h3>Recomendações aos Alunos</h3>
<hr />
<div class="row">
	<div class="col-lg-12">
%if nomeAluno != '':
        <div class="card card-register mx-auto mb-3">
%if len(listaMensanges) != 0:
            <input type="hidden" name="id_aluno" value="{{id_aluno}}" />
            <div class="card-header">Caro aluno, <b>{{nomeAluno}}</b>. Você foi classificado "em risco" por um sistema de previsão com uma taxa de acerto de <i>{{tx_acerto}}%</i> </div>
            <div class="card-body">
%for msg in listaMensanges:
%if msg.descartado != 'S':
                <p class="form-group" style="margin: 0px;">
                    <div class="form-control" id="msg_{{msg.id}}" name="msg_{{msg.id}}" >{{msg.descricao}}</div>
                </p>
%end
%end
                
            </div>
            
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