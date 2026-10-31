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
  let detailsBeforePrint = [];
  window.addEventListener('beforeprint', () => {
    detailsBeforePrint = Array.from(document.querySelectorAll('.paper-details'), element => ({element, open:element.open}));
    detailsBeforePrint.forEach(({element}) => { element.open = true; });
  });
  window.addEventListener('afterprint', () => {
    detailsBeforePrint.forEach(({element, open}) => { element.open = open; });
    detailsBeforePrint = [];
  });
  document.querySelector('#print-cv').addEventListener('click', () => window.print());
})();
