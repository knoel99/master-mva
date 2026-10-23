# Commit evolution through 23 October 2026

This note reads the git history of `master` and of `ccr-35a7ca30-pszhhr` as it stood at `65ff71f`. Every hash below is a commit on one of those two refs. The count is twelve commits. `master` contains only the first. The other eleven are on the work-in-progress branch. Later commits are outside this note.

The dates and subjects are the ones `git log` prints. The file counts are from `git diff-tree` and `git show --shortstat` on those commits.

## The twelve commits

| Hash | Date | Subject | What the diff contains |
|---|---|---|---|
| `75b32eb` | 22 October 2026 | Initial commit | `LICENSE` and `README.md` only. This commit is `master`. |
| `cb8cf26` | 22 October 2026 | Scaffold the MVA notes site from the final LLGA framework | 29 paths. Added the catalogue, the contracts under `specs/`, the tools, the theme assets, `AGENTS.md`, and `.nojekyll`. No course page yet. |
| `896660b` | 22 October 2026 | Framing pages (hospital immersion, Regulating AI, reproducible-research project, internship), generated home page; pilot page in progress | 10 added paths, including `index.html` and the first five course sources. |
| `fb17230` | 22 October 2026 | WIP: course pages being written (pilot Kernel Methods and first batch) | 17 paths under `courses/`. Sixteen science sources appear here for the first time. |
| `f3b931f` | 22 October 2026 | Kernel Methods for Machine Learning: full page (pilot), written and independently reviewed | 13 paths under `courses/`. The Kernel Methods source was already in the tree. This commit is the one whose subject calls that page finished and reviewed. |
| `19f35b3` | 22 October 2026 | WIP: pages in progress | One file, `courses/s1-deep-learning-signal-industry/index.qmd` (3 insertions, 1 deletion). |
| `7c5e2f0` | 22 October 2026 | WIP: pages being written and edited by agents | 79 paths under `courses/` (63 added, 16 modified). Thirty-one course sources appear here for the first time. |
| `b061483` | 22 October 2026 | WIP: pages being written and edited by agents | 3 paths. The topological data analysis source appears here for the first time. |
| `1c797b3` | 23 October 2026 | Fix duplicated 'assumed' prefix in the volume row of the skeleton tool and three pages; pages in progress | 10 paths, including `tools/new_course.py`. |
| `0d2ebf2` | 23 October 2026 | WIP: pages in progress | 3 paths. The linear-algebra refresher and the Turing seminar appear here for the first time. |
| `67f25b2` | 23 October 2026 | WIP: pages in progress | 18 paths under `courses/` (7463 insertions, 212 deletions). Four sources appear here for the first time. |
| `65ff71f` | 23 October 2026 | WIP: pages in progress | 4 modified course sources (279 insertions, 36 deletions). This is the tip of `ccr-35a7ca30-pszhhr`. |

## What each phase unlocked

**An empty repository.** `75b32eb` puts the licence and the readme on `master`. Nothing in the site can be served from `master` alone.

**A contract and a catalogue.** `cb8cf26` unlocks the structural source `data/catalog-2026-2027.json`, the page contracts, and the generators and gates (`tools/new_course.py`, `tools/render.py`, `tools/build_home.py`, `tools/check_gates.py`). Course prose is still impossible to publish, because no course directory exists.

**A home page and the non-science frames.** `896660b` unlocks the generated home page and the four framing pages (hospital immersion, Regulating AI, the reproducible-research project, the internship). It also adds the Kernel Methods source, which the subject line still calls a pilot in progress. A reader can see the year, and cannot yet read a finished science course.

**The first science sources.** `fb17230` unlocks sixteen science directories, still under a work-in-progress subject. The batch is eleven semester 1 sources and five semester 2 sources (restoration, physics and uncertainty, point clouds, remote sensing, and large-model training).

**One finished pilot.** `f3b931f` is the first commit whose subject says a science page is complete. The page is Kernel Methods. The subject also says the page was independently reviewed. That claim lives in the commit message. This note does not re-do the review.

**The bulk of the tree.** `19f35b3` is a one-file edit and does not unlock a new page. `7c5e2f0` unlocks most of the remaining directories, full notes and skeletons together. The subject line does not distinguish them. `b061483` unlocks the topological data analysis source.

**A tool fix, then more unfinished pages.** `1c797b3` unlocks a correction in the skeleton generator. The subject names a duplicated "assumed" prefix in the volume row. `0d2ebf2` and `67f25b2` unlock the three refresher sources, the Turing seminar, convex optimisation, and optimal transport. `65ff71f` edits four existing sources and adds no new course.

## What is still unfinished at this tip

At `65ff71f` the catalogue has 71 courses. Thirty-seven science pages are long notes with a projects section. Fifteen science pages are short skeletons whose source still contains the placeholder TODO. Twelve catalogue courses have no directory.

The twelve missing directories are `s1-3d-computer-vision`, `s2-ai-cultural-heritage`, `s2-ai-environment`, `s2-audio-analysis-indexing`, `s2-audio-time-frequency`, `s2-brain-imaging-bci`, `s2-deep-learning-in-practice`, `s2-detection-theory`, `s2-protein-science`, `s2-responsible-ml`, `s2-sequential-learning`, and `s2-speech-nlp`.

The fifteen skeletons are `s1-convex-optimization`, `s1-deep-learning`, `s1-distributed-optimization`, `s1-extreme-values`, `s1-foundations-llms`, `s1-geometric-data-analysis`, `s1-optimal-transport-ml`, `s1-stochastic-calculus-ml`, `s1-tda-imaging-ml`, `s1-turing-seminar-ai-safety`, `s2-graphical-models-discrete`, `s2-interactions`, `s2-reinforcement-learning`, `s2-representation-learning-medical`, and `s2-stopping-times-online`.

At `65ff71f` there is no `projects/index.qmd`. The home page already links to `projects/index.html`.

GitHub Pages for this repository, read on 23 October 2026 from the repository pages API, builds branch `ccr-35a7ca30-pszhhr` at path `/`. The published site is `https://knoel99.github.io/master-mva/`. On that date `master` is only `75b32eb`, so a Pages setting that follows `master` would not serve the notes until `master` advances.
