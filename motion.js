'use strict';
(() => {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  const header = document.querySelector('.site-header');
  const progress = document.createElement('div');
  progress.className = 'scroll-progress';
  progress.setAttribute('aria-hidden', 'true');
  document.body.append(progress);
  let scheduled = false;
  function update() {
    const range = document.documentElement.scrollHeight - window.innerHeight;
    progress.style.transform = `scaleX(${range > 0 ? window.scrollY / range : 0})`;
    header.classList.toggle('scrolled', window.scrollY > 15);
    scheduled = false;
  }
  window.addEventListener('scroll', () => { if (!scheduled) { scheduled = true; requestAnimationFrame(update); } }, {passive:true});
  window.addEventListener('resize', update);
  update();
  if (!reduce.matches && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); }
    }), {threshold:0.08});
    document.querySelectorAll('.section-heading,.focus-card,.steps article,.purpose-photo,.purpose>div,.cta,.detail-row,.founder,.op-grid article').forEach(element => {
      if (element.getBoundingClientRect().top > window.innerHeight) { element.classList.add('reveal-ready'); observer.observe(element); }
    });
  }
  const hero = document.querySelector('.hero');
  if (hero && !reduce.matches) {
    const toggle = document.createElement('button');
    const tr = document.documentElement.lang === 'tr';
    toggle.className = 'motion-toggle'; toggle.type = 'button';
    toggle.textContent = tr ? 'Hareketi duraklat' : 'Pause motion';
    toggle.setAttribute('aria-pressed','false');
    toggle.addEventListener('click', () => {
      const paused = document.body.classList.toggle('motion-paused');
      toggle.setAttribute('aria-pressed',String(paused));
      toggle.textContent = tr ? (paused ? 'Hareketi oynat' : 'Hareketi duraklat') : (paused ? 'Play motion' : 'Pause motion');
    });
    hero.append(toggle);
  }
})();
