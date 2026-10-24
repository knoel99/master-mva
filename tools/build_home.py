#!/usr/bin/env python3
"""Generate the home page (index.html) from the catalogue and the course pages.

Usage (repository root):  python3 tools/build_home.py

Sources:
- data/catalog-2026-2027.json — the single structural source (specs/catalog-source.md):
  which courses are offered, semester, label, track, ECTS, official volume.
- courses/<slug>/index.qmd — the session plan of each page (number of sessions,
  self-study estimate), read as in specs/hours-and-progression.md.
- ROUTES below — the three example programmes of specs/home-and-tracks.md; each one
  must satisfy the validation rules (checked by tools/check_gates.py).
"""

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAT = json.loads((ROOT / "data/catalog-2026-2027.json").read_text(encoding="utf-8"))
COURSES = CAT["courses"]
BY_SLUG = {c["slug"]: c for c in COURSES}

UPS_URL = "https://www.universite-paris-saclay.fr/en/education/master/mathematics-and-applications/m2-mathematics-vision-learning"
MVA_URL = "https://www.master-mva.com/"

# Example programmes: exactly 8 modules each (specs/home-and-tracks.md).
ROUTES = {
    "theory": ("Learning theory route", [
        "s1-convex-optimization", "s1-theoretical-foundations-dl", "s1-optimal-transport-ml",
        "s1-stochastic-calculus-ml", "s2-kernel-methods", "s2-sequential-learning",
        "s2-random-matrices-ml", "s2-stopping-times-online"]),
    "vision": ("Vision and imaging route", [
        "s1-object-recognition-cv", "s1-3d-computer-vision", "s1-deep-learning",
        "s1-image-denoising", "s2-dl-image-restoration-synthesis", "s2-generative-models-images",
        "s2-point-clouds-3d", "s2-remote-sensing"]),
    "genai": ("Generative AI and LLM route", [
        "s1-foundations-llms", "s1-deep-learning", "s1-probabilistic-graphical-models",
        "s1-stochastic-calculus-ml", "s2-diffusion-multiscale", "s2-llm-code-proof",
        "s2-training-deploying-large-models", "s2-reinforcement-learning"]),
}
ROUTE_TEXT = {
    "theory": ("Why this selection — the theory spine. Semester 1 sets the tools every proof in the master "
               "relies on: convex optimisation, the approximation / optimisation / generalisation triangle of "
               "deep networks, optimal transport between distributions and the stochastic calculus behind "
               "sampling and diffusion. Semester 2 turns them into learning theory: kernels and RKHS, online "
               "and sequential learning, random-matrix asymptotics of learning algorithms, and optimal stopping. "
               "Six Learning modules and two Modelling modules, four per semester: the validation rules hold. "
               "Profile: a PhD in statistical learning or optimisation."),
    "vision": ("Why this selection — the imaging spine. Semester 1 covers recognition (deep networks and "
               "object recognition), geometry (3D vision) and the signal side of images (denoising, with the "
               "human–machine competition as a benchmark culture). Semester 2 moves to generation and 3D data: "
               "deep restoration and synthesis, mathematical generative models of images, point clouds and "
               "satellite imagery. Two Learning modules and six Modelling modules, four per semester. "
               "Profile: computer vision or imaging R&D, in a lab or in industry."),
    "genai": ("Why this selection — the generative spine. Semester 1 builds the language-model stack (the "
              "Transformer and its training), the deep-learning basis, latent-variable and deep generative "
              "models, and the stochastic calculus of diffusion. Semester 2 studies diffusion and multiscale "
              "generation, LLMs for code and proof, distributed training and deployment, and reinforcement "
              "learning for post-training and agents. Six Learning modules and two Modelling modules, four per "
              "semester. Profile: research engineer or PhD on foundation models."),
}
TRACK_TOKEN = {"Santé": "sante", "I&I": "ii", "RR": "rr"}
TRACK_TEXT = {
    "sante": ("Track Santé — the official health track: at least five courses with the Santé label plus three "
              "free choices; one course may be replaced by the paired project with a physician. Most Santé "
              "courses are taught at the Université Paris Cité faculty of medicine (Cochin and Necker sites)."),
    "ii": ("Track Industrie & Ingénierie — for engineering students or engineers: eight modules, two of which are "
           "I&I modules designed by industrial partners, plus at least two Learning and two Modelling modules "
           "chosen outside the I&I list. Students outside the track may take one I&I module (it counts as Modelling)."),
    "rr": ("Track Recherche reproductible — open to everyone: validating one or two modules labelled RR places the "
           "student in the track (reproducible research, free software, open science)."),
}


def page_title(slug):
    p = ROOT / "courses" / slug / "index.qmd"
    if p.is_file():
        m = re.search(r'^title: "(.*)"', p.read_text(encoding="utf-8"), re.M)
        if m:
            return m.group(1)
    return BY_SLUG[slug]["title_en"]


def plan_info(slug):
    p = ROOT / "courses" / slug / "index.qmd"
    if not p.is_file():
        return "—", "—"
    src = p.read_text(encoding="utf-8")
    plan = src.split("### Session plan {#sessions}", 1)
    if len(plan) != 2:
        return "—", "—"
    body = plan[1].split("\n### ", 1)[0]
    rows = len(re.findall(r"^\|\s*\d+\s*\|", body, re.M))
    sm = re.search(r"\*\*Self-study, outside the [^*]*\*\* \(about (\d+(?:\.\d+)?) h", body)
    return f"{rows} sessions", (f"≈ {sm.group(1)} h" if sm else "none")


def tokens(c):
    toks = [r for r, (_, lst) in ROUTES.items() if c["slug"] in lst]
    toks += [TRACK_TOKEN[t] for t in c["tracks"]]
    return " ".join(toks)


def badges(c):
    out = [f'<span class="badge label">{t}</span>' for t in c["types"]]
    out += [f'<span class="badge track">Track {html.escape(t)}</span>' for t in c["tracks"]]
    if c["ects"] and c["ects"] != 5:
        out.append(f'<span class="badge choice">{c["ects"]:g} ECTS</span>')
    return " ".join(out)


def li(c):
    return (f'<li data-p="{tokens(c)}"><a href="courses/{c["slug"]}/index.html">'
            f'{html.escape(page_title(c["slug"]))}</a> {badges(c)}</li>')


def group(sem, typ):
    return [c for c in COURSES if c["semester"] == sem and typ in c["types"]]


def tree():
    out = ['<div class="tree" id="curriculum-tree">', "<ul>"]
    ref = [c for c in COURSES if c["kind"] == "refresher"]
    out.append("<li><h3>Refresher fortnight — 14 to 24 September 2026</h3>")
    out.append('<p class="tree-hint">Official refresher courses, optional and without registration (mandatory for the I&amp;I track); '
               "their programme is not published. The three pages below are independent support for the same fortnight.</p><ul>")
    for c in ref:
        out.append(f'<li><a href="courses/{c["slug"]}/index.html">{html.escape(page_title(c["slug"]))}</a> '
                   '<span class="badge pedagogical">Off-curriculum support</span></li>')
    out.append("</ul></li>")
    for sem, head in [(1, "Semester 1 — period 1 (28 September 2026 – 8 January 2027)"),
                      (2, "Semester 2 — period 2 (4 January – 2 April 2027)")]:
        out.append(f"<li><h3>{head}</h3><ul>")
        for typ, hint in [("Learning", "Learning label"), ("Modelling", "Modelling label"),
                          ("Opening", "Opening label — 2.5 ECTS courses count as half a module")]:
            items = group(sem, typ)
            if not items:
                continue
            out.append(f'<li><h4>{hint}</h4><ul>')
            out += [li(c) for c in items]
            out.append("</ul></li>")
        if sem == 2:
            proj = [c for c in COURSES if c["semester"] == 2 and not c["types"]]
            if proj:
                out.append("<li><h4>Project module</h4><ul>")
                out += [li(c) for c in proj]
                out.append("</ul></li>")
        out.append("</ul></li>")
    both = [c for c in COURSES if c["semester"] == "both"]
    out.append("<li><h3>Across both semesters</h3><ul>")
    out += [li(c) for c in both]
    out.append("</ul></li>")
    intern = BY_SLUG["s3-research-internship"]
    out.append("<li><h3>Research internship — from 5 April 2027</h3><ul>")
    out.append(f'<li><span class="badge mandatory">Mandatory</span> <a href="courses/{intern["slug"]}/index.html">'
               f'{html.escape(page_title(intern["slug"]))}</a> — 20 ECTS, at least four months, report and defence</li>')
    out.append("</ul></li>")
    out += ["</ul>", "</div>"]
    return "\n".join(out)


def programme():
    out = ["<!-- programme:start -->", '<div class="tbl-wrap"><table class="tbl programme">',
           "<thead><tr><th>Course</th><th>Label</th><th>ECTS</th><th>Official volume</th>"
           "<th>These notes</th><th>Self-study</th><th>Source notes</th></tr></thead><tbody>"]
    sections = [
        ("Refresher fortnight (independent support)", [c for c in COURSES if c["kind"] == "refresher"]),
        ("Semester 1", [c for c in COURSES if c["semester"] == 1]),
        ("Semester 2", [c for c in COURSES if c["semester"] == 2]),
        ("Across both semesters and internship", [c for c in COURSES if c["semester"] in ("both", 3)]),
    ]
    for head, items in sections:
        out.append(f'<tr><th colspan="7">{head}</th></tr>')
        for c in items:
            ours, self_h = plan_info(c["slug"]) if c["kind"] != "non-science" else ("—", "—")
            if c["hours_status"] == "official":
                vol = f'{c["plan_hours"]:g} h'
            elif c["hours_status"] == "assumed":
                vol = f'{c["plan_hours"]:g} h (assumed)'
            elif c["hours_status"] == "self-study":
                vol = "— (self-study)"
            elif c["hours_total"]:
                vol = f'{c["hours_total"]:g} h'
            else:
                vol = "—"
            lab = ", ".join(c["types"] + [f"Track {t}" for t in c["tracks"]]) or "—"
            note = c.get("discrepancy_note") or ("" if c["hours_status"] != "assumed" else c["plan_hours_note"])
            ects = f'{c["ects"]:g}' if c["ects"] else "—"
            out.append(f'<tr><td><a href="courses/{c["slug"]}/index.html">{html.escape(page_title(c["slug"]))}</a></td>'
                       f"<td>{html.escape(lab)}</td><td>{ects}</td><td>{vol}</td><td>{ours}</td><td>{self_h}</td>"
                       f"<td>{html.escape(note)}</td></tr>")
    out += ["</tbody></table></div>", "<!-- programme:end -->"]
    return "\n".join(out)


def route_list():
    out = ["<ul>"]
    for key, (name, lst) in ROUTES.items():
        names = ", ".join(html.escape(page_title(s)) for s in lst)
        out.append(f"<li><strong>{name}</strong>: {names}.</li>")
    out.append("</ul>")
    return "\n".join(out)


def page():
    texts = {**ROUTE_TEXT, **TRACK_TEXT}
    js_texts = json.dumps(texts, ensure_ascii=False)
    n_sci = sum(1 for c in COURSES if c["kind"] == "science")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<script>
(function(){{try{{var t=localStorage.getItem("mva-theme");if(t==="dark"||t==="light")document.documentElement.setAttribute("data-theme",t);}}catch(e){{}}}})();
</script>
<meta charset="utf-8">
<meta name="color-scheme" content="light dark">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Mathématiques, Vision, Apprentissage (MVA) — Master 2 of ENS Paris-Saclay. Independent open-source study notes: official description, validation rules, curriculum tree with the official tracks and three example programmes, course units and hours, projects, official documentation.">
<title>Mathématiques, Vision, Apprentissage (MVA)</title>
<link rel="stylesheet" href="assets/paper.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="topbar">
  <button type="button" class="tb-btn" id="toc-toggle" aria-controls="sidetoc" aria-expanded="false"><span aria-hidden="true">☰</span><span class="tb-label">Contents</span></button>
  <a class="brand" href="#top">MVA<span class="brand-sub"> · Independent study notes</span></a>
  <span class="tb-title" id="tb-title"></span>
  <button type="button" class="tb-btn" id="theme-toggle"><span aria-hidden="true">◐</span><span class="tb-label">Theme</span></button>
</header>
<div class="layout">
<nav class="sidetoc" id="sidetoc" aria-label="Contents"></nav>
<main class="paper home" id="main">

<header class="hero">
  <figure class="hero-illu" aria-hidden="true">
    <img src="assets/illu-hero-mva.svg" alt="" width="480" height="160">
  </figure>
  <h1>Mathématiques, Vision, Apprentissage (MVA)</h1>
  <p class="subtitle">Master 2 research programme of ENS Paris-Saclay, co-accredited with Institut Polytechnique de Paris and shared with Université Paris Cité</p>
</header>

<nav class="toc home-toc" aria-label="Contents">
<p class="toc-title">Contents</p>
<ol>
<li><a href="#description">Official description of the master</a></li>
<li><a href="#about">What is this website?</a></li>
<li><a href="#rules">How the year is validated</a></li>
<li><a href="#tree">Curriculum tree</a></li>
<li><a href="#programme">Programme 2026–2027: courses and hours</a></li>
<li><a href="#projects">Projects and assessment</a></li>
<li><a href="#official">Official documentation</a></li>
<li><a href="#after">After the master</a></li>
</ol>
</nav>

<section class="track-brief" id="description" aria-labelledby="description-title">
  <h2 id="description-title">Official description of the master</h2>
  <p>The MVA is a 2nd year Master’s Research programme which started in 1996, run by the mathematics department of ENS Paris-Saclay, co-accredited with the Institut Polytechnique de Paris and shared with Université Paris Cité. The Master’s in MVA is unique in France for its scientific focus on mathematical interfaces and its openness to an innovation ecosystem that brings together academic laboratories, research organisations and companies in France and abroad.</p>
  <p>In cooperation with several academic partners, it trains a large number of university and “grandes écoles” students each year in Research, Development and Innovation for public and private organizations and companies in the field of mathematics applied to data, image and signal processing. The huge growth in the use of digital data in all fields of science, technology and society requires the training of high-level mathematical researchers mastering the acquisition and processing of digital data on the one hand, and their automatic interpretation on the other. These two aspects are strictly complementary and are reflected in the three terms characterizing the MVA program.</p>
  <p>Courses run from mid-September to early April; the research internship starts in April and lasts four to six months.</p>
  <p class="hint">Source: <a href="{UPS_URL}">M2 Mathematics, Vision, Learning</a> (Université Paris-Saclay programme page). The master is directed by Yann Gousseau and Laurent Oudre (<a href="{MVA_URL}equipe/">master-mva.com, the team</a>).</p>
</section>

<section class="track-brief" id="about" aria-labelledby="about-title">
  <h2 id="about-title">What is this website?</h2>
  <p>This website is an independent, open-source project. It is not created, maintained or endorsed by ENS Paris-Saclay, its partner institutions or the instructors of the master.</p>
  <p>Its purpose is to share with the open community what may be taught in each course, based on the official course descriptions, the state of the art and existing published work. The content is organised and completed with the help of AI and LLM tools. For enrolment rules, ECTS and the official course list, always refer to the official documentation.</p>
  <p>Every scientific course of the 2026–2027 catalogue ({n_sci} courses) has one long page: an official fiche, a session plan that matches the official volume, the course itself with definitions, theorems, proofs and Python code, graded exercises, project subjects and a written-exam proposal, and references.</p>
</section>

<section class="track-brief" id="rules" aria-labelledby="rules-title">
  <h2 id="rules-title">How the year is validated</h2>
  <ul>
    <li>Each course counts <strong>5 ECTS</strong> (no compensation between courses) and the mandatory <strong>research internship 20 ECTS</strong>.</li>
    <li>Validate <strong>8 modules</strong> (at least 40 ECTS) with a mark of at least 10/20: at least <strong>4 in semester 1</strong> and <strong>3 in semester 2</strong>; over the year at least <strong>2 Modelling</strong> and <strong>2 Learning</strong> courses.</li>
    <li>Some <strong>Opening</strong> courses count 2.5 ECTS: two of them make one module.</li>
    <li>Tracks: <strong>Santé</strong> (5 Santé courses + 3 free choices), <strong>Industrie &amp; Ingénierie</strong> (2 I&amp;I modules + at least 2 Learning and 2 Modelling outside I&amp;I), <strong>Recherche reproductible</strong> (one or two RR modules). Double-degree students of ENSAE, ENSTA, Mines and CentraleSupélec validate 6 MVA modules and 2 approved modules of their school.</li>
    <li>The final transcript keeps the <strong>8 best marks</strong>; the internship mark must exceed 10/20.</li>
  </ul>
  <p>Calendar 2026–2027: refresher fortnight 14–24 September 2026; period 1 from 28 September 2026 to 8 January 2027; period 2 from 4 January to 2 April 2027; course choice from 14 September to 18 October and from 14 December to 17 January; internship forum on 2 December 2026; internships from 5 April 2027; juries on 24 September and 12 November 2027.</p>
  <p class="hint">Sources: master-mva.com, <a href="{MVA_URL}formation-mva/modalites-de-validation/">validation rules</a> and <a href="{MVA_URL}formation-mva/planning/">planning</a> (read on 22 October 2026).</p>
</section>

<section class="track-brief" id="tree" aria-labelledby="tree-title">
  <h2 id="tree-title">Curriculum tree</h2>
  <div class="tree-nav" role="group" aria-label="Track and route preselection">
    <button type="button" class="cta cta-ghost" data-path="" aria-pressed="true" title="Every course of the 2026–2027 catalogue">Full catalogue</button>
    <button type="button" class="cta cta-ghost" data-path="sante" aria-pressed="false" title="Courses labelled Track Santé">Track Santé</button>
    <button type="button" class="cta cta-ghost" data-path="ii" aria-pressed="false" title="Courses labelled Track I&amp;I">Track I&amp;I</button>
    <button type="button" class="cta cta-ghost" data-path="rr" aria-pressed="false" title="Courses labelled Track RR">Track RR</button>
    <button type="button" class="cta cta-ghost" data-path="theory" aria-pressed="false" title="Example programme: optimisation, deep-learning theory, kernels, sequential learning, random matrices">Learning theory route</button>
    <button type="button" class="cta cta-ghost" data-path="vision" aria-pressed="false" title="Example programme: recognition, 3D, denoising, restoration and synthesis, point clouds, remote sensing">Vision and imaging route</button>
    <button type="button" class="cta cta-ghost" data-path="genai" aria-pressed="false" title="Example programme: LLMs, generative models, diffusion, large-scale training, RL">Generative AI and LLM route</button>
  </div>
  <p id="path-desc" class="path-desc" hidden aria-live="polite"></p>
  <p class="tree-legend"><span class="badge label">Learning</span> / <span class="badge label">Modelling</span> / <span class="badge label">Opening</span> = official course labels; <span class="badge track">Track …</span> = official track label (source: <a href="{MVA_URL}cours-1er-semestre/">master-mva.com course lists</a>).<br>
  Track buttons highlight the courses carrying the track label. Route buttons highlight one example programme of eight modules that satisfies the validation rules — a route is this site’s reading guidance, not an official rule.</p>

{tree()}
  <p class="tree-hint">Example programmes behind the route buttons:</p>
{route_list()}
</section>

<section class="track-brief" id="programme" aria-labelledby="programme-title">
  <h2 id="programme-title">Programme 2026–2027: courses and hours</h2>
  <p>This table lists every course of the 2026–2027 MVA catalogue (master-mva.com semester lists, read in full on 22 October 2026). Official volumes and ECTS come from the <a href="{UPS_URL}">Université Paris-Saclay programme table</a>. Where that table displays no volume, the volume is derived from the session list published on master-mva.com and marked “assumed”. Where the two official sources disagree, the last column says so.</p>
  <p><strong>How to read “These notes”.</strong> Every course page has a <em>Session plan</em>: the official volume split into sessions (most MVA courses meet for 3 h).</p>
  <ul>
    <li>Each session has a level — <strong>1</strong> foundations, <strong>2</strong> core methods, <strong>3</strong> advanced — that never goes down from one session to the next.</li>
    <li>Chapters that do not fit in the official hours (research directions, extensions) are listed as self-study with a time estimate.</li>
  </ul>
{programme()}
</section>

<section class="track-brief" id="projects" aria-labelledby="projects-title">
  <h2 id="projects-title">Projects and assessment</h2>
  <p>MVA courses are mostly assessed by a project — often the study and reimplementation of a research paper — and a written exam. Every course page ends with a <strong>Projects and assessment</strong> section: solo and group project subjects with deliverables and grading criteria, and a written-exam proposal with sample questions.</p>
  <p>The <a href="projects/index.html">end-of-year projects</a> page proposes integrative projects that combine several courses of a semester or of a route, the way the research internship will.</p>
</section>

<section class="track-brief" id="official" aria-labelledby="official-title">
  <h2 id="official-title">Official documentation</h2>
  <p>These notes are independent; enrolment rules, ECTS and course lists live in the official sources:</p>
  <ul>
    <li><a href="{MVA_URL}">master-mva.com</a> — the master’s site: <a href="{MVA_URL}cours-1er-semestre/">semester 1 courses</a>, <a href="{MVA_URL}cours-2nd-semestre/">semester 2 courses</a>, <a href="{MVA_URL}formation-mva/modalites-de-validation/">validation rules</a>, <a href="{MVA_URL}formation-mva/planning/">planning</a>, <a href="{MVA_URL}formation-mva/stage/">internship</a></li>
    <li><a href="{MVA_URL}formation-mva/track-sante/">Track Santé</a> · <a href="{MVA_URL}formation-mva/track-industrie-et-ingenierie/">Track Industrie &amp; Ingénierie</a> · <a href="{MVA_URL}formation-mva/track-recherche-reproductible/">Track Recherche reproductible</a></li>
    <li><a href="{UPS_URL}">Université Paris-Saclay — M2 Mathematics, Vision, Learning</a>: programme table with ECTS and hourly volumes, admission</li>
    <li><a href="{MVA_URL}formation-mva/candidatures/">Applications</a> · <a href="{MVA_URL}formation-mva/faire-une-these-apres-le-mva/">Doing a PhD after the MVA</a></li>
  </ul>
</section>

<section class="track-brief" id="after" aria-labelledby="after-title">
  <h2 id="after-title">After the master</h2>
  <p>According to master-mva.com, the MVA is followed in the short term by a PhD or by a position as data scientist or engineer in the private sector; after a PhD, careers continue in public research and in the R&amp;D divisions of companies and administrations, across industry, health, defence and security, digital marketing, banking and insurance, and deep tech (<a href="{MVA_URL}accueil/apres-le-mva/les-debouches/">les débouchés</a>).</p>
  <p>An overview of the problem spaces the courses open onto — inferred from the curriculum and these notes, not an official employability claim:</p>
  <ul>
    <li><strong>PhD in mathematics of learning</strong> — optimisation, statistical learning theory, optimal transport, random matrices, sequential decision.</li>
    <li><strong>Computer vision and imaging researcher</strong> — recognition, 3D, restoration, generative models of images, remote sensing.</li>
    <li><strong>Medical imaging and health data scientist</strong> — the Santé track: medical image analysis, shape spaces, biostatistics, brain imaging.</li>
    <li><strong>Foundation-model research engineer</strong> — LLMs, diffusion, large-scale training and deployment, alignment and safety.</li>
    <li><strong>Industrial R&amp;D engineer</strong> — the I&amp;I track: signals, scientific imaging, uncertainty quantification, network optimisation.</li>
  </ul>
</section>

</main>
</div>
<footer class="foot">
<p>Independent, open-source study notes in English.
Official programme (ENS Paris-Saclay) —
  <a href="{MVA_URL}">master-mva.com</a> ·
  <a href="{UPS_URL}">Université Paris-Saclay programme page</a>
</p>
</footer>
<script defer src="assets/theme.js"></script>
<script>
(function(){{
  var nav = document.querySelector('.tree-nav');
  var tree = document.getElementById('curriculum-tree');
  var desc = document.getElementById('path-desc');
  if (!nav || !tree || !desc) return;
  var TEXTS = {js_texts};
  nav.addEventListener('click', function(e){{
    var b = e.target.closest('button[data-path]');
    if (!b) return;
    if (b.dataset.path) {{
      tree.dataset.path = b.dataset.path;
      desc.textContent = TEXTS[b.dataset.path] || '';
      desc.hidden = false;
    }} else {{
      delete tree.dataset.path;
      desc.hidden = true;
    }}
    nav.querySelectorAll('button[data-path]').forEach(function(x){{
      x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
    }});
  }});
}})();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    (ROOT / "index.html").write_text(page(), encoding="utf-8")
    print("index.html: generated from data/catalog-2026-2027.json and the course pages")
