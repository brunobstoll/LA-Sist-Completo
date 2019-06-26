% rebase('layout.tpl', title='Machine Learning - Recomenda��es', scriptGrafico='')

<a href="/mineracao_dados?id={{tabela.id}}">Voltar</a>
<h3>Recomenda��es :: {{tabela.nome}}</h3>
<hr />


%for aluno in lista:
<div class="card card-register mx-auto mt-5">
    <div class="card-header">Caro aluno, <b>{{aluno['nome']}}</b>. Voc� foi classificado "em risco" por um sistema de previs�o com uma taxa de acerto de <i>{{tx_acerto}}%</i> </div>
    <div class="card-body">
%for msg in aluno['MsgsAluno']:
<hr />
<p>
    <pre>{{msg.descricao}}</pre>
</p>
%end    
        
    </div>
</div>
%end
