const uploadForm = document.getElementById("uploadForm");
const fileInput = document.getElementById("fileInput");
const errorAlert = document.getElementById("errorAlert");

uploadForm.addEventListener("submit", (event) => {
  const file = fileInput.files[0];
  if (file && file.type !== "image/jpg") {
    event.preventDefault(); // Detener el envío del formulario
    errorAlert.style.display = "block"; // Mostrar el aviso de error
  } else {
    errorAlert.style.display = "none"; // Ocultar el aviso de error si es válido
  }
});
