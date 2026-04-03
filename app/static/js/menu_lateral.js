document.addEventListener("DOMContentLoaded", function () {
  const btnMenu = document.getElementById("btn-menu");
  const btnCerrarMenu = document.getElementById("btn-cerrar-menu");
  const menuLateral = document.getElementById("menu-lateral");
  const overlayMenu = document.getElementById("overlay-menu");
  const enlacesMenu = document.querySelectorAll("#menu-lateral a");

  if (!btnMenu || !btnCerrarMenu || !menuLateral || !overlayMenu) {
    return;
  }

  function abrirMenu() {
    menuLateral.classList.remove("-translate-x-full");
    overlayMenu.classList.remove("hidden");
  }

  function cerrarMenu() {
    menuLateral.classList.add("-translate-x-full");
    overlayMenu.classList.add("hidden");
  }

  btnMenu.addEventListener("click", abrirMenu);
  btnCerrarMenu.addEventListener("click", cerrarMenu);
  overlayMenu.addEventListener("click", cerrarMenu);

  enlacesMenu.forEach(function (enlace) {
    enlace.addEventListener("click", cerrarMenu);
  });
});
