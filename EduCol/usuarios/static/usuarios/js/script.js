function mostrarSeccion(seccionId) {
    // Ocultar todas las secciones
    const secciones = document.querySelectorAll('.seccion');
    secciones.forEach(seccion => {
        seccion.classList.remove('activa');
    });

    // Mostrar la sección seleccionada
    const seccionActiva = document.getElementById(seccionId);
    if (seccionActiva) {
        seccionActiva.classList.add('activa');
    }
}
