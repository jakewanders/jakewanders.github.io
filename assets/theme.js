// Theme toggle. The inline script in <head> already applied the initial theme
// before first paint; this file only wires up the button.
(function () {
  var KEY = "theme";
  var root = document.documentElement;
  var btn = document.querySelector("[data-theme-toggle]");
  if (!btn) return;

  function current() {
    return root.getAttribute("data-theme") === "dark" ? "dark" : "light";
  }

  function apply(theme) {
    root.setAttribute("data-theme", theme);
    btn.setAttribute("aria-label", "Switch to " + (theme === "dark" ? "light" : "dark") + " mode");
    try { localStorage.setItem(KEY, theme); } catch (e) { /* private mode etc. */ }
  }

  btn.addEventListener("click", function () {
    apply(current() === "dark" ? "light" : "dark");
  });

  // If the user never chose explicitly, follow OS changes live.
  var saved = null;
  try { saved = localStorage.getItem(KEY); } catch (e) {}
  if (!saved && window.matchMedia) {
    window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", function (e) {
      root.setAttribute("data-theme", e.matches ? "dark" : "light");
    });
  }

  btn.setAttribute("aria-label", "Switch to " + (current() === "dark" ? "light" : "dark") + " mode");
})();
