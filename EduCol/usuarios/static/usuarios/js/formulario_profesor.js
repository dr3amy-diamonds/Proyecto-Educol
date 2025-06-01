document.addEventListener("DOMContentLoaded", function () {
  const paginas = document.querySelectorAll(".pagina");
  const anteriorBtn = document.getElementById("anteriorBtn");
  const siguienteBtn = document.getElementById("siguienteBtn");
  const submitBtn = document.getElementById("submitBtn");
  const formulario = document.getElementById("formularioProfesor");
  const toast = document.getElementById("toast");

  let paginaActual = 0;

  function mostrarPagina(index) {
    paginas.forEach((p, i) => (p.style.display = i === index ? "block" : "none"));
    anteriorBtn.style.display = index > 0 ? "inline-block" : "none";
    siguienteBtn.style.display = index < paginas.length - 1 ? "inline-block" : "none";
    submitBtn.style.display = index === paginas.length - 1 ? "inline-block" : "none";
  }

  anteriorBtn.addEventListener("click", function () {
    if (paginaActual > 0) paginaActual--;
    mostrarPagina(paginaActual);
  });

  siguienteBtn.addEventListener("click", function () {
    if (paginaActual < paginas.length - 1) paginaActual++;
    mostrarPagina(paginaActual);
  });

  formulario.addEventListener("submit", function (event) {
    if (!formulario.checkValidity()) {
      event.preventDefault(); // Evita el envío
      mostrarToast("Por favor, complete todos los campos obligatorios.");
    }
  });

  function mostrarToast(mensaje) {
    toast.textContent = mensaje;
    toast.classList.remove("toast-hidden");
    toast.classList.add("toast-visible");

    setTimeout(() => {
      toast.classList.remove("toast-visible");
      toast.classList.add("toast-hidden");
    }, 3000);
  }

  mostrarPagina(paginaActual);
});
