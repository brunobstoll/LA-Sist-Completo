<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">
    <title>{{title}}</title>
    <!-- Bootstrap core CSS-->
    <link href="static/bootstrap/css/bootstrap.min.css" rel="stylesheet">
    <!-- Custom fonts for this template-->
    <link href="static/font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css">
    <!-- Page level plugin CSS-->
    <link href="static/datatables/dataTables.bootstrap4.css" rel="stylesheet">
    <!-- Custom styles for this template-->
    <link href="static/css/sb-admin.css" rel="stylesheet">
</head>

<body class="fixed-nav sticky-footer bg-dark" id="page-top">
    <!-- Navigation-->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top" id="mainNav">
        <a class="navbar-brand" href="/homeProfessor">Learning Analytis - Área do Professor</a>
        <button class="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarResponsive">
            <!-- menu lateral -->
            <ul class="navbar-nav navbar-sidenav" id="exampleAccordion">
                <li class="nav-item" data-toggle="tooltip" data-placement="right" title="Importação">
                    <a class="nav-link" href="/recomendacao_professor">
                        <i class="fa fa-fw fa-line-chart"></i>
                        <span class="nav-link-text">Recomendações</span>
                    </a>
                </li>

               <!--menuPainel-->

                

                <li class="nav-item" data-toggle="tooltip" data-placement="right" title="Alunos">
                    <a class="nav-link" href="/profAlunos">
                        <i class="fa fa-fw fa-group"></i>
                        <span class="nav-link-text">Alunos</span>
                    </a>
                </li>
                
			</ul>
            <!-- esconder menu lateral -->
            <ul class="navbar-nav sidenav-toggler" >
                <li class="nav-item">
                    <a class="nav-link" id="sidenavToggler">
                        <i class="fa fa-fw fa-bars"></i> <!-- fa-bars fa-angle-left -->
                    </a>
                </li>
            </ul>
            <!-- menu do topo -->
            <ul class="navbar-nav ml-auto">
                <li class="nav-item">
                    <a class="nav-link" data-toggle="modal" data-target="#exampleModal">
                        <i class="fa fa-fw fa-sign-out"></i>Sair</a>
                </li>
            </ul>
        </div>
    </nav>
    <div class="content-wrapper">
        <div class="container-fluid">
            <ol class="breadcrumb">
				<li class="breadcrumb-item active">{{title}}</li>
			</ol>
			{{!base}}
        </div>
        <!-- /.container-fluid-->
        <!-- /.content-wrapper-->
        <footer class="sticky-footer">
            <div class="container">
                <div class="text-center">
                    <small>© LA - Intervensão [ 2018 ]</small>
                </div>
            </div>
        </footer>
        <!-- Scroll to Top Button-->
        <a class="scroll-to-top rounded" href="#page-top">
            <i class="fa fa-angle-up"></i>
        </a>
        <!-- Logout Modal-->
        <div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel">Confirme</h5>
                        <button class="close" type="button" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">×</span>
                        </button>
                    </div>
                    <div class="modal-body">Deseja sair do sistema?</div>
                    <div class="modal-footer">
                        <button class="btn btn-secondary" type="button" data-dismiss="modal">Cancelar</button>
                        <a class="btn btn-primary" href="/login">Sair</a>
                    </div>
                </div>
            </div>
        </div>
        <!-- Bootstrap core JavaScript-->
        <script src="static/jquery/jquery.min.js"></script>
        <script src="static/bootstrap/js/bootstrap.bundle.min.js"></script>
        <!-- Core plugin JavaScript-->
        <script src="static/jquery-easing/jquery.easing.min.js"></script>
        <!-- Page level plugin JavaScript-->
        <script src="static/chart.js/Chart.min.js"></script>
        <script src="static/datatables/jquery.dataTables.js"></script>
        <script src="static/datatables/dataTables.bootstrap4.js"></script>
        <!-- Custom scripts for all pages-->
        <script src="static/js/sb-admin.min.js"></script>
        <!-- Custom scripts for this page-->
        <script src="static/js/sb-admin-datatables.min.js"></script>
        <script src="static/js/sb-admin-charts.min.js"></script>
        <script src="static/treeView/bootstrap-treeview.js"></script>
        <script type="text/javascript" src="https://public.tableau.com/javascripts/api/tableau-2.min.js"></script>
        <script type="text/javascript">
            function initViz(UrlRpt, divRpt) {
                var containerDiv = document.getElementById(divRpt);
                var options = {
                    hideTabs: true,
                    onFirstInteractive: function () {
                        console.log("Run this code when the viz has finished loading.");
                    }
                };

                // Create a viz object and embed it in the container div.
                var viz = new tableau.Viz(containerDiv, UrlRpt, options);
            }
        </script>



%if scriptGrafico != None:
	{{!scriptGrafico}}
%end
    </div>

<script>
$(document).ready(function () {
    $('[data-toggle="tooltip"]').tooltip();
    $.getJSON('/painel_professor_lista', function (lista) {
        var menuPainel = '';
        for (var i=0; i < lista.length; i++) {
            obj = lista[i];
            menuPainel = menuPainel + '<li class="nav-item" data-toggle="tooltip" data-placement="right" title="Painel">' +
                '<a class="nav-link" href="/painel_professor_vw?id=' + obj.id + '">' +
                '<i class="fa fa-fw fa-search"></i>' +
                '<span class="nav-link-text">' + obj.nome + '</span>' +
                '</a>' +
                '</li>';
        }

        var menuHtml = $('#exampleAccordion').html();
        menuHtml = menuHtml.replace('<!--menuPainel-->', menuPainel)


        $('#exampleAccordion').html(menuHtml);
    });
    
});


</script>
</body>

</html>
