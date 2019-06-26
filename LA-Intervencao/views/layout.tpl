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
        <a class="navbar-brand" href="/homeAnalista">LA :: Analista</a>
        <button class="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarResponsive">
            <!-- menu lateral -->
            <ul class="navbar-nav navbar-sidenav" id="exampleAccordion">
                <li class="nav-item" data-toggle="tooltip" data-placement="right" title="Importação">
                    <a class="nav-link" href="importacao">
                        <i class="fa fa-fw fa-database"></i>
                        <span class="nav-link-text">Importação</span>
                    </a>
                </li>
                <li class="nav-item" data-toggle="tooltip" data-placement="right" title="Metadados">
                    <a class="nav-link" href="colunas">
                        <i class="fa fa-fw fa-table"></i>
                        <span class="nav-link-text">Metadados</span>
                    </a>
                </li>
                <li class="nav-item" data-toggle="tooltip" data-placement="right" title="Pré-Processamento">
                    <a class="nav-link" href="pre_processamento">
                        <i class="fa fa-fw fa-cube"></i>
                        <span class="nav-link-text">Pré-Processamento</span>
                    </a>
                </li>
                <li class="nav-item" data-toggle="tooltip" data-placement="right" title="Transformação">
                    <a class="nav-link" href="transformacao">
                        <i class="fa fa-fw fa-random"></i>
                        <span class="nav-link-text">Transformação</span>
                    </a>
                </li>
                <li class="nav-item" data-toggle="tooltip" data-placement="right" title="Data Mining">
                    <a class="nav-link" href="mineracao_dados">
                        <i class="fa fa-fw fa-flask"></i>
                        <span class="nav-link-text">Machine Learning</span>
                    </a>
                </li>
                <li class="nav-item" data-toggle="tooltip" data-placement="right" title="Data Mining">
                    <a class="nav-link" href="explorar_dados">
                        <i class="fa fa-fw fa-search"></i>
                        <span class="nav-link-text">Explorar Dados</span>
                    </a>
                </li>
                <li class="nav-item" data-toggle="tooltip" data-placement="right" title="Visões">
                    <a class="nav-link" href="visao">
                        <i class="fa fa-fw fa-area-chart"></i>
                        <span class="nav-link-text">Visões</span>
                    </a>
                </li>
                <li class="nav-item" data-toggle="tooltip" data-placement="right" title="Link">
                    <a class="nav-link" href="dashboard">
                        <i class="fa fa-fw fa-pie-chart"></i>
                        <span class="nav-link-text">Dashboard</span>
                    </a>
                </li>
			</ul>
            <!-- esconder menu lateral -->
            <ul class="navbar-nav sidenav-toggler" style="background-colo2r: black;">
                <li class="nav-item">
                    <a class="nav-link" id="sidenavToggler">
                        <i class="fa fa-fw fa-bars"></i> <!-- fa-bars fa-angle-left -->
                    </a>
                </li>
            </ul>
            <!-- menu do topo -->
            <ul class="navbar-nav ml-auto">
                <li class="nav-item "><!-- dropdown-->
                    <a class="nav-link dropdown-toggle mr-lg-2" id="messagesDropdown2" href="/usuario">
                        <i class="fa fa-fw fa-group"></i>
                    </a>
                    <div class="dropdown-menu" aria-labelledby="messagesDropdown" style="display: none">
                        <h6 class="dropdown-header">New Messages:</h6>
                        <div class="dropdown-divider"></div>
                        <a class="dropdown-item" href="#">
                            <strong>David Miller</strong>
                            <span class="small float-right text-muted">11:21 AM</span>
                            <div class="dropdown-message small">Hey there! This new version of SB Admin is pretty awesome! These messages clip off when they reach the end of the box so they don't overflow over to the sides!</div>
                        </a>
                        <div class="dropdown-divider"></div>
                        <a class="dropdown-item" href="#">
                            <strong>Jane Smith</strong>
                            <span class="small float-right text-muted">11:21 AM</span>
                            <div class="dropdown-message small">I was wondering if you could meet for an appointment at 3:00 instead of 4:00. Thanks!</div>
                        </a>
                        <div class="dropdown-divider"></div>
                        <a class="dropdown-item" href="#">
                            <strong>John Doe</strong>
                            <span class="small float-right text-muted">11:21 AM</span>
                            <div class="dropdown-message small">I've sent the final files over to you for review. When you're able to sign off of them let me know and we can discuss distribution.</div>
                        </a>
                        <div class="dropdown-divider"></div>
                        <a class="dropdown-item small" href="#">View all messages</a>
                    </div>
                </li>
                <li class="nav-item dropdown" style="display: none">
                    <a class="nav-link dropdown-toggle mr-lg-2" id="alertsDropdown" href="#" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        <i class="fa fa-fw fa-bell"></i>
                        <span class="d-lg-none">Alerts

                            <span class="badge badge-pill badge-warning">6 New</span>
                        </span>
                        <span class="indicator text-warning d-none d-lg-block">
                            <i class="fa fa-fw fa-circle"></i>
                        </span>
                    </a>
                    <div class="dropdown-menu" aria-labelledby="alertsDropdown">
                        <h6 class="dropdown-header">New Alerts:</h6>
                        <div class="dropdown-divider"></div>
                        <a class="dropdown-item" href="#">
                            <span class="text-success">
                                <strong>
                                    <i class="fa fa-long-arrow-up fa-fw"></i>Status Update</strong>
                            </span>
                            <span class="small float-right text-muted">11:21 AM</span>
                            <div class="dropdown-message small">This is an automated server response message. All systems are online.</div>
                        </a>
                        <div class="dropdown-divider"></div>
                        <a class="dropdown-item" href="#">
                            <span class="text-danger">
                                <strong>
                                    <i class="fa fa-long-arrow-down fa-fw"></i>Status Update</strong>
                            </span>
                            <span class="small float-right text-muted">11:21 AM</span>
                            <div class="dropdown-message small">This is an automated server response message. All systems are online.</div>
                        </a>
                        <div class="dropdown-divider"></div>
                        <a class="dropdown-item" href="#">
                            <span class="text-success">
                                <strong>
                                    <i class="fa fa-long-arrow-up fa-fw"></i>Status Update</strong>
                            </span>
                            <span class="small float-right text-muted">11:21 AM</span>
                            <div class="dropdown-message small">This is an automated server response message. All systems are online.</div>
                        </a>
                        <div class="dropdown-divider"></div>
                        <a class="dropdown-item small" href="#">View all alerts</a>
                    </div>
                </li>
                <li class="nav-item" style="display: none;">
                    <form class="form-inline my-2 my-lg-0 mr-lg-2">
                        <div class="input-group">
                            <input class="form-control" type="text" placeholder="Search for...">
                            <span class="input-group-btn">
                                <button class="btn btn-primary" type="button">
                                    <i class="fa fa-search"></i>
                                </button>
                            </span>
                        </div>
                    </form>
                </li>
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
});
</script>
</body>

</html>
