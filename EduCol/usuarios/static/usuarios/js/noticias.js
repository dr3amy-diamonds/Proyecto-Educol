/// static/usuarios/js/noticias.js

const API_KEY = "4d354dc1289a41e99fa29f4b38f622f9";
const query = encodeURIComponent("education OR school OR university OR students OR teachers");
const API_URL = `https://api.worldnewsapi.com/search-news?text=${query}&language=es&number=30&api-key=${API_KEY}`;

let noticias = [];
let paginaActual = 1;
const noticiasPorPagina = 6;

// Formatea fecha a DD/MM/YYYY
function formatearFecha(fechaISO) {
  const fecha = new Date(fechaISO);
  return `${fecha.getDate().toString().padStart(2,'0')}/` +
         `${(fecha.getMonth()+1).toString().padStart(2,'0')}/` +
         `${fecha.getFullYear()}`;
}

// Renderiza únicamente las .noticia dentro del #noticias-container
function renderizarNoticias(pagina) {
  const contenedor = document.getElementById("noticias-container");
  contenedor.innerHTML = "";

  const inicio = (pagina - 1) * noticiasPorPagina;
  const fin    = inicio + noticiasPorPagina;
  const slice  = noticias.slice(inicio, fin);

  if (!slice.length) {
    contenedor.innerHTML = "<p>No se encontraron noticias educativas.</p>";
    return;
  }

  // Genera cada tarjeta .noticia directamente en el contenedor
  slice.forEach(noticia => {
    const fechaPubli = noticia.publish_date
      ? formatearFecha(noticia.publish_date)
      : "Fecha no disponible";

    const tarjeta = document.createElement("div");
    tarjeta.className = "noticia";
    tarjeta.innerHTML = `
      <img src="${noticia.image || '/static/usuarios/images/placeholder.png'}"
           alt="Imagen de noticia"
           onerror="this.src='/static/usuarios/images/placeholder.png';">
      <h2>${noticia.title}</h2>
      <p>${noticia.text
        ? noticia.text.substring(0, 100) + '...'
        : 'Sin descripción disponible.'}</p>
      <p><strong>Fuente:</strong> ${noticia.source || 'No disponible'}</p>
      <p><strong>Autor:</strong> ${noticia.author || 'Desconocido'}</p>
      <p><strong>Fecha:</strong> ${fechaPubli}</p>
      <a href="${noticia.url}" target="_blank" rel="noopener noreferrer">
        Leer más
      </a>
    `;
    contenedor.appendChild(tarjeta);
  });

  renderizarPaginacion();
}

// Botones de paginación
function renderizarPaginacion() {
  const paginacion = document.getElementById("paginacion");
  paginacion.innerHTML = "";

  const total = Math.ceil(noticias.length / noticiasPorPagina);
  for (let i = 1; i <= total; i++) {
    const btn = document.createElement("button");
    btn.textContent = i;
    if (i === paginaActual) btn.classList.add("active");
    btn.addEventListener("click", () => {
      paginaActual = i;
      renderizarNoticias(paginaActual);
    });
    paginacion.appendChild(btn);
  }
}

// Carga y arranca
async function cargarNoticias() {
  try {
    const res = await fetch(API_URL);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    noticias = data.news || data.articles || data.results || [];
    renderizarNoticias(paginaActual);
  } catch (e) {
    console.error(e);
    document.getElementById("noticias-container").innerHTML =
      `<p>No se pudieron cargar las noticias. ${e.message}</p>`;
  }
}

document.addEventListener("DOMContentLoaded", cargarNoticias);
