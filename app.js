'use strict';
const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#main-nav');
function closeMenu() { navigation.classList.remove('open'); menuButton.setAttribute('aria-expanded', 'false'); }
menuButton.addEventListener('click', () => { const open = navigation.classList.toggle('open'); menuButton.setAttribute('aria-expanded', String(open)); });
document.addEventListener('keydown', event => { if (event.key === 'Escape') { closeMenu(); menuButton.focus(); } });
document.addEventListener('click', event => { if (!event.target.closest('.site-header')) closeMenu(); });
const form = document.querySelector('#contact-form');
if (form) {
  const config = JSON.parse(document.querySelector('#site-config').textContent);
  const status = document.querySelector('#form-status');
  const submit = form.querySelector('[type="submit"]');
  document.querySelector('#email-draft').addEventListener('click', () => {
    if (!form.reportValidity()) return;
    const data = new FormData(form);
    const keys = ['company', 'name', 'position', 'email', 'phone', 'product', 'therapeutic_area', 'interest', 'message'];
    const body = keys.map(key => `${form.querySelector(`label[for="${key}"]`).textContent}: ${data.get(key)}`).join('\n\n');
    window.location.href = `mailto:fatmatartuk@gmail.com?subject=${encodeURIComponent('OrphaRx — Partnership enquiry')}&body=${encodeURIComponent(body)}`;
    status.textContent = config.draftStatus;
  });
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    if (!config.deliveryEnabled) { status.textContent = config.formStatus; return; }
    if (submit.disabled) return;
    submit.disabled = true; submit.textContent = config.sending;
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 15000);
    try {
      const response = await fetch(form.action, {method:'POST', body:new FormData(form), headers:{Accept:'application/json'}, signal:controller.signal});
      const result = await response.json();
      if (!response.ok || result.ok !== true) throw new Error('Delivery failed');
      status.textContent = config.sent; form.reset();
    } catch { status.textContent = config.error; }
    finally { clearTimeout(timeout); submit.disabled = false; submit.textContent = config.submit; }
  });
}
