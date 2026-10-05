/* The light / dark switch on the studio pages.
   Each page sets <html data-mode> from the saved choice before first paint (a one-line
   script in its head), so this file only has to run the button. With no saved choice
   the page follows the system setting. */
(function () {
  var root = document.documentElement;
  var button = document.querySelector(".mode-toggle");
  if (!button) return;
  var system = window.matchMedia("(prefers-color-scheme: light)");

  function current() {
    return root.dataset.mode || (system.matches ? "light" : "dark");
  }

  function describe() {
    var next = current() === "light" ? "dark" : "light";
    button.setAttribute("aria-label", "Use " + next + " theme");
    button.title = "Use " + next + " theme";
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = current() === "light" ? "#f3f1ec" : "#1d2024";
  }

  button.hidden = false;
  describe();

  button.addEventListener("click", function () {
    var next = current() === "light" ? "dark" : "light";
    root.dataset.mode = next;
    try {
      localStorage.setItem("mode", next);
    } catch (e) {
      /* private browsing: the choice lasts for this page only */
    }
    describe();
  });

  system.addEventListener("change", describe);
})();
