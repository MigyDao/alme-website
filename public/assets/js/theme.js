(() => {
  const DEFAULT_THEME = 'light';
  const THEMES = new Set(['light', 'dark']);
  const params = new URLSearchParams(window.location.search);
  const requested = params.get('theme');
  const current = THEMES.has(requested) ? requested : DEFAULT_THEME;

  document.documentElement.dataset.theme = current;
  document.documentElement.style.colorScheme = current;

  window.ALME_THEME = Object.freeze({
    defaultTheme: DEFAULT_THEME,
    currentTheme: current,
    previewTheme: THEMES.has(requested) ? requested : null
  });
})();