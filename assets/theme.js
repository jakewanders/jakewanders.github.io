// Theme toggle. The inline script in <head> already applied the initial theme
// before first paint; this file wires up the button and keeps the choice in sync.
(function () {
  var KEY = "theme";
  var root = document.documentElement;
  var btn = document.querySelector("[data-theme-toggle]");
  if (!btn) return;

  function current() {
    return root.getAttribute("data-theme") === "dark" ? "dark" : "light";
  }

  function label(theme) {
    btn.setAttribute("aria-label", "Switch to " + (theme === "dark" ? "light" : "dark") + " mode");
  }

  function persist(theme) {
    try { localStorage.setItem(KEY, theme); } catch (e) { /* storage blocked */ }
    // Cookie fallback so the choice survives even where localStorage is unavailable.
    try { document.cookie = KEY + "=" + theme + "; path=/; max-age=31536000; SameSite=Lax"; } catch (e) {}
  }

  function apply(theme, save) {
    root.setAttribute("data-theme", theme);
    label(theme);
    if (save) persist(theme);
  }

  btn.addEventListener("click", function () {
    apply(current() === "dark" ? "light" : "dark", true);
  });

  // Another tab changed the theme: follow it.
  window.addEventListener("storage", function (e) {
    if (e.key === KEY && (e.newValue === "dark" || e.newValue === "light")) apply(e.newValue, false);
  });

  // Never chose explicitly: follow OS changes live.
  var saved = null;
  try { saved = localStorage.getItem(KEY); } catch (e) {}
  if (!saved) saved = (document.cookie.match(/(?:^|; )theme=(dark|light)/) || [])[1] || null;
  if (!saved && window.matchMedia) {
    window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", function (e) {
      apply(e.matches ? "dark" : "light", false);
    });
  }

  label(current());
})();
