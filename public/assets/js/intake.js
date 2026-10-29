(() => {
  const frame = document.querySelector('iframe[data-tally-src]');
  if (!frame) return;
  const embed = new URL(frame.dataset.tallySrc);
  const direct = document.getElementById('intake-direct-link');
  const service = new URLSearchParams(window.location.search).get('service');
  const services = [
    'Maker Project Consultation', '3D Modelling / Design',
    'Custom Build / Furniture', 'Growing / Land',
    'Organization / Spatial Systems', 'Remote Design & Production Support',
    'General / Other'
  ];
  if (services.includes(service)) {
    embed.searchParams.set('service', service);
    if (direct) {
      const url = new URL(direct.href);
      url.searchParams.set('service', service);
      direct.href = url.href;
    }
  }
  frame.dataset.tallySrc = embed.href;
  // Let Tally initialize resizing; retain a scrollable form if its widget fails.
  const fallback = () => { frame.src = embed.href; };
  const script = document.createElement('script');
  script.src = 'https://tally.so/widgets/embed.js';
  script.onload = () => {
    if (typeof Tally !== 'undefined') Tally.loadEmbeds();
    else fallback();
  };
  script.onerror = fallback;
  document.body.appendChild(script);
})();
