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

<body class="bg-dark" id="page-top">
    <!-- Navigation
        <a class="navbar-brand" href="/homeAnalista">LA :: Analista</a>
    -->
    <div class="content" style="background-color: #fff">
        <div class="container-fluid">
            <!--
            <ol class="breadcrumb">
				<li class="breadcrumb-item active">{{title}}</li>
			</ol>
            -->
			{{!base}}
        </div>
        <!-- /.container-fluid-->
        <!-- /.content-wrapper-->
        
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
