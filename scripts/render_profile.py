"""Render public profile pages and SVG assets from profile.json (standard library only)."""
from pathlib import Path
import json
from html import escape
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'profile.json').read_text(encoding='utf-8'))
ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)

def write(path, content):
    (ROOT / path).write_text(content.rstrip() + '\n', encoding='utf-8')

def svg(width, height, title, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">\n<title>{escape(title)}</title>\n{body}\n</svg>'

def icon(kind, color='#a78bfa'):
    shapes = {
        'workflow': '<rect x="5" y="4" width="15" height="13" rx="3"/><rect x="44" y="4" width="15" height="13" rx="3"/><rect x="24" y="44" width="15" height="13" rx="3"/><path d="M20 10h24M32 10v34"/>',
        'agent': '<rect x="12" y="17" width="40" height="34" rx="9"/><path d="M32 17V8M5 28v13M59 28v13M23 42h18"/><circle cx="23" cy="30" r="2"/><circle cx="41" cy="30" r="2"/><circle cx="32" cy="5" r="3"/>',
        'cloud': '<path d="M16 47h34a11 11 0 0 0 1-22A19 19 0 0 0 15 22a13 13 0 0 0 1 25Z"/><path d="m23 31-6 6 6 6m18-12 6 6-6 6m-9-14-4 16"/>',
        'robot': '<rect x="12" y="8" width="40" height="35" rx="6"/><circle cx="24" cy="23" r="3"/><circle cx="40" cy="23" r="3"/><path d="M22 34h20M23 43v12M41 43v12M5 15v22M59 15v22"/>',
        'search': '<circle cx="27" cy="27" r="18"/><path d="m40 40 17 17M17 30l7-9 7 13 7-11"/>',
        'chart': '<path d="M8 8v48h48M19 45V31M33 45V20M47 45V10"/>',
        'mesh': '<path d="m10 12 44 8-20 33-24-41 24 41 21-9-1-24M10 12l45 32"/><circle cx="10" cy="12" r="4"/><circle cx="54" cy="20" r="4"/><circle cx="34" cy="53" r="4"/><circle cx="55" cy="44" r="4"/>',
        'code': '<path d="m21 15-16 17 16 17m22-34 16 17-16 17M38 7 26 57"/>'
    }
    return f'<g fill="none" stroke="{color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">{shapes[kind]}</g>'

header = '''<defs><linearGradient id="accent"><stop stop-color="#7c3aed"/><stop offset="1" stop-color="#0891b2"/></linearGradient><clipPath id="typing"><rect class="reveal" x="275" y="173" width="550" height="54"/></clipPath></defs>
<style>.reveal{animation:type 7s steps(28,end) infinite}.cursor{animation:blink 1s steps(2,end) infinite}@keyframes type{0%,10%{width:0}45%,90%,100%{width:550}}@keyframes blink{50%{opacity:0}}@media(prefers-reduced-motion:reduce){.reveal,.cursor{animation:none}}</style>
<g fill="none" stroke="#a78bfa" stroke-width="2" opacity=".45"><circle cx="125" cy="123" r="43"/><ellipse cx="125" cy="123" rx="65" ry="23" transform="rotate(-35 125 123)"/><circle cx="975" cy="123" r="43"/><ellipse cx="975" cy="123" rx="65" ry="23" transform="rotate(35 975 123)"/></g>
<circle cx="165" cy="98" r="5" fill="#06b6d4"/><circle cx="942" cy="153" r="5" fill="#8b5cf6"/>
<g text-anchor="middle" font-family="Segoe UI,Arial,sans-serif"><text x="550" y="57" fill="#64748b" font-size="17" letter-spacing="5">HELLO / HOLA</text><text x="550" y="130" fill="url(#accent)" font-size="62" font-weight="700">NAME</text><text x="550" y="163" fill="#64748b" font-size="22">TITLE</text></g>
<g clip-path="url(#typing)" font-family="Consolas,monospace" font-size="30" fill="#8b5cf6"><text x="287" y="214">I build useful automation.</text></g><rect class="cursor" x="813" y="190" width="3" height="29" fill="#8b5cf6"/>
<text x="550" y="259" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="16" fill="#64748b">Lima, Peru · Enterprise AI · APIs · Automation</text>
<rect x="360" y="285" width="380" height="2" rx="1" fill="url(#accent)"/>'''.replace('NAME', escape(DATA['name'])).replace('TITLE', escape(DATA['title']))
write('assets/profile-header.svg', svg(1100, 300, DATA['name'] + ' - animated introduction', header))

for specialty in DATA['specialties']:
    kind = specialty['kind']
    body = f'<circle cx="100" cy="48" r="36" fill="#241d3c"/>' + f'<g transform="translate(76 24) scale(.75)">{icon(kind)}</g>'
    body += f'<g text-anchor="middle" font-family="Segoe UI,Arial,sans-serif"><text x="100" y="107" fill="#8b5cf6" font-size="18" font-weight="700">{escape(specialty["label"])}</text><text x="100" y="132" fill="#64748b" font-size="13">{escape(specialty["detail"])}</text></g>'
    write(f'assets/specialty-{kind}.svg', svg(200, 145, specialty['label'] + ': ' + specialty['detail'], body))

def project_svg(project, lang):
    body = '<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#151a2d"/><stop offset="1" stop-color="#241d3c"/></linearGradient></defs><rect x="1" y="1" width="618" height="248" rx="16" fill="url(#bg)" stroke="#55436f"/>'
    body += f'<g transform="translate(516 32) scale(.9)">{icon(project["kind"])}</g>'
    body += '<g font-family="Segoe UI,Arial,sans-serif">'
    body += f'<text x="30" y="37" font-size="12" letter-spacing="1.4" fill="#a78bfa">{escape(project["category"])}</text>'
    body += f'<text x="30" y="83" font-size="30" font-weight="700" fill="#f8fafc">{escape(project["name"])}</text>'
    for i, line in enumerate(project['lines'][lang]):
        body += f'<text x="30" y="{122+i*28}" font-size="18" fill="#cbd5e1">{escape(line)}</text>'
    body += f'<text x="30" y="189" font-size="14" fill="#94a3b8">{escape(project["stack"])}</text>'
    label = 'Explore project →' if lang == 'en' else 'Explorar proyecto →'
    body += f'<text x="30" y="226" font-size="16" font-weight="600" fill="#c4b5fd">{label}</text></g>'
    return svg(620, 250, project['name'] + '. ' + ' '.join(project['lines'][lang]), body)

for lang in ('en', 'es'):
    for p in DATA['projects']:
        write(f'assets/project-{p["repo"].lower()}-{lang}.svg', project_svg(p, lang))

def period(job, lang):
    end = job['end'] or ('Present' if lang == 'en' else 'Actualidad')
    result = f'{job["start"]} – {end}'
    if job.get('second_period'):
        second = job['second_period']
        result += f' / {second["start"]} – {second["end"]}'
    return result

def career(lang):
    title = 'Professional background' if lang == 'en' else 'Trayectoria profesional'
    home = 'README.md' if lang == 'en' else 'README.es.md'
    other = 'CAREER.es.md' if lang == 'en' else 'CAREER.md'
    body = f'# {DATA["name"]} · {title}\n\n**{DATA["title"]}**  \n{DATA["location"]}\n\n'
    body += f'[GitHub profile]({home}) · [English]({"CAREER.md"}) · [Español]({"CAREER.es.md"}) · [LinkedIn]({DATA["links"]["linkedin"]})\n\n'
    body += DATA['summary'][lang] + '\n\n'
    body += '## Experience\n\n' if lang == 'en' else '## Experiencia\n\n'
    for job in DATA['experience']:
        body += f'### {job["company"]} · {job["role"]}\n\n**{period(job, lang)}**\n\n'
        body += '\n'.join('- ' + x for x in job['points'][lang]) + '\n\n'
    body += '## Education & research\n\n' if lang == 'en' else '## Educación e investigación\n\n'
    for edu in DATA['education']:
        body += f'### {edu["program"][lang]}\n\n**{edu["institution"]} · {edu["dates"]}**  \n{edu["status"][lang]}\n\n'
        if edu['detail'][lang]:
            body += edu['detail'][lang] + '\n\n'
    body += '## Achievements & certification\n\n' if lang == 'en' else '## Logros y certificación\n\n'
    body += '\n'.join('- ' + a[lang] for a in DATA['achievements']) + '\n'
    body += f'- [{DATA["certification"]}]({DATA["links"]["certification"]})\n\n'
    body += '## Technical competencies\n\n' if lang == 'en' else '## Competencias técnicas\n\n'
    for skill in DATA['skills']:
        body += f'**{skill["category"]}:** {skill["items"]}.\n\n'
    body += '## Languages\n\n' if lang == 'en' else '## Idiomas\n\n'
    body += DATA['languages'][lang] + '\n\n'
    body += '## Projects\n\n' if lang == 'en' else '## Proyectos\n\n'
    for p in DATA['projects']:
        body += f'- [{p["name"]}](https://github.com/{DATA["username"]}/{p["repo"]}): {" ".join(p["lines"][lang])}\n'
    body += f'\n---\n\n[LinkedIn]({DATA["links"]["linkedin"]}) · [Email]({DATA["links"]["email"]}) · [ORCID]({DATA["links"]["orcid"]})\n'
    return body

def readme(lang):
    career_file = 'CAREER.md' if lang == 'en' else 'CAREER.es.md'
    career_label = 'Full background' if lang == 'en' else 'Trayectoria completa'
    cert_label = 'Certification' if lang == 'en' else 'Certificación'
    body = f'<p align="center"><img src="assets/profile-header.svg" width="100%" alt="{DATA["name"]} · {DATA["title"]}" /></p>\n\n'
    body += '<p align="center"><a href="README.md">English</a> · <a href="README.es.md">Español</a></p>\n\n'
    body += f'<p align="center"><a href="{DATA["links"]["linkedin"]}">LinkedIn</a> · <a href="{DATA["links"]["email"]}">Email</a> · <a href="{career_file}">{career_label}</a> · <a href="{DATA["links"]["certification"]}">{cert_label}</a></p>\n\n'
    body += DATA['summary'][lang] + '\n\n'
    if lang == 'en':
        body += '**Currently at EVOL** · AI & Intelligent Automation Architect, since August 2026.\n\n'
    else:
        body += '**Actualmente en EVOL** · AI & Intelligent Automation Architect, desde agosto de 2026.\n\n'
    body += '<p align="center">\n' + '\n'.join(f'  <img src="assets/specialty-{s["kind"]}.svg" width="18%" alt="{s["label"]}: {s["detail"]}" />' for s in DATA['specialties']) + '\n</p>\n\n'
    body += '## 🚀 AI & automation projects\n\n' if lang == 'en' else '## 🚀 Proyectos de IA y automatización\n\n'
    for start in (0, 2):
        body += '<p align="center">\n'
        for p in DATA['projects'][start:start+2]:
            body += f'  <a href="https://github.com/{DATA["username"]}/{p["repo"]}"><img src="assets/project-{p["repo"].lower()}-{lang}.svg" width="49%" alt="{p["name"]}: {escape(" ".join(p["lines"][lang]), quote=True)}" /></a>\n'
        body += '</p>\n\n'
    body += ('**Also building:** ' if lang == 'en' else '**Más proyectos:** ') + '[LazyArcade](https://github.com/berniehans/lazyarcade) · [NASA Space Apps tools](https://github.com/berniehans/NSAC_SCRAPER)\n\n'
    body += '<details>\n<summary>🎬 ' + ('Project demos, charts & architecture' if lang == 'en' else 'Demos, gráficos y arquitectura de los proyectos') + '</summary>\n\n'
    for p in DATA['projects'][:3]:
        body += f'### {p["name"]}\n\n<a href="https://github.com/{DATA["username"]}/{p["repo"]}"><img src="{p["preview"]}" width="700" alt="{p["name"]} - {"architecture overview" if p["repo"]=="AxiomRAG" else "project preview"}" /></a>\n\n'
    body += '</details>\n\n'
    body += '## 🧭 Professional background\n\n' if lang == 'en' else '## 🧭 Trayectoria profesional\n\n'
    body += '| ' + ('Company & role | Period' if lang == 'en' else 'Empresa y cargo | Periodo') + ' |\n|---|---|\n'
    for job in DATA['experience'][:2]:
        body += f'| **{job["company"]}** · {job["role"]} | {period(job, lang)} |\n'
    text = 'Earlier: Gesnext · Belltech · NTT Data · Indra · Equifax.' if lang == 'en' else 'Anteriormente: Gesnext · Belltech · NTT Data · Indra · Equifax.'
    body += f'\n{text}  \n[**{career_label} →**]({career_file})\n\n'
    body += '## 🎓 Education & milestones\n\n' if lang == 'en' else '## 🎓 Formación y logros\n\n'
    body += ('- **NASA Space Apps Challenge 2025:** National winner.\n- **International Indra Hackathon:** Winner.\n- **AI master\'s program · UNI, 2024–2025:** Coursework completed; **thesis pending**. Coursework average: 17/20.\n- **Computer and Systems Engineering · USIL:** Degree obtained in 2017.\n' if lang == 'en' else '- **NASA Space Apps Challenge 2025:** Ganador nacional.\n- **Hackathon Internacional de Indra:** Ganador.\n- **Maestría en IA · UNI, 2024–2025:** Cursos completados; **tesis pendiente**. Promedio de cursos: 17/20.\n- **Ingeniería en Informática y Sistemas · USIL:** Grado obtenido en 2017.\n')
    body += f'- [**{DATA["certification"]} ↗**]({DATA["links"]["certification"]})\n\n'
    body += '<details>\n<summary>🛠️ ' + ('Technical competencies & languages' if lang == 'en' else 'Competencias técnicas e idiomas') + '</summary>\n\n'
    for s in DATA['skills']:
        body += f'- **{s["category"]}:** {s["items"]}.\n'
    body += '\n' + DATA['languages'][lang] + '\n\n</details>\n\n---\n\n'
    body += '<p align="center"><strong>' + ("Let's build useful automation." if lang == 'en' else 'Construyamos automatización útil.') + f'</strong><br /><a href="{DATA["links"]["linkedin"]}">LinkedIn</a> · <a href="{DATA["links"]["email"]}">Email</a> · <a href="{DATA["links"]["orcid"]}">ORCID</a></p>\n'
    return body

for lang, suffix in [('en', ''), ('es', '.es')]:
    write(f'README{suffix}.md', readme(lang))
    write(f'CAREER{suffix}.md', career(lang))

for p in ASSETS.glob('*.svg'):
    ET.parse(p)
print('Rendered 4 pages and', len(list(ASSETS.glob('*.svg'))), 'SVG assets from profile.json')
