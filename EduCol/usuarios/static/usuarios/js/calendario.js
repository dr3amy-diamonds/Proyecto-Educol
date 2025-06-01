const gridDias        = document.getElementById("grid-dias");
const mesActualTexto  = document.getElementById("mes-actual");
const btnPrev         = document.getElementById("prev");
const btnNext         = document.getElementById("next");

let fechaActual = new Date();

const NOMBRES_MESES = [
  "Enero","Febrero","Marzo","Abril","Mayo","Junio",
  "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"
];

// Guarda aquí los eventos del mes actual
let eventosMes = [];

async function cargarEventos() {
  const res = await fetch('/api/eventos/');
  const allEvents = await res.json();
  eventosMes = allEvents.map(evt => {
    // parseamos fechas ISO a Date
    const start = new Date(evt.start);
    // FullCalendar envía end como día siguiente, así que restamos un día
    const end   = evt.end
      ? new Date((new Date(evt.end)).getTime() - 24*60*60*1000)
      : start;
    return { title: evt.title, start, end };
  });
}

function renderCalendario(fecha) {
  gridDias.innerHTML = "";

  const anio = fecha.getFullYear();
  const mes  = fecha.getMonth();

  const primerDia = new Date(anio, mes, 1);
  const ultimoDia = new Date(anio, mes + 1, 0);
  const diasEnMes = ultimoDia.getDate();
  const diaInicio = primerDia.getDay(); // 0=domingo

  mesActualTexto.textContent = `${NOMBRES_MESES[mes]} ${anio}`;

  // Casillas vacías hasta el primer día
  for (let i = 0; i < diaInicio; i++) {
    gridDias.innerHTML += `<div class="empty"></div>`;
  }

  // Render de cada día con data-date
  for (let dia = 1; dia <= diasEnMes; dia++) {
    const yyyy = anio.toString().padStart(4,'0');
    const mm   = (mes + 1).toString().padStart(2,'0');
    const dd   = dia.toString().padStart(2,'0');
    const isoDate = `${yyyy}-${mm}-${dd}`;

    gridDias.innerHTML += `
      <div class="day" data-date="${isoDate}">
        <span class="num">${dia}</span>
      </div>`;
  }

  // Una vez creado el grid, marca los eventos
  marcarEventos();
}

function marcarEventos() {
  // Para cada evento, recorre sus fechas de start a end
  eventosMes.forEach(evt => {
    for (
      let d = new Date(evt.start);
      d <= evt.end;
      d.setDate(d.getDate() + 1)
    ) {
      const iso = d.toISOString().slice(0,10);
      const cell = gridDias.querySelector(`.day[data-date="${iso}"]`);
      if (cell) {
        cell.classList.add('has-event');
        // añade tooltip con el título
        const tip = document.createElement('div');
        tip.className = 'event-tip';
        tip.innerText = evt.title;
        cell.appendChild(tip);
      }
    }
  });
}

// Navegación de meses
btnPrev.addEventListener("click", () => {
  fechaActual.setMonth(fechaActual.getMonth() - 1);
  renderCalendario(fechaActual);
});
btnNext.addEventListener("click", () => {
  fechaActual.setMonth(fechaActual.getMonth() + 1);
  renderCalendario(fechaActual);
});

(async () => {
  // 1) Dibuja inmediatamente el mes (offsets + días)
  renderCalendario(fechaActual);

  // 2) Carga los eventos y márcalos encima del grid ya existente
  try {
    await cargarEventos();
    marcarEventos();  // solo la parte de añadir .has-event y tooltips
  } catch (e) {
    console.error("No se pudieron cargar eventos", e);
  }
})();
