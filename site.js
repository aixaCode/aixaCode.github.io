(function () {
  var root = document.documentElement;
  var theme = document.getElementById("theme");
  var nav = document.getElementById("nav");
  var menu = document.getElementById("menu");
  var themeKey = "ab-theme";
  var stored = null;

  try { stored = localStorage.getItem(themeKey) || localStorage.getItem("theme"); } catch (error) {}

  var media = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)");
  setTheme(stored || (media && media.matches ? "dark" : "light"));

  function setTheme(value) {
    root.setAttribute("data-theme", value);
    if (theme) theme.setAttribute("aria-checked", value === "dark" ? "true" : "false");
  }

  if (theme) {
    theme.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      setTheme(next);
      try { localStorage.setItem(themeKey, next); } catch (error) {}
    });
  }

  if (menu && nav) {
    menu.addEventListener("click", function () {
      var open = nav.getAttribute("data-open") === "true";
      nav.setAttribute("data-open", String(!open));
      menu.setAttribute("aria-expanded", String(!open));
    });

    document.getElementById("navlinks").addEventListener("click", function () {
      nav.setAttribute("data-open", "false");
      menu.setAttribute("aria-expanded", "false");
    });
  }

  if (nav && "IntersectionObserver" in window) {
    var sentinel = document.createElement("div");
    sentinel.style.cssText = "position:absolute;top:0;height:1px;width:1px";
    document.body.prepend(sentinel);
    new IntersectionObserver(function (entries) {
      nav.setAttribute("data-stuck", String(!entries[0].isIntersecting));
    }).observe(sentinel);
  }

  var year = document.getElementById("yr");
  if (year) year.textContent = new Date().getFullYear();
})();
