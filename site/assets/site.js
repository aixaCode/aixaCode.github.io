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
  // Gentle syntax colours for the few code samples; the source stays plain text.
  const token = /(\/\/.*|#.*)|("(?:[^"\\]|\\.)*"|`(?:[^`\\]|\\.)*`)|\b(if|return|await|async|const|let|export|interface|readonly|throw|new|function|only)\b|^(\s*-?\s*[\w]+)(?=:\s)/gm;
  const kinds = ['comment', 'string', 'keyword', 'key'];
  const escape = text => text.replace(/[&<>]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;'}[c]));
  document.querySelectorAll('.code-block code').forEach(code => {
    const text = code.textContent;
    let html = '', last = 0;
    for (const match of text.matchAll(token)) {
      const kind = kinds[match.slice(1).findIndex(Boolean)];
      html += escape(text.slice(last, match.index)) + `<span class="tok-${kind}">${escape(match[0])}</span>`;
      last = match.index + match[0].length;
    }
    code.innerHTML = html + escape(text.slice(last));
  });
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
