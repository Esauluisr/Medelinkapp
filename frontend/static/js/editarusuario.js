//change password
function habilitarBotones() {
  document.getElementById("btnpassword").disabled = false;
  document.getElementById("btnconfirmarpassword").disabled = false;
}

function desactivarBotones() {
  document.getElementById("btnnombre").disabled = true;
  document.getElementById("btnemail").disabled = true;
  document.getElementById("btnpassword").disabled = true;
  document.getElementById("btnconfirmarpassword").disabled = true;
}

//edit user
function habilitarCampos() {
  document.getElementById("nombreuser").disabled = false;
  document.getElementById("apellidouser").disabled = false;
  document.getElementById("emailuser").disabled = false;
  document.getElementById("telefonouser").disabled = false;
  document.getElementById("edaduser").disabled = false;
}
function desactivarCampos() {
  document.getElementById("nombreuser").disabled = true;
  document.getElementById("apellidouser").disabled = true;
  document.getElementById("emailuser").disabled = true;
  document.getElementById("telefonouser").disabled = true;
  document.getElementById("edaduser").disabled = true;
}
