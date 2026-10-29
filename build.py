"""Генератор внутренних страниц сайта: услуги, города, статьи, sitemap.

Запуск из папки сайта:  python build.py
Главная (index.html) пишется руками; всё остальное собирается отсюда из content.py.
"""
import json
from datetime import date
from html import escape
from pathlib import Path

from content import ARTICLES, CITIES, SERVICES

SITE = "https://centbuh-sevastopol.ru"   # заменить на настоящий домен
PHONE, PHONE_HREF = "+7 (978) 765-39-81", "+79787653981"
WA = "https://wa.me/79787653981"
MAX_URL = ""                              # ссылка на чат в MAX; пока пусто — кнопка не выводится
ORG_ID = f"{SITE}/#org"
ROOT = Path(__file__).parent
TODAY = date.today().isoformat()


def messengers(extra_class=""):
    out = [f'<a class="btn btn--ghost {extra_class}" href="{WA}" target="_blank" rel="noopener">WhatsApp</a>']
    if MAX_URL:
        out.append(f'<a class="btn btn--ghost btn--max {extra_class}" href="{MAX_URL}" target="_blank" rel="noopener">Написать в MAX</a>')
    return "\n".join(out)


def layout(*, path, title, description, h1, eyebrow, lead, body, crumbs, schema, pre):
    url = f"{SITE}/{path}"
    crumbs_ld = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": f"{SITE}/{p}"} for i, (n, p) in enumerate(crumbs)]}
    graph = {"@context": "https://schema.org", "@graph": [crumbs_ld] + schema}
    crumbs_html = " / ".join(
        f'<a href="{pre}{p}">{escape(n)}</a>' if i < len(crumbs) - 1 else f"<span>{escape(n)}</span>"
        for i, (n, p) in enumerate(crumbs))
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="geo.region" content="RU-SEV">
<meta name="geo.placename" content="Севастополь">
<meta name="geo.position" content="44.609315;33.516817">
<meta name="ICBM" content="44.609315, 33.516817">
<meta property="og:type" content="website">
<meta property="og:locale" content="ru_RU">
<meta property="og:site_name" content="Центральная бухгалтерия">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#f6efe6">
<link rel="icon" href="{pre}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lora:wght@500;600&family=Manrope:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pre}styles.css">
<script type="application/ld+json">
{json.dumps(graph, ensure_ascii=False, indent=1)}
</script>
</head>
<body>
<a class="skip" href="#main">Перейти к содержанию</a>
<header class="top">
  <div class="wrap top__row">
    <a class="brand" href="{pre}" aria-label="Центральная бухгалтерия — на главную">
      <img src="{pre}owl.jpg" alt="" width="40" height="51">
      <span><b>Центральная бухгалтерия</b><small>Севастополь · Крым</small></span>
    </a>
    <nav class="nav" aria-label="Основное меню">
      <a href="{pre}#services">Услуги</a>
      <a href="{pre}#prices">Цены</a>
      <a href="{pre}stati/">Статьи</a>
      <a href="{pre}#faq">Вопросы</a>
      <a href="#contacts">Контакты</a>
    </nav>
    <a class="top__phone" href="tel:{PHONE_HREF}">{PHONE}</a>
  </div>
</header>

<main id="main">
<section class="hero hero--inner">
  <div class="wrap">
    <nav class="crumbs" aria-label="Навигация">{crumbs_html}</nav>
    <p class="eyebrow">{escape(eyebrow)}</p>
    <h1>{escape(h1)}</h1>
    <p class="lead">{lead}</p>
    <div class="cta">
      <a class="btn btn--main" href="#contacts">Бесплатная консультация</a>
      {messengers()}
    </div>
  </div>
</section>
{body}
{contacts_block(pre)}
</main>
{footer(pre)}
<a class="float-call" href="tel:{PHONE_HREF}" aria-label="Позвонить в Центральную бухгалтерию">Позвонить</a>
<script src="{pre}app.js" defer></script>
</body>
</html>
"""


def contacts_block(pre):
    return f"""
<section id="contacts" class="section section--soft">
  <div class="wrap contacts">
    <div>
      <p class="eyebrow">Контакты</p>
      <h2>Обсудим вашу задачу</h2>
      <address>
        <p><b>Офис:</b> Севастополь, ул. Кулакова, 6, 2 этаж</p>
        <p><b>Телефон и WhatsApp:</b> <a href="tel:{PHONE_HREF}">{PHONE}</a></p>
        <p><b>Часы работы:</b> пн–пт 9:00–17:00</p>
      </address>
      <div class="cta">{messengers()}</div>
    </div>
    <form class="mini" id="callForm" action="{pre}send.php" method="post" novalidate>
      <h3>Перезвоним в рабочее время</h3>
      <label class="field"><span>Имя</span><input type="text" name="name" autocomplete="name" required maxlength="80"></label>
      <label class="field"><span>Телефон</span><input type="tel" name="phone" autocomplete="tel" inputmode="tel" placeholder="+7 (978) ___-__-__" required maxlength="25"></label>
      <input class="hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
      <input type="hidden" name="source" value="callback">
      <label class="consent"><input type="checkbox" name="consent" required> <span>Согласен на обработку персональных данных по <a href="{pre}privacy.html" target="_blank">политике конфиденциальности</a></span></label>
      <button type="submit" class="btn btn--main">Жду звонка</button>
      <p class="form-msg" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>"""


def footer(pre):
    svc = "".join(f'<li><a href="{pre}{s["slug"]}/">{escape(s["short"])}</a></li>' for s in SERVICES)
    cty = "".join(f'<li><a href="{pre}{c["slug"]}/">Бухгалтер {escape(c["in"])}</a></li>' for c in CITIES)
    art = "".join(f'<li><a href="{pre}stati/{a["slug"]}/">{escape(a["short"])}</a></li>' for a in ARTICLES)
    return f"""<footer class="foot">
  <div class="wrap">
    <div class="foot__cols">
      <div><h4>Услуги</h4><ul>{svc}</ul></div>
      <div><h4>Города Крыма</h4><ul><li><a href="{pre}">Бухгалтер в Севастополе</a></li>{cty}</ul></div>
      <div><h4>Статьи</h4><ul>{art}<li><a href="{pre}stati/">Все статьи</a></li></ul></div>
    </div>
    <div class="foot__row">
      <p>© {date.today().year} ООО «Центральная бухгалтерия» · Севастополь, ул. Кулакова, 6 · <a href="tel:{PHONE_HREF}">{PHONE}</a></p>
      <p><a href="{pre}privacy.html">Политика конфиденциальности</a></p>
    </div>
  </div>
</footer>"""


def faq_html(faq):
    items = "".join(f"<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>" for q, a in faq)
    return f'<section class="section"><div class="wrap faq"><p class="eyebrow">Вопросы и ответы</p><h2>Частые вопросы</h2>{items}</div></section>'


def faq_ld(faq):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}


def blocks_html(blocks):
    out = []
    for i, (h, paras) in enumerate(blocks):
        cls = "section section--soft" if i % 2 else "section"
        inner = "".join(f"<p>{p}</p>" if not p.startswith("<") else p for p in paras)
        out.append(f'<section class="{cls}"><div class="wrap prose"><h2>{escape(h)}</h2>{inner}</div></section>')
    return "\n".join(out)


def related_html(title, links):
    cards = "".join(f'<a class="card card--link" href="{href}"><h3>{escape(t)}</h3><p>{escape(d)}</p></a>' for t, d, href in links)
    return f'<section class="section"><div class="wrap"><h2>{escape(title)}</h2><div class="cards cards--3">{cards}</div></div></section>'


def write(path, html):
    out = ROOT / path / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8", newline="\n")


def build_services():
    for s in SERVICES:
        others = [(o["short"], o["teaser"], f'../{o["slug"]}/') for o in SERVICES if o is not s][:3]
        body = blocks_html(s["blocks"]) + faq_html(s["faq"]) + related_html("Другие услуги", others)
        schema = [{
            "@type": "Service", "name": s["name"], "serviceType": s["short"], "description": s["description"],
            "provider": {"@type": "AccountingService", "@id": ORG_ID, "name": "Центральная бухгалтерия",
                         "telephone": "+7-978-765-39-81",
                         "address": {"@type": "PostalAddress", "streetAddress": "ул. Кулакова, 6",
                                     "addressLocality": "Севастополь", "addressCountry": "RU"}},
            "areaServed": ["Севастополь", "Республика Крым"],
            **({"offers": {"@type": "Offer", "priceCurrency": "RUB", "price": s["price"]}} if s.get("price") else {}),
        }, faq_ld(s["faq"])]
        write(s["slug"], layout(path=f'{s["slug"]}/', title=s["title"], description=s["description"], h1=s["h1"],
                                eyebrow="Услуги · Севастополь и Крым", lead=s["lead"], body=body,
                                crumbs=[("Главная", ""), (s["short"], f'{s["slug"]}/')], schema=schema, pre="../"))


def build_cities():
    svc_links = [(o["short"], o["teaser"], f'../{o["slug"]}/') for o in SERVICES[:6]]
    for c in CITIES:
        body = blocks_html(c["blocks"]) + related_html(f"Что делаем для бизнеса {c['in']}", svc_links) + faq_html(c["faq"])
        schema = [{
            "@type": "Service", "name": f"Бухгалтерские услуги {c['in']}", "serviceType": "Бухгалтерское обслуживание",
            "description": c["description"],
            "provider": {"@type": "AccountingService", "@id": ORG_ID, "name": "Центральная бухгалтерия"},
            "areaServed": {"@type": "City", "name": c["name"]},
        }, faq_ld(c["faq"])]
        write(c["slug"], layout(path=f'{c["slug"]}/', title=c["title"], description=c["description"], h1=c["h1"],
                                eyebrow=f"{c['name']} · дистанционно из Севастополя", lead=c["lead"], body=body,
                                crumbs=[("Главная", ""), (f"Бухгалтер {c['in']}", f'{c["slug"]}/')], schema=schema, pre="../"))


def build_articles():
    for a in ARTICLES:
        body = f'<section class="section"><div class="wrap prose article"><p class="muted">Опубликовано {a["date_human"]} · Обновлено {a["updated_human"]}</p>{a["html"]}<p class="note">Статья носит справочный характер. Правила меняются — перед сдачей отчётности сверяйтесь с налоговым календарём ФНС или спросите нас.</p></div></section>'
        body += faq_html(a["faq"])
        schema = [{
            "@type": "Article", "headline": a["h1"], "description": a["description"],
            "datePublished": a["date"], "dateModified": a["updated"], "inLanguage": "ru",
            "author": {"@type": "Organization", "@id": ORG_ID, "name": "Центральная бухгалтерия"},
            "publisher": {"@type": "Organization", "@id": ORG_ID, "name": "Центральная бухгалтерия",
                          "logo": {"@type": "ImageObject", "url": f"{SITE}/owl.jpg"}},
            "image": f"{SITE}/og.png", "mainEntityOfPage": f"{SITE}/stati/{a['slug']}/",
        }, faq_ld(a["faq"])]
        write(f'stati/{a["slug"]}', layout(path=f'stati/{a["slug"]}/', title=a["title"], description=a["description"],
                                           h1=a["h1"], eyebrow="Статьи · налоги и учёт", lead=a["lead"], body=body,
                                           crumbs=[("Главная", ""), ("Статьи", "stati/"), (a["short"], f'stati/{a["slug"]}/')],
                                           schema=schema, pre="../../"))
    cards = "".join(f'<a class="card card--link" href="{a["slug"]}/"><p class="muted">{a["date_human"]}</p><h3>{escape(a["h1"])}</h3><p>{escape(a["description"])}</p></a>' for a in ARTICLES)
    body = f'<section class="section"><div class="wrap"><div class="cards cards--3">{cards}</div></div></section>'
    schema = [{"@type": "Blog", "name": "Статьи «Центральной бухгалтерии»", "url": f"{SITE}/stati/",
               "publisher": {"@id": ORG_ID}}]
    write("stati", layout(path="stati/", title="Статьи о налогах и бухгалтерии для бизнеса в Севастополе и Крыму",
                          description="Простые статьи о налогах, отчётности и выборе налогового режима для ИП и ООО в Севастополе и Крыму от «Центральной бухгалтерии».",
                          h1="Статьи о налогах и учёте", eyebrow="Полезное для предпринимателей",
                          lead="Разбираем сроки, налоговые режимы и изменения законов простым языком — для ИП и компаний Севастополя и Крыма.",
                          body=body, crumbs=[("Главная", ""), ("Статьи", "stati/")], schema=schema, pre="../"))


def build_home():
    """Подставляет общий подвал и кнопку MAX в главную (между маркерами)."""
    p = ROOT / "index.html"
    s = p.read_text(encoding="utf-8")
    start, end = s.index("<!--FOOTER-->") + len("<!--FOOTER-->"), s.index("<!--/FOOTER-->")
    s = s[:start] + "\n" + footer("") + "\n" + s[end:]
    start, end = s.index("<!--MAX-->") + len("<!--MAX-->"), s.index("<!--/MAX-->")
    btn = f'<a class="btn btn--ghost btn--max" href="{MAX_URL}" target="_blank" rel="noopener">Написать в MAX</a>' if MAX_URL else ""
    s = s[:start] + btn + s[end:]
    p.write_text(s, encoding="utf-8", newline="\n")


def build_sitemap():
    urls = [("", "1.0", "monthly")]
    urls += [(f'{s["slug"]}/', "0.9", "monthly") for s in SERVICES]
    urls += [(f'{c["slug"]}/', "0.8", "monthly") for c in CITIES]
    urls += [("stati/", "0.6", "weekly")] + [(f'stati/{a["slug"]}/', "0.7", "yearly") for a in ARTICLES]
    urls += [("privacy.html", "0.2", "yearly")]
    rows = "\n".join(f"  <url><loc>{SITE}/{u}</loc><lastmod>{TODAY}</lastmod><changefreq>{f}</changefreq><priority>{p}</priority></url>" for u, p, f in urls)
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{rows}\n</urlset>\n', encoding="utf-8", newline="\n")


if __name__ == "__main__":
    build_services()
    build_cities()
    build_articles()
    build_home()
    build_sitemap()
    print(f"ok: {len(SERVICES)} услуг, {len(CITIES)} городов, {len(ARTICLES)} статей")
