% rebase('layout_black.tpl', title=titulo, scriptGrafico=js)
<style type="text/css">
figure {
  width: auto !important; /*override the width below*/
  width: 100%;
  max-width: 678px;
  clear: both;
}
</style>
<form action="/do_dashboard_pln" method="POST">
    <div class="card-body">
        <div class="form-group row">
            <textarea id='expressao', name='expressao' class="form-control" style='width: 100%; font-size: 13pt' rows="3"  placeholder="Informe a expressão de pergunta">{{expressao}}</textarea>
        </div>
        <div class="text-center">
            <input type="submit" class="btn btn-primary btn-block" value="Processar Expressão"/>
        </div>
    </div>
</form>
{{!html}}


