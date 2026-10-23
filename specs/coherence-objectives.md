# Coherence of the notes with the MVA validation rules

This note maps the 2026 to 2027 catalogue onto the notes in this repository. It is a reference for someone choosing a year, and a backlog for the people writing the missing pages. It does not add a course, an ECTS value, or an assessment rule.

## Sources

The structural source is `data/catalog-2026-2027.json`, read from master-mva.com and the Université Paris-Saclay programme table on 22 October 2026. The validation page <https://www.master-mva.com/formation-mva/modalites-de-validation/> was fetched again on 23 October 2026. Where the two disagree, both wordings are quoted and neither is "corrected" here.

The catalogue has no UE code field. This note does not invent one. A missing fact stays missing.

Page state is a reading of the tree, not a catalogue field. `full notes` means a science source with no TODO placeholder. `skeleton` means a science source that still has that placeholder. On this tree the skeletons are 247 to 293 words and the full notes are at least 20 000 words, so a 2000-word reading selects the same pages. `framing` is a non-science page. `refresher` is one of the three fortnight pages. `missing` means the catalogue slug has no `courses/<slug>/index.qmd`. `tools/check_project_sections.py` uses the TODO test for a substantial science page.

## Validation constraints

The catalogue stores this statement, which is the rule this site checks on the home page.

> Each course counts 5 ECTS (no compensation) and the mandatory internship 20 ECTS. Validate 8 modules (40 ECTS minimum) with a mark >= 10/20: at least 4 modules in semester 1 and 3 in semester 2; over the year at least 2 courses labelled Modelling and 2 labelled Learning. Some Opening courses count 2.5 ECTS: two of them make one 5-ECTS module. Track I&I: 8 modules with 2 I&I modules, at least 2 Learning and 2 Modelling outside I&I; non-I&I students may validate one I&I module (counts as Modelling). Track RR: open to all; validating one or two RR modules places the student in the track. Track Santé: at least 5 Santé-labelled courses + 3 free choices (one may be replaced by the hospital-immersion project). Double degree (ENSAE, ENSTA, Mines, CentraleSupélec): 6 MVA modules (2 Modelling + 2 Learning minimum) + 2 approved modules of the home school, no per-semester constraint. The final transcript keeps the 8 best marks.

The validation page fetched on 23 October 2026 agrees with the general rule, the I&I split, the RR rule, the Santé minimum of five labelled courses plus three free choices, the Opening 2.5 ECTS pairing, and the double-degree shape (six MVA modules, two Modelling and two Learning, two home-school modules, no per-semester constraint, partner schools ENSAE, ENSTA, Mines, CentraleSupélec).

Two catalogue sentences are not on that page.

- The catalogue says the final transcript keeps the 8 best marks. The fetched validation page does not say this.
- The catalogue says one Santé course may be replaced by the hospital-immersion project. The fetched validation page does not say this. The hospital page in these notes does. Its fiche says that in the Santé track the module may replace one course, and it points at master-mva.com for the module.

The catalogue calendar says the refresher fortnight is optional, without registration, and mandatory for the I&I track. That sentence is on the planning record, not on the validation page.

## Counts

The catalogue lists 71 courses. Kinds: 64 science, 4 non-science, 3 refresher. Labels on the courses that have one: 29 Learning, 32 Modelling, 4 Opening. Six courses have an empty label list: `s0-refresher-probability-statistics`, `s0-refresher-linear-algebra-optimization`, `s0-refresher-python-scientific-computing`, `year-hospital-immersion`, `s2-reproducible-research-project`, `s3-research-internship`. Tracks: 14 Santé, 5 I&I, 2 RR. A course can carry a track and a Learning or Modelling label at the same time. Kernel Methods does. It is Learning and Santé.

Page state today: 37 full notes, 15 skeletons, 4 framing pages, 3 refreshers, 12 missing.

ECTS values that actually occur are 0 (the three refreshers), 2.5, 5, and 20 (the internship).

## Half modules

The validation rule that two 2.5 ECTS courses make one module is stated for courses labelled Opening. The catalogue rows at 2.5 ECTS are these.

- `s1-turing-seminar-ai-safety` is 2.5 ECTS, label Opening, page skeleton. Official title: Turing Seminar: An Introduction to AGI Safety.
- `s2-ai-cultural-heritage` is 2.5 ECTS, label Opening, page missing. Official title: Artificial Intelligence and Computer Vision for Cultural Heritage.
- `s2-regulating-ai` is 2.5 ECTS, label Opening, page framing. Official title: Regulating AI.
- `s2-ai-environment` is 2.5 ECTS, label Opening, page missing. Official title: Artificial Intelligence and the Environment.
- `s2-responsible-ml` is 2.5 ECTS, label Learning, page missing. Official title: Responsible Machine Learning.

`s2-responsible-ml` is the odd row. It is 2.5 ECTS and labelled Learning, and it has no page. This note does not decide whether it pairs with an Opening course or counts as half a Learning module. That decision needs the official fiche, which is not settled by the two sources above.

## The map

| Slug | Title | Semester | Label | Track | ECTS | Page |
|---|---|---|---|---|---|---|
| `s0-refresher-probability-statistics` | Refresher: Probability and Statistics for MVA | 0 | none | none | 0 | refresher |
| `s0-refresher-linear-algebra-optimization` | Refresher: Linear Algebra, Analysis and Optimization for MVA | 0 | none | none | 0 | refresher |
| `s0-refresher-python-scientific-computing` | Refresher: Scientific Python, NumPy and PyTorch for MVA | 0 | none | none | 0 | refresher |
| `s1-foundations-llms` | Foundations of Large Language Models | 1 | Learning | none | 5 | skeleton |
| `s1-stochastic-calculus-ml` | Stochastic Calculus in Machine Learning: Sampling and Generative Modelling | 1 | Modelling | none | 5 | skeleton |
| `s1-geometry-processing-gdl` | Geometry Processing and Geometric Deep Learning | 1 | Learning | none | 5 | full notes |
| `s1-extreme-values` | Statistical Learning with Extreme Values | 1 | Learning | none | 5 | skeleton |
| `s1-turing-seminar-ai-safety` | Turing Seminar: An Introduction to AGI Safety | 1 | Opening | none | 2.5 | skeleton |
| `s1-robotics` | Robotics | 1 | Modelling | none | 5 | full notes |
| `s1-geometric-data-analysis` | Geometric Data Analysis | 1 | Modelling | Santé | 5 | skeleton |
| `s1-reproducible-research` | Fundamentals of Reproducible Research and Free Software | 1 | Learning | RR | 5 | full notes |
| `s1-machine-intelligence-images` | The Machine Intelligence of Images | 1 | Modelling | I&I | 5 | full notes |
| `s1-ml-geosciences` | Statistical Learning for Scientific Imaging and Physical Measurements: Geosciences | 1 | Modelling | I&I | 5 | full notes |
| `s1-deep-learning-signal-industry` | Deep Learning and Signal Processing: Introduction and Industrial Applications | 1 | Modelling | I&I | 5 | full notes |
| `s1-time-series` | Machine Learning for Time Series | 1 | Modelling | none | 5 | full notes |
| `s1-theoretical-foundations-dl` | Theoretical Foundations of Deep Learning | 1 | Learning | none | 5 | full notes |
| `s1-distributed-optimization` | Foundations of Distributed and Large-Scale Computing Optimization | 1 | Learning | none | 5 | skeleton |
| `s1-deep-learning` | Deep Learning | 1 | Learning | none | 5 | skeleton |
| `s1-altegrad` | Advanced Learning for Text and Graph Data (ALTEGRAD) | 1 | Learning | none | 5 | full notes |
| `s1-intro-statistical-learning` | Introduction to Statistical Learning | 1 | Learning | none | 5 | full notes |
| `s1-optimal-transport-ml` | Optimal Transport for Machine Learning | 1 | Learning | none | 5 | skeleton |
| `s1-probabilistic-graphical-models` | Introduction to Probabilistic Graphical Models and Deep Generative Models | 1 | Learning | none | 5 | full notes |
| `s1-convex-optimization` | Convex Optimization and Applications in Machine Learning | 1 | Learning | none | 5 | skeleton |
| `s1-computational-statistics` | Computational Statistics | 1 | Learning | Santé | 5 | full notes |
| `s1-neuroscience-maths` | Mathematical Methods for Neuroscience | 1 | Modelling | Santé | 5 | full notes |
| `s1-image-denoising` | Image Denoising: the Human–Machine Competition | 1 | Modelling | none | 5 | full notes |
| `s1-3d-computer-vision` | 3D Computer Vision | 1 | Modelling | none | 5 | missing |
| `s1-sub-pixel-image-processing` | Sub-Pixel Image Processing | 1 | Modelling | none | 5 | full notes |
| `s1-object-recognition-cv` | Object Recognition and Computer Vision | 1 | Modelling | none | 5 | full notes |
| `s1-digital-photography` | Mathematical Models for Digital Photography | 1 | Modelling | none | 5 | full notes |
| `s1-medical-image-analysis` | Medical Image Analysis Based on Generative, Geometric and Biophysical Models | 1 | Modelling | Santé | 5 | full notes |
| `s1-tda-imaging-ml` | Topological Data Analysis for Imaging and Machine Learning | 1 | Modelling | none | 5 | skeleton |
| `year-hospital-immersion` | Hospital Immersion: Paired Project with a Physician | both | none | Santé | 5 | framing |
| `s2-physics-learning-uq` | Learning Physical Phenomena: Metamodelling and Uncertainty Quantification | 2 | Modelling | I&I | 5 | full notes |
| `s2-training-deploying-large-models` | Training and Deploying Large-Scale Models | 2 | Learning | none | 5 | full notes |
| `s2-multimodal-xai` | Multimodal Explainable AI (XAI) | 2 | Learning | none | 5 | full notes |
| `s2-ai-cultural-heritage` | Artificial Intelligence and Computer Vision for Cultural Heritage | 2 | Opening | none | 2.5 | missing |
| `s2-representation-learning-medical` | Representation Learning for Computer Vision and Medical Imaging | 2 | Learning | Santé | 5 | skeleton |
| `s2-llm-code-proof` | Large Language Models for Code and Proof | 2 | Learning | none | 5 | full notes |
| `s2-interactions` | Interactions: Complexity, Stochasticity, Extrema and Rare Events | 2 | Modelling | none | 5 | skeleton |
| `s2-protein-science` | Algorithms and Learning for Protein Science | 2 | Learning | Santé | 5 | missing |
| `s2-regulating-ai` | Regulating AI | 2 | Opening | none | 2.5 | framing |
| `s2-ai-environment` | Artificial Intelligence and the Environment | 2 | Opening | none | 2.5 | missing |
| `s2-stopping-times-online` | Stopping Times and Online Algorithms | 2 | Modelling | none | 5 | skeleton |
| `s2-reproducible-research-project` | Open Science in the Age of AI: Reproducible Research Project | 2 | none | RR | 5 | framing |
| `s2-network-optimization` | Algorithms for Network Optimization and Management | 2 | Modelling | I&I | 5 | full notes |
| `s2-reinforcement-learning` | Reinforcement Learning | 2 | Learning | none | 5 | skeleton |
| `s2-responsible-ml` | Responsible Machine Learning | 2 | Learning | none | 2.5 | missing |
| `s2-graphical-models-discrete` | Graphical Models: Discrete Inference and Learning | 2 | Learning | none | 5 | skeleton |
| `s2-deep-learning-medical-imaging` | Deep Learning for Medical Imaging | 2 | Learning | Santé | 5 | full notes |
| `s2-bayesian-ml` | Bayesian Machine Learning | 2 | Learning | none | 5 | full notes |
| `s2-dl-image-restoration-synthesis` | Deep Learning for Image Restoration and Synthesis | 2 | Learning | none | 5 | full notes |
| `s2-deep-learning-in-practice` | Deep Learning in Practice / Advanced Deep Learning | 2 | Learning | none | 5 | missing |
| `s2-sequential-learning` | Sequential Learning | 2 | Learning | none | 5 | missing |
| `s2-graphs-in-ml` | Graphs in Machine Learning | 2 | Learning | none | 5 | full notes |
| `s2-kernel-methods` | Kernel Methods for Machine Learning | 2 | Learning | Santé | 5 | full notes |
| `s2-random-matrices-ml` | Large Random Matrices and Applications to Machine Learning | 2 | Learning | none | 5 | full notes |
| `s2-speech-nlp` | Algorithms for Speech and Natural Language Processing | 2 | Modelling | none | 5 | missing |
| `s2-inverse-problems-imaging` | Inverse Problems and Imaging: Statistical and Stochastic Approaches | 2 | Modelling | Santé | 5 | full notes |
| `s2-shape-spaces` | Geometry and Shape Spaces | 2 | Modelling | Santé | 5 | full notes |
| `s2-audio-analysis-indexing` | Audio Signal Analysis, Indexing and Transformations | 2 | Modelling | none | 5 | missing |
| `s2-generative-models-images` | Generative Models for Images | 2 | Modelling | none | 5 | full notes |
| `s2-deformable-models-geodesics` | Deformable Models and Geodesic Methods for Image Analysis | 2 | Modelling | Santé | 5 | full notes |
| `s2-brain-imaging-bci` | Functional Brain Imaging and Brain–Computer Interfaces | 2 | Modelling | Santé | 5 | missing |
| `s2-point-clouds-3d` | Point Clouds and 3D Modelling (NPM3D) | 2 | Modelling | none | 5 | full notes |
| `s2-audio-time-frequency` | Audio Signal Processing: Time–Frequency Analysis | 2 | Modelling | none | 5 | missing |
| `s2-remote-sensing` | Remote Sensing Data: from Sensor to Large-Scale Geospatial Data Exploitation | 2 | Modelling | none | 5 | full notes |
| `s2-biostatistics` | Biostatistics | 2 | Modelling | Santé | 5 | full notes |
| `s2-diffusion-multiscale` | Diffusion and Multiscale Models in Artificial Intelligence | 2 | Modelling | none | 5 | full notes |
| `s2-detection-theory` | Detection Theory and Industrial Applications | 2 | Modelling | none | 5 | missing |
| `s3-research-internship` | Research Internship (4–6 months) | 3 | none | none | 20 | framing |

## Routes the home page already highlights

`tools/build_home.py` defines three example programmes of eight modules. `tools/check_gates.py` checks that each one has eight modules, at least 40 ECTS, at least four modules in semester 1, at least three in semester 2, at least two Learning and two Modelling. The home page calls each route reading guidance.

**Learning theory route.** `s1-convex-optimization` (skeleton, Learning, semester 1); `s1-theoretical-foundations-dl` (full notes, Learning, semester 1); `s1-optimal-transport-ml` (skeleton, Learning, semester 1); `s1-stochastic-calculus-ml` (skeleton, Modelling, semester 1); `s2-kernel-methods` (full notes, Learning, semester 2); `s2-sequential-learning` (missing, Learning, semester 2); `s2-random-matrices-ml` (full notes, Learning, semester 2); `s2-stopping-times-online` (skeleton, Modelling, semester 2).

**Vision and imaging route.** `s1-object-recognition-cv` (full notes, Modelling, semester 1); `s1-3d-computer-vision` (missing, Modelling, semester 1); `s1-deep-learning` (skeleton, Learning, semester 1); `s1-image-denoising` (full notes, Modelling, semester 1); `s2-dl-image-restoration-synthesis` (full notes, Learning, semester 2); `s2-generative-models-images` (full notes, Modelling, semester 2); `s2-point-clouds-3d` (full notes, Modelling, semester 2); `s2-remote-sensing` (full notes, Modelling, semester 2).

**Generative AI and LLM route.** `s1-foundations-llms` (skeleton, Learning, semester 1); `s1-deep-learning` (skeleton, Learning, semester 1); `s1-probabilistic-graphical-models` (full notes, Learning, semester 1); `s1-stochastic-calculus-ml` (skeleton, Modelling, semester 1); `s2-diffusion-multiscale` (full notes, Modelling, semester 2); `s2-llm-code-proof` (full notes, Learning, semester 2); `s2-training-deploying-large-models` (full notes, Learning, semester 2); `s2-reinforcement-learning` (skeleton, Learning, semester 2).

Several buttons highlight a module whose notes are not written.

- Learning theory still depends on skeletons for convex optimisation, optimal transport, and stochastic calculus in semester 1, and on stopping times in semester 2. Sequential learning is on the button and has no directory.
- Vision and imaging still depends on a skeleton for the semester 1 deep learning course. 3D computer vision is on the button and has no directory. The written imaging spine is object recognition, denoising, restoration and synthesis, generative models, point clouds, and remote sensing.
- Generative AI and LLM still depends on skeletons for foundations of large language models, deep learning, stochastic calculus, and reinforcement learning. The written spine is probabilistic graphical models, diffusion, LLMs for code and proof, and training large models.

## Tracks

**Santé.** Five Santé-labelled courses are the official minimum, plus three free choices. The hospital page says the immersion may replace one course. Full Santé notes already cover more than five courses: computational statistics, neuroscience, medical image analysis, deep learning for medical imaging, kernel methods, inverse problems, shape spaces, deformable models, and biostatistics. Still thin or absent: `s1-geometric-data-analysis` (skeleton), `s2-representation-learning-medical` (skeleton), `s2-protein-science` (missing), `s2-brain-imaging-bci` (missing). Kernel Methods is the bridge from the learning-theory notes into the Santé count. A student can use it as one of the five Santé courses and as one of the two Learning courses.

**I&I.** The official minimum is two I&I modules, plus at least two Learning courses and two Modelling courses chosen outside I&I. All five I&I courses are Modelling, and all five have full notes: `s1-machine-intelligence-images`, `s1-ml-geosciences`, `s1-deep-learning-signal-industry`, `s2-physics-learning-uq`, `s2-network-optimization`. Written Learning courses outside I&I, usable for the Learning quota, include `s1-geometry-processing-gdl`, `s1-reproducible-research`, `s1-theoretical-foundations-dl`, `s1-altegrad`, `s1-intro-statistical-learning`, `s1-probabilistic-graphical-models`, `s1-computational-statistics`, `s2-training-deploying-large-models`, `s2-multimodal-xai`, `s2-llm-code-proof`, `s2-deep-learning-medical-imaging`, `s2-bayesian-ml`, `s2-dl-image-restoration-synthesis`, `s2-graphs-in-ml`, `s2-kernel-methods`, `s2-random-matrices-ml`. There are 16 full Modelling notes outside I&I. The track is feasible on the pages that exist. The refresher fortnight is mandatory for this track in the catalogue calendar, and those three pages are refreshers rather than science courses.

**RR.** Validating one or two RR modules places the student in the track. Both modules have pages. `s1-reproducible-research` is full notes, labelled Learning. `s2-reproducible-research-project` is a framing page, with no Learning or Modelling label, and its official assessment is a reproducible article (IPOL pre-print, code, demo) plus a review of another group. The framing page links to `s2-detection-theory`, which has no directory.

## Gaps and missing bridges

**Unwritten route joints.** The theory route's semester 1 tools (convex optimisation, optimal transport, stochastic calculus) are skeletons, and sequential learning has no page. A reader of the finished Kernel Methods and random-matrix notes cannot yet follow the route the home button draws.

**Unwritten language-model joint.** Foundations of large language models is a skeleton. Speech and NLP has no page. The semester 2 notes on code, proof, and large-model training are full. The bridge from a first transformer course into those notes is not written.

**3D vision.** Object recognition, geometry processing, point clouds, shape spaces, and deformable models are full notes. The semester 1 course 3D computer vision, which the vision route lists, has no directory. Point clouds and geometry processing are written, and the catalogue still lists 3D computer vision as its own module.

**Audio.** `s2-audio-analysis-indexing` and `s2-audio-time-frequency` have no directories. Nothing else in the catalogue is an audio course. There is no written bridge.

**Discrete graphical models.** `s1-probabilistic-graphical-models` is full notes. `s2-graphical-models-discrete` is a skeleton. The semester 2 continuation is named and not written.

**Online learning.** `s2-sequential-learning` is missing and `s2-stopping-times-online` is a skeleton. The theory route lists both.

## Redundancies worth knowing before choosing eight modules

9 full notes list Image processing or Computer Vision among their catalogue domains. The pages form a stack, from formation and denoising through recognition, restoration, and generation. A student who stays inside that stack meets the Modelling minimum and can still miss the two Learning courses.

Several courses share the words "deep learning" and play different roles. `s1-theoretical-foundations-dl` is the Learning theory page and it is written. `s1-deep-learning` is a skeleton on the vision and generative routes. `s1-deep-learning-signal-industry` is an I&I Modelling page and it is written. `s2-deep-learning-medical-imaging` is Santé and written. `s2-training-deploying-large-models` is written. `s2-deep-learning-in-practice` has no directory. Taking the theory page and the large-model page is a bridge. Taking two introductory deep-learning pages, once the skeletons exist, would repeat the same entry.

## Backlog

1. Add the twelve missing directories with `tools/new_course.py`. Do not invent a UE code, an instructor, or an assessment line. The slugs are `s1-3d-computer-vision`, `s2-ai-cultural-heritage`, `s2-protein-science`, `s2-ai-environment`, `s2-responsible-ml`, `s2-deep-learning-in-practice`, `s2-sequential-learning`, `s2-speech-nlp`, `s2-audio-analysis-indexing`, `s2-brain-imaging-bci`, `s2-audio-time-frequency`, `s2-detection-theory`.
2. Replace the fifteen skeletons. Start with the ones a home-page route already highlights: `s1-foundations-llms`, `s1-stochastic-calculus-ml`, `s1-deep-learning`, `s1-optimal-transport-ml`, `s1-convex-optimization`, `s2-stopping-times-online`, `s2-reinforcement-learning`. The other skeletons are `s1-extreme-values`, `s1-turing-seminar-ai-safety`, `s1-geometric-data-analysis`, `s1-distributed-optimization`, `s1-tda-imaging-ml`, `s2-representation-learning-medical`, `s2-interactions`, `s2-graphical-models-discrete`.
3. Write `s1-3d-computer-vision` and `s2-sequential-learning` before treating the vision and theory routes as readable end to end.
4. Ask the programme, with the fiche in hand, how `s2-responsible-ml` (2.5 ECTS, Learning) interacts with the Opening pairing rule. Do not guess in the catalogue.
5. When `s2-detection-theory` exists, check the link from `s2-reproducible-research-project`. Until then the link points at a missing page.
6. Point GitHub Pages at `master` only after `master` contains the notes. On 23 October 2026 the Pages API reported branch `ccr-35a7ca30-pszhhr`. This repository's `master` was still `75b32eb`.

The end-of-year proposals that can be read on the pages that exist are in `projects/index.qmd`. They link only to course pages that are in the tree. They do not replace the official assessment of any course.
