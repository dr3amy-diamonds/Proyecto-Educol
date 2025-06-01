const API_KEY = "AIzaSyDkIqNBcKryUzvv1WZqhrbr8i6V7DtKezY";
const CONTENEDOR = document.querySelector(".Contenedor_Principal");
const BOTONES = document.querySelectorAll(".Categorias button");
const BTN_ANTERIOR = document.getElementById("btn-anterior");
const BTN_SIGUIENTE = document.getElementById("btn-siguiente");
const PAGINA_ACTUAL = document.getElementById("pagina-actual");
const PAGINA_TOTAL = document.getElementById("pagina-total");

let pagina = 1;
let videosPorPagina = 4;
let resultados = [];

BOTONES.forEach((boton) => {
    boton.addEventListener("click", async () => {
        const query = boton.getAttribute("data-query");
        pagina = 1;
        resultados = await buscarVideos(query);
        actualizarPaginacion();
        mostrarVideos();
    });
});

BTN_ANTERIOR.addEventListener("click", () => {
    if (pagina > 1) {
        pagina--;
        mostrarVideos();
        actualizarPaginacion();
    }
});

BTN_SIGUIENTE.addEventListener("click", () => {
    const totalPaginas = Math.ceil(resultados.length / videosPorPagina);
    if (pagina < totalPaginas) {
        pagina++;
        mostrarVideos();
        actualizarPaginacion();
    }
});

async function buscarVideos(query) {
    const url = `https://www.googleapis.com/youtube/v3/search?key=${API_KEY}&q=${query}&part=snippet&type=video&maxResults=20`;
    const response = await fetch(url);
    const data = await response.json();
    return data.items;
}

function mostrarVideos() {
    CONTENEDOR.innerHTML = "";
    const inicio = (pagina - 1) * videosPorPagina;
    const fin = inicio + videosPorPagina;
    const videosPagina = resultados.slice(inicio, fin);

    videosPagina.forEach((item) => {
        const videoId = item.id.videoId;
        const video = document.createElement("iframe");
        video.src = `https://www.youtube.com/embed/${videoId}`;
        video.width = "400";
        video.height = "215";
        video.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
        video.allowFullscreen = true;
        CONTENEDOR.appendChild(video);
    });
}

function actualizarPaginacion() {
    const totalPaginas = Math.ceil(resultados.length / videosPorPagina);
    PAGINA_ACTUAL.textContent = pagina;
    PAGINA_TOTAL.textContent = totalPaginas;
    BTN_ANTERIOR.disabled = pagina === 1;
    BTN_SIGUIENTE.disabled = pagina === totalPaginas || totalPaginas === 0;
}
