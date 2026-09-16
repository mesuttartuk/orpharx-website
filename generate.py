from pathlib import Path
import html,json
ROOT=Path(__file__).resolve().parent
def esc(s): return html.escape(s,quote=True)
data=json.loads((ROOT/'content-source.json').read_text(encoding='utf-8'))
EN,TR=data['en'],data['tr']
pages=['index','about','focus','partnerships','founders','contact']
names=['Ziya Akkurt','Tuna Yavuz, M.D.','Fatma Tartuk']
def paras(arr): return ''.join('<p>'+esc(x)+'</p>' for x in arr)
def generate(lang,d):
    prefix='' if lang=='en' else 'tr/'
    base='' if lang=='en' else '../'
    folder=ROOT/prefix;folder.mkdir(exist_ok=True)
    def link(p): return p+'.html'
    def cta(): return f'<section class="cta wrap"><div><span class="eyebrow">ORPHARX · TÜRKİYE</span><h2>{d["ctaTitle"]}</h2></div><div><p>{d["ctaText"]}</p><a class="button light" href="contact.html">{d["talk"]}<span aria-hidden="true">↗</span></a></div></section>'
    def head(title,intro,kicker):return f'<section class="page-head wrap"><span class="eyebrow">{kicker}</span><h1>{title}</h1><p class="lead">{intro}</p></section>'
    def rows(titles,texts): return ''.join(f'<article class="detail-row"><span class="index">0{i+1}</span><h3>{t}</h3><p>{texts[i]}</p></article>' for i,t in enumerate(titles))
    for current,page in enumerate(pages):
        nav=''.join(f'<a href="{link(p)}"'+(' aria-current="page"' if p==page else '')+f'>{d["nav"][i]}</a>' for i,p in enumerate(pages))
        other=f'{base}tr/{page}.html' if lang=='en' else f'../{page}.html'
        switch=f'<div class="languages" aria-label="Language"><a href="{other if lang=="tr" else page+".html"}" lang="en"'+(' aria-current="true"' if lang=='en' else '')+'>EN</a><span>/</span>'+f'<a href="{other if lang=="en" else page+".html"}" lang="tr"'+(' aria-current="true"' if lang=='tr' else '')+'>TR</a></div>'
        if page=='index':
            cards=''.join(f'<a class="focus-card" href="focus.html#area-{i}"><span class="index">0{i+1}</span><h3>{t}</h3><p>{d["focusShort"][i]}</p><span class="card-arrow" aria-hidden="true">↗</span></a>' for i,t in enumerate(d['focusNames']))
            body=f'''<section class="hero"><div class="hero-copy"><span class="eyebrow">{d['eyebrow']}</span><h1>{d['hero']}</h1><p>{d['intro']}</p><a class="button" href="about.html">{d['discover']}<span aria-hidden="true">↗</span></a></div><div class="hero-art"><img src="{base}assets/science.webp" alt="" fetchpriority="high" width="1536" height="1024"><div class="image-caption">{'SCIENCE. PURPOSE. POSSIBILITY.' if lang=='en' else 'BİLİM. AMAÇ. OLASILIK.'}</div></div></section>
<div class="discipline-strip"><span>ORPHARX PHARMACEUTICALS</span><span>{'RARE · ORPHAN · SPECIALTY' if lang=='en' else 'NADİR · YETİM · UZMANLAŞMIŞ'}</span><span>TÜRKİYE</span></div>
<section class="wrap section"><div class="section-heading"><span class="eyebrow">01 / {d['nav'][2]}</span><h2>{d['focusTitle']}</h2><p>{d['focusIntro']}</p></div><div class="focus-grid">{cards}</div></section>
<section class="approach"><div class="wrap section"><div class="section-heading"><span class="eyebrow">02 / {'Our approach' if lang=='en' else 'Yaklaşımımız'}</span><h2>{d['approachTitle']}</h2><p>{d['approachIntro']}</p></div><div class="steps">{''.join(f'<article><span class="index">0{i+1}</span><h3>{t}</h3><p>{d["stepText"][i]}</p></article>' for i,t in enumerate(d['steps']))}</div></div></section>
<section class="wrap section purpose"><div><span class="eyebrow">03 / {'Our purpose' if lang=='en' else 'Amacımız'}</span><h2>{d['whyTitle']}</h2></div><div>{paras([d['why'],d['why2']])}</div></section>{cta()}'''
        elif page=='about':
            body=head(d['aboutTitle'],d['aboutLead'],d['nav'][1])+f'<section class="wrap section split"><h2>{d["aboutLead"]}</h2><div>{paras(d["aboutParas"])}</div></section><section class="soft"><div class="wrap section"><h2>{d["experience"]}</h2><div class="expertise">'+''.join(f'<div><span>0{i+1}</span>{x}</div>' for i,x in enumerate(d['experienceItems']))+f'</div></div></section><section class="wrap section split"><h2>{d["purposeTitle"]}</h2><p>{d["purpose"]}</p></section>'+cta()
        elif page=='focus':
            body=head(d['focusPageTitle'],d['focusPageIntro'],d['nav'][2])+ '<section class="wrap section focus-details">'+''.join(f'<article id="area-{i}" class="focus-detail"><span class="index">0{i+1}</span><div><h2>{t}</h2><p>{d["focusLong"][i]}</p></div></article>' for i,t in enumerate(d['focusNames']))+'</section>'+cta()
        elif page=='partnerships':
            body=head(d['partnerTitle'],d['partnerIntro'],d['nav'][3])+f'<section class="wrap section split"><h2>{d["offer"]}</h2><p>{d["partnerBody"]}</p></section><section class="wrap rows">{rows(d["offerNames"],d["offerText"])}</section><section class="soft"><div class="wrap section"><h2>{d["opportunities"]}</h2><div class="op-grid">'+''.join(f'<article><span class="index">0{i+1}</span><h3>{t}</h3><p>{d["opText"][i]}</p></article>' for i,t in enumerate(d['opNames']))+f'</div></div></section><section class="wrap section split"><h2>{d["lookTitle"]}</h2><div><ul class="look-list">'+''.join(f'<li>{x}</li>' for x in d['look'])+f'</ul><p>{d["lookNote"]}</p></div></section>'+cta()
        elif page=='founders':
            body=head(d['foundersTitle'],d['foundersIntro'],d['nav'][4])+'<section class="wrap section founders">'+''.join(f'<article class="founder"><div class="founder-name"><span class="index">0{i+1}</span><h2>{name}</h2><span class="eyebrow">{d["cofounder"]}</span></div><div><p class="bio-lead">{esc(d["bios"][i][0])}</p><details><summary>{d["bio"]}<span aria-hidden="true">+</span></summary>{paras(d["bios"][i][1:])}</details></div></article>' for i,name in enumerate(names))+'</section>'+cta()
        else:
            fields=''
            keys=['company','name','position','email','phone','product','therapeutic_area','interest','message']
            for i,key in enumerate(keys):
                required=key in ['name','email','message']
                label=d['labels'][i]+(' *' if required else f' <span>({d["optional"]})</span>')
                if key=='message': control=f'<textarea id="{key}" name="{key}" rows="5" maxlength="5000" required></textarea>'
                elif key=='phone': control=f'''<div class="phone-control"><details class="country-picker"><summary aria-label="{'Select country' if lang=='en' else 'Ülke seçin'}"><img id="phone-flag" src="{base}assets/flags/tr.svg" alt=""><span id="phone-code">+90</span><span aria-hidden="true">▾</span></summary><div class="country-options" id="phone-countries"></div></details><select hidden id="phone-country" name="phone_country" aria-label="{'Country' if lang=='en' else 'Ülke'}"><option value="TR">Türkiye (+90)</option></select><input id="phone" name="phone" type="tel" autocomplete="tel-national" inputmode="tel" maxlength="40" aria-describedby="phone-hint phone-error"></div><small id="phone-hint"></small><small id="phone-error" aria-live="polite"></small>'''
                elif key=='interest': control=f'<select id="{key}" name="{key}"><option value="">{d["choose"]}</option>'+''.join(f'<option value="{esc(x)}">{esc(x)}</option>' for x in d['opNames'])+'</select>'
                else:
                    typ='email' if key=='email' else 'tel' if key=='phone' else 'text'
                    auto={'company':'organization','name':'name','position':'organization-title','email':'email','phone':'tel'}.get(key,'off')
                    control=f'<input id="{key}" name="{key}" type="{typ}" autocomplete="{auto}" maxlength="250"'+(' required' if required else '')+'>'
                fields+=f'<div class="field {"full" if key in ("message", "phone") else ""}"><label for="{key}">{label}</label>{control}</div>'
            body=f'<section class="wrap section contact-layout"><div class="contact-copy"><span class="eyebrow">{d["nav"][5]}</span><h1>{d["contactTitle"]}</h1><p>{d["contactIntro"]}</p><p>{d["contactText"]}</p><a class="email-link" href="mailto:fatmatartuk@gmail.com">fatmatartuk@gmail.com ↗</a></div><form id="contact-form" action="{base}api/contact.php" method="post"><div class="form-grid">{fields}</div><div class="trap" aria-hidden="true"><label>Website<input name="website" tabindex="-1" autocomplete="off"></label></div><p class="form-note">{d["formNote"]}</p><p class="form-note">{d["formPrivacy"]}</p><button class="button" type="submit">{d["submit"]}<span aria-hidden="true">↗</span></button><p id="form-status" role="status" aria-live="polite">{d["formStatus"]}</p><button id="email-draft" class="text-button" type="button">{d["emailDraft"]} ↗</button><noscript><p>{d["formStatus"]}</p><a href="mailto:fatmatartuk@gmail.com">fatmatartuk@gmail.com</a></noscript></form></section>'
        title='OrphaRx | '+('Specialised medicines in Türkiye' if lang=='en' else 'Uzmanlık gerektiren ilaçlar') if page=='index' else d['nav'][current]+' | OrphaRx'
        config={k:d[k] for k in ['sent','error','sending','submit','draftStatus','formStatus']};config['deliveryEnabled']=False
        out=f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title><meta name="description" content="{esc(d['intro'])}"><meta name="theme-color" content="#0A2540"><link rel="stylesheet" href="{base}styles.css?v=phone-flags-3"><link rel="alternate" hreflang="{'tr' if lang=='en' else 'en'}" href="{other}"><script src="{base}assets/libphonenumber-max.js" defer></script><script src="{base}phone.js?v=phone-flags-3" defer></script><script src="{base}app.js?v=phone-flags-3" defer></script></head><body><a class="skip" href="#main">{d['skip']}</a><header class="site-header"><a class="brand" href="index.html" aria-label="OrphaRx — {d['nav'][0]}"><img src="{base}assets/logo.svg" width="2048" height="682" alt="OrphaRx Pharmaceuticals"></a><button class="menu-toggle" aria-expanded="false" aria-controls="main-nav">{d['menu']} <span aria-hidden="true">☰</span></button><nav id="main-nav" aria-label="{'Main navigation' if lang=='en' else 'Ana gezinme'}">{nav}</nav>{switch}</header><main id="main">{body}</main><footer class="site-footer wrap"><div><a class="brand" href="index.html"><img src="{base}assets/logo.svg" width="2048" height="682" alt="OrphaRx Pharmaceuticals"></a><p>{d['footer']}</p></div><div class="footer-links">{nav}</div><div class="footer-bottom"><span>© 2026 OrphaRx. {d['rights']}</span><span>{d['footnote']}</span></div></footer><script type="application/json" id="site-config">{json.dumps(config,ensure_ascii=False)}</script></body></html>'''
        (folder/(page+'.html')).write_text(out,encoding='utf-8')
generate('en',EN)
generate('tr',TR)
print('Generated 12 HTML pages')
