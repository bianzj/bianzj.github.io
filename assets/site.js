(() => {
  const root = document.documentElement;
  const toggle = document.querySelector('#language-toggle');
  function setLanguage(language) {
    root.lang = language === 'en' ? 'en' : 'zh-CN';
    document.title = root.lang === 'en' ? 'Zunjian Bian | Thermal Infrared Remote Sensing' : '卞尊健 | 热红外遥感';
    toggle.textContent = root.lang === 'en' ? '中文' : 'EN';
    toggle.setAttribute('aria-label', root.lang === 'en' ? '切换为中文' : 'Switch to English');
    try { localStorage.setItem('cv-language', root.lang); } catch (_) {}
  }
  let saved;
  try { saved = localStorage.getItem('cv-language'); } catch (_) {}
  if (saved) setLanguage(saved);
  toggle.addEventListener('click', () => setLanguage(root.lang === 'en' ? 'zh-CN' : 'en'));
  document.querySelectorAll('[data-gallery]').forEach(gallery => {
    const tabs = Array.from(gallery.querySelectorAll('[role="tab"]'));
    const select = tab => {
      tabs.forEach(item => {
        const active = item === tab;
        item.setAttribute('aria-selected', String(active));
        item.tabIndex = active ? 0 : -1;
        document.getElementById(item.getAttribute('aria-controls')).hidden = !active;
      });
    };
    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => select(tab));
      tab.addEventListener('keydown', event => {
        let next;
        if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
        if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = tabs.length - 1;
        if (next !== undefined) { event.preventDefault(); select(tabs[next]); tabs[next].focus(); }
      });
    });
    gallery.dataset.enhanced = 'true';
    select(tabs[0]);
  });
  let printExpanded = false;
  let detailsBeforePrint = [];
  let panelsBeforePrint = [];
  window.addEventListener('beforeprint', () => {
    if (printExpanded) return;
    printExpanded = true;
    detailsBeforePrint = Array.from(document.querySelectorAll('.paper-details'), element => ({element, open:element.open}));
    detailsBeforePrint.forEach(({element}) => { element.open = true; });
    panelsBeforePrint = Array.from(document.querySelectorAll('.result-panel'), element => ({element, hidden:element.hidden}));
    panelsBeforePrint.forEach(({element}) => { element.hidden = false; });
  });
  window.addEventListener('afterprint', () => {
    detailsBeforePrint.forEach(({element, open}) => { element.open = open; });
    detailsBeforePrint = [];
    panelsBeforePrint.forEach(({element, hidden}) => { element.hidden = hidden; });
    printExpanded = false;
    panelsBeforePrint = [];
  });
  document.querySelector('#print-cv').addEventListener('click', () => window.print());
})();
