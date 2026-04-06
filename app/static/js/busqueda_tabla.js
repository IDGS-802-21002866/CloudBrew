/**
 * busqueda_tabla.js
 * Búsqueda genérica en tablas. Usado en todos los módulos con listar.html.
 *
 * Uso en el template:
 *   <input data-busqueda-tabla="idDeLaTabla" data-busqueda-col="col-nombre" ...>
 *
 *   data-busqueda-tabla : id del elemento <table>
 *   data-busqueda-col   : clase CSS de la columna por la que se busca (default: col-nombre)
 */
document.addEventListener("DOMContentLoaded", function () {
  const input = document.querySelector("[data-busqueda-tabla]");
  if (!input) return;

  const tablaId = input.dataset.busquedaTabla;
  const colClass = input.dataset.busquedaCol || "col-nombre";

  input.addEventListener("keyup", function () {
    const busqueda = this.value.toLowerCase();
    const filas = document.querySelectorAll(`#${tablaId} tbody tr`);

    filas.forEach((fila) => {
      const col = fila.querySelector(`.${colClass}`);
      if (col) {
        fila.style.display = col.textContent.toLowerCase().includes(busqueda)
          ? ""
          : "none";
      }
    });
  });
});
