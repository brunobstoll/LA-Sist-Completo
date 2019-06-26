% rebase('layout.tpl', title='Machine Learning - Recomendações', scriptGrafico='')

<a href="/mineracao_dados?id={{tabela.id}}">Voltar</a>
<h3>Recomendações :: {{tabela.nome}}</h3>
<hr />


%for aluno in lista:
<div class="card card-register mx-auto mt-5">
    <div class="card-header">Caro aluno, <b>{{aluno['nome']}}</b>. Você foi classificado "em risco" por um sistema de previsão com uma taxa de acerto de <i>{{tx_acerto}}%</i> </div>
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
