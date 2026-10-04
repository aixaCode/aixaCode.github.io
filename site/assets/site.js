(() => {
  const header = document.querySelector('.site-header');
  const menu = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.primary-nav');
  if (menu && nav) {
    const close = () => { header.dataset.open = 'false'; menu.setAttribute('aria-expanded','false'); };
    menu.addEventListener('click', () => {
      const open = menu.getAttribute('aria-expanded') !== 'true';
      header.dataset.open = String(open); menu.setAttribute('aria-expanded', String(open));
    });
    nav.addEventListener('click', close);
    document.addEventListener('keydown', event => { if (event.key === 'Escape') { close(); menu.focus(); } });
    window.matchMedia('(min-width: 721px)').addEventListener('change', close);
  }
  const filters = [...document.querySelectorAll('[data-filter]')];
  const cards = [...document.querySelectorAll('[data-tags]')];
  const contents = document.querySelector('.article-toc details');
  if (contents) {
    const readingLayout = window.matchMedia('(min-width: 721px)');
    const setContents = () => { contents.open = readingLayout.matches; };
    setContents();
    readingLayout.addEventListener('change', setContents);
  }
  if (filters.length && cards.length) {
    const apply = value => {
      filters.forEach(button => button.setAttribute('aria-pressed',String(button.dataset.filter === value)));
      cards.forEach(card => { card.classList.toggle('is-hidden', value !== 'all' && !card.dataset.tags.split(' ').includes(value)); });
      const count = document.querySelector('#project-count');
      if (count) count.textContent = `${cards.filter(card => !card.classList.contains('is-hidden')).length} case studies`;
    };
    const requested = new URLSearchParams(location.search).get('filter') || 'all';
    apply(filters.some(button => button.dataset.filter === requested) ? requested : 'all');
    filters.forEach(button => button.addEventListener('click', () => {
      apply(button.dataset.filter);
      history.replaceState({},'',location.pathname + (button.dataset.filter === 'all' ? '' : '?filter=' + encodeURIComponent(button.dataset.filter)));
    }));
  }
})();
(() => {
  // Fade sections in as they scroll into view. Only for things below the fold at load, so nothing visible blinks.
  if (!('IntersectionObserver' in window) || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const selector = 'main > section:not(.home-hero):not(.page-hero):not(:has(.article-card, .filter-card)), main > div, .article-card, .filter-card, .notes-rail, .article-body figure, .pillar, .role, .site-footer .footer-top';
  const fold = window.innerHeight;
  const items = [...document.querySelectorAll(selector)].filter(el => el.getBoundingClientRect().top > fold * 0.9);
  if (!items.length) return;
  document.documentElement.classList.add('js-motion');
  const observer = new IntersectionObserver(entries => {
    entries.filter(entry => entry.isIntersecting).forEach((entry, index) => {
      entry.target.style.setProperty('--i', index);
      entry.target.classList.add('is-in');
      observer.unobserve(entry.target);
    });
  }, { rootMargin: '0px 0px -8% 0px' });
  items.forEach(el => { el.classList.add('reveal'); observer.observe(el); });
})();
