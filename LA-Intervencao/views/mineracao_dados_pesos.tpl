% rebase('layout.tpl', title='Machine Learning - Pesos', scriptGrafico=scriptGrafico)

<a href="/mineracao_dados?id={{id_tabela}}">Voltar</a>
<div class="card">
    <div class="card-header">{{nome}}</div>
    <div class="card-body">
<table border=1 cellspacin="1" width="100%">
%for peso in pesos:
<tr style="font-weight: bold; background-color:cadetblue">
    <td>{{peso['Campo']}}</td>
    <td>{{peso['Peso']}}</td>    
</tr>
<tr>
    <td colspan="2">
        <table width="100%">
            <tr style="font-weight:bold; ">
                <td>Valor</td>
                <td>Target</td>
                <td>Qtd</td>
                <td>%</td>
                <td>% Valor</td>
                <td>% Relativo</td>
            </tr>
%for val in peso['Valores']:
<tr
%if val['destaca'] == 'S':
    style="color: blue"
%elif val['destaca'] == 'F':
    style="color: red"
%end
    >
    <td>{{val['Valor']}}</td>
    <td>{{val['Classe']}}</td>
    <td>{{val['_qtd']}}</td>
%if val['destaca'] == 'S' or val['destaca'] == 'F':
    <td><b>{{val['_percValor']}}</b></td>
%else:
    <td>{{val['_percValor']}}</td>
%end

    <td>{{val['_perc']}}</td>
    <td>{{val['_percRelativo']}}</td>
</tr>
%end
        </table>
        <table width="100%">
            <tr>
                <td valign="top" style="width: 50%">
                    {{!peso['grfFalha']}}
                </td>
                <td valign="top" style="width: 50%">
                    {{!peso['grfSucesso']}}
                </td>
            </tr>
        </table>
        <br>
    </td>
    
</tr>
%end
</table>
	</div>
</div>
