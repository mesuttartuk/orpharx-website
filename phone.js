'use strict';
(() => {
  const input = document.getElementById('phone');
  if (!input) return;
  const country = document.getElementById('phone-country');
  const hint = document.getElementById('phone-hint');
  const error = document.getElementById('phone-error');
  const tr = document.documentElement.lang === 'tr';
  const lib = window.libphonenumber;
  if (!lib) {
    input.setCustomValidity(tr ? 'Telefon doğrulaması yüklenemedi. Sayfayı yenileyin.' : 'Phone validation could not load. Please reload.');
    return;
  }
  const names = new Intl.DisplayNames([tr ? 'tr' : 'en'], {type:'region'});
  const picker = document.querySelector('.country-picker');
  const trigger = picker.querySelector('summary');
  const flag = document.getElementById('phone-flag');
  const flagBase = flag.getAttribute('src').replace(/tr\.svg$/, '');
  const options = document.getElementById('phone-countries');
  const countries = lib.getCountries().filter(code => !['AC', 'TA'].includes(code)).sort((a,b) => names.of(a).localeCompare(names.of(b), tr ? 'tr' : 'en'));
  country.replaceChildren(...countries.map(code => {
    const option = document.createElement('option');
    option.value = code;
    option.textContent = `${names.of(code)} (+${lib.getCountryCallingCode(code)})`;
    option.selected = code === 'TR';
    return option;
  }));
  countries.forEach(code => {
    const button = document.createElement('button');
    button.type = 'button';
    button.dataset.country = code;
    const image = document.createElement('img');
    image.src = flagBase + code.toLowerCase() + '.svg';
    image.alt = '';
    image.loading = 'lazy';
    const label = document.createElement('span');
    label.textContent = `${names.of(code)} (+${lib.getCountryCallingCode(code)})`;
    button.append(image, label);
    button.addEventListener('click', () => {
      country.value = code;
      updateCountry();
      picker.open = false;
      input.focus();
    });
    options.append(button);
  });
  picker.addEventListener('keydown', event => {
    if (event.key === 'Escape') { event.stopPropagation(); picker.open = false; trigger.focus(); }
    if (['ArrowDown','ArrowUp','Home','End'].includes(event.key)) {
      event.preventDefault(); picker.open = true;
      const buttons = Array.from(options.querySelectorAll('button'));
      const index = buttons.indexOf(document.activeElement);
      const next = event.key === 'Home' ? 0 : event.key === 'End' ? buttons.length - 1 : event.key === 'ArrowDown' ? Math.min(index + 1, buttons.length - 1) : Math.max(index - 1, 0);
      buttons[next].focus();
    }
  });
  document.addEventListener('click', event => { if (!picker.contains(event.target)) picker.open = false; });
  picker.addEventListener('focusout', event => { if (!picker.contains(event.relatedTarget)) picker.open = false; });
  let canonical = '';
  function validate(showError = false) {
    const raw = input.value.trim();
    canonical = '';
    let valid = !raw;
    if (raw) {
      const number = lib.parsePhoneNumberFromString(raw, {defaultCountry:country.value, extract:false});
      valid = Boolean(number && !number.ext && number.country === country.value && number.isValid());
      if (valid) canonical = number.number;
    }
    const message = valid ? '' : (tr ? `${names.of(country.value)} için geçerli bir telefon numarası girin.` : `Enter a valid phone number for ${names.of(country.value)}.`);
    input.setCustomValidity(message);
    input.setAttribute('aria-invalid', String(!valid && showError));
    error.textContent = showError ? message : '';
    return valid;
  }
  function updateCountry() {
    const code = lib.getCountryCallingCode(country.value);
    flag.src = flagBase + country.value.toLowerCase() + '.svg';
    document.getElementById('phone-code').textContent = '+' + code;
    trigger.setAttribute('aria-label', `${tr ? 'Ülke seçin' : 'Select country'}: ${names.of(country.value)} (+${code})`);
    options.querySelectorAll('button').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.country === country.value)));
    hint.textContent = tr ? 'Seçilen ülkeye ait telefon numaranızı girin.' : 'Enter your phone number for the selected country.';
    input.placeholder = tr ? 'Telefon numarası' : 'Phone number';
    validate(Boolean(input.value));
  }
  input.addEventListener('input', () => {
    // Format while typing at the end; preserve the caret when editing inside the number.
    if (input.selectionStart === input.value.length && /^[+\d\s().-]*$/.test(input.value)) {
      input.value = new lib.AsYouType(country.value).input(input.value);
    }
    validate(false);
  });
  input.addEventListener('blur', () => {
    if (validate(true) && canonical) input.value = lib.parsePhoneNumberFromString(canonical).formatNational();
  });
  input.addEventListener('invalid', () => validate(true));
  country.addEventListener('change', updateCountry);
  input.form.addEventListener('formdata', event => {
    validate();
    event.formData.set('phone', canonical);
    event.formData.set('phone_country', country.value);
  });
  input.form.addEventListener('reset', () => setTimeout(() => { updateCountry(); error.textContent = ''; }, 0));
  updateCountry();
})();
