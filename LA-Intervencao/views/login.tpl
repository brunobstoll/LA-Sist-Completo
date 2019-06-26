<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">
    <title>LA - Login</title>
    <!-- Bootstrap core CSS-->
    <link href="static/bootstrap/css/bootstrap.min.css" rel="stylesheet">
    <!-- Custom fonts for this template-->
    <link href="static/font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css">
    <!-- Custom styles for this template-->
    <link href="static/css/sb-admin.css" rel="stylesheet">
</head>

<body class="bg-dark">
    <div class="container">
        <div class="card card-login mx-auto mt-5">
            <div class="card-header">Login</div>
            <div class="card-body">
                <form action="/do_login" method="POST">
                    <div class="form-group">
                        <label for="login">Usuário</label>
                        <input class="form-control" id="login" name="login" type="text" aria-describedby="emailHelp" placeholder="Informe login ou email">
                    </div>
                    <div class="form-group">
                        <label for="senha">Senha</label>
                        <input class="form-control" id="senha" name="senha" type="password" placeholder="Entre com a senha">
                    </div>
                    <!--<div class="form-group">
                        <div class="form-check">
                            <label class="form-check-label">
                                <input class="form-check-input" type="checkbox">
                                Lembrar da senha</label>
                        </div>
                    </div>-->

                    <input type="submit" class="btn btn-primary btn-block" value="Entrar" />
                </form>
                <!--
                <div class="text-center">
                    <a class="d-block small" href="#">Esqueceu a senha?</a>
                </div>
                -->
%if msg != '':
                <div class="alert alert-danger">
                    <strong>Atenção</strong> {{msg}}
                </div>
%end
            </div>
        </div>
    </div>
    <!-- Bootstrap core JavaScript-->
    <script src="static/jquery/jquery.min.js"></script>
    <script src="static/bootstrap/js/bootstrap.bundle.min.js"></script>
    <!-- Core plugin JavaScript-->
    <script src="static/jquery-easing/jquery.easing.min.js"></script>
</body>

</html>
