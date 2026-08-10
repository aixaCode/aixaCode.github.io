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

  /* Mermaid flows read left-to-right on wider screens and top-to-bottom on mobile. */
  if (window.matchMedia && window.matchMedia("(max-width: 700px)").matches) {
    Array.prototype.forEach.call(document.querySelectorAll(".mermaid"), function (diagram) {
      diagram.textContent = diagram.textContent.replace(/^flowchart LR/m, "flowchart TB");
    });
  }

  var filterButtons = document.querySelectorAll("[data-filter]");
  var filterCards = document.querySelectorAll("[data-tags]");
  if (filterButtons.length && filterCards.length) {
    var requested = new URLSearchParams(window.location.search).get("filter") || "all";
    var valid = Array.prototype.some.call(filterButtons, function (button) {
      return button.getAttribute("data-filter") === requested;
    });
    applyFilter(valid ? requested : "all");

    Array.prototype.forEach.call(filterButtons, function (button) {
      button.addEventListener("click", function () {
        var value = button.getAttribute("data-filter");
        applyFilter(value);
        var url = value === "all" ? window.location.pathname : window.location.pathname + "?filter=" + encodeURIComponent(value);
        window.history.replaceState({}, "", url);
      });
    });

    function applyFilter(value) {
      Array.prototype.forEach.call(filterButtons, function (button) {
        button.setAttribute("aria-pressed", String(button.getAttribute("data-filter") === value));
      });
      Array.prototype.forEach.call(filterCards, function (card) {
        var tags = (card.getAttribute("data-tags") || "").split(" ");
        card.classList.toggle("is-hidden", value !== "all" && tags.indexOf(value) === -1);
      });
    }
  }
})();
