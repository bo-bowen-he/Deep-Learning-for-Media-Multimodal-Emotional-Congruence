# Deep-Learning-for-Media-Multimodal-Emotional-Congruence
Multimodal Emotional Congruence in Music, Album Art, and Lyrics with ImageBind, Clip, Clap, and MERT. 


A 5-person Spring 2026 Deep Learning project asking a single question: **do
generalist and specialist multimodal models perceive emotion the same way across
audio, album art, and lyrics?** We test it on 150 curated tracks across 6
emotion categories, using one generalist encoder (ImageBind) and three modality
specialists (MERT for audio, CLIP for image, CLAP for lyrics).

---

## 1. Project goals

The literature treats cross-modal alignment mostly in the caption-image domain;
music-and-art-and-lyrics is comparatively under-tested. We want to know:

1. **Does cross-modal emotional alignment exist in music?** If audio of a
   track is "close" to its album cover and lyrics in a shared embedding space,
   that alignment should be detectable as a cosine signal above chance.
2. **Does the generalist (ImageBind) recover the same structure as three
   modality specialists?** If yes, alignment is not modality-specific.
   If no, the gap reveals what specialization actually buys you.
3. **What does each encoder actually cluster the 150 tracks by?** Do they
   organize by emotion, or by something simpler like genre, contributor, or
   instrumentation?
4. **Does better audio / lyric sampling improve the emotion signal?** Both
   ImageBind audio and CLAP/ImageBind text use windowed inputs (2 s clip, 77
   tokens). We test alternative samplers to see if the encoders were missing
   emotional content via truncation.
5. **Can we recover continuous valence-arousal coordinates from the
   embeddings?** Anchor-based V-A regression as a probe for category
   separability.

---

## 2. Data

We curated **150 songs** spanning **6 emotion categories** (25 tracks per
category):

| Emotion category | Anchor V-A position |
|---|---|
| Vital & Joyful                    | (+0.85, +0.85) |
| Tender & Intimacy                 | (+0.70, −0.70) |
| Awe, Beauty & Transcendence       | (+0.90, +0.10) |
| Tension, Threat & Aggression      | (−0.80, +0.80) |
| Sadness, Loss & Lament            | (−0.75, −0.75) |
| Dreaminess, Curiosity & Ambiguity | ( 0.00,  0.00) |

Each of the 5 team members curated 30 tracks (6 per category), giving us a
built-in inter-rater check on the labels. Each track has three artifacts:
the audio (`.wav`), the album cover (`.jpg`), and the lyrics (`.txt`,
capped at 1000 characters in standardization). Track titles, artists, and
genre tags live in `raw_data_labels.xlsx` and `metadata.csv`.

**Raw data access.** The audio, image, and lyric files are commercial copyrighted
material and are NOT redistributed in this repo. The 150-track manifest with
artists and titles is included; reproduce by sourcing the audio yourself,
or contact the team for the private dataset link.
For grading: the private Drive folder is at **[paste Drive link here]**.

---

## 3. Code structure

Eight Colab-runnable Jupyter notebooks, each owned by one of the five leads.
Run order is **01 → 02 → 02b → 03 → 04 → 05 → 06**, then **07 / 07.5** as
optional extensions.

| Notebook | What it does | Owner |
|---|---|---|
| `01_Data_Standardization_and_Manifest.ipynb` | Reads raw audio/images/lyrics, standardizes formats (16 kHz mono wav, fixed image dim, 1000-char lyric cap), writes `metadata.csv`. | Bowen |
| `02_Audio_Feature_Extraction_ImageBind_MERT.ipynb` | Extracts ImageBind audio (1024-d) and MERT-v1-95M (768-d) embeddings for all 150 tracks. | Jiexin |
| `02b_Audio_Exploration.ipynb` | Inline audio diagnostics: waveforms, spectrograms, embedding norm distributions. | Jiexin |
| `03_Visual_Feature_Extraction_ImageBind_CLIP.ipynb` | Extracts ImageBind image (1024-d) and CLIP ViT-B/32 (512-d) embeddings for all 150 covers. | Sabria |
| `04_Text_Sentiment_and_Lyric_Embeddings_ImageBind_CLAP.ipynb` | RoBERTa GoEmotions sentiment + ImageBind text (1024-d) + CLAP HTSAT-tiny text (512-d) embeddings. | Olivia |
| `05_Cross_Modal_Similarity_and_Retrieval.ipynb` | Per-track cosine congruence (A↔V, A↔L, master), CKA / RSA / Procrustes between encoders, Recall@K retrieval, 1-NN confusion matrix. | Jazlyn |
| `06_UMAP_Visualizations_and_Final_Analysis.ipynb` | UMAP grids, V-A circumplex constellations, V-A regression probe, per-model silhouette + 1-NN purity. | Bowen |
| `07_Exploration.ipynb` | Additive 5-method analysis with two new audio samplers (random K-mean + energy-peak) across 3 random seeds. | Bowen |
| `07.5_Exploration_Text_and_Audio.ipynb` | Extends 07 with chorus + multi-segment lyric resampling and an anchor-based V-A regression probe across 14 encoder spaces × 3 seeds. | Bowen |

**Folder layout:**

- `02_Embeddings/` — 6 original `.npy` embedding sets (1 per encoder).
- `03_Final_Results/` — CSVs and figures from the canonical pipeline run
  (`final_similarity_report.csv`, `category_performance.csv`,
  `subcategory_performance.csv`, `generalist_vs_specialist.csv`,
  `retrieval_recall.csv`, `sentiment_results.csv`, plus 10 figure PNGs).
- `04_Visual_Checks/` — inline-rendered figures from individual notebook runs.
- `Explorations/` — 3 seed runs of `07_Exploration.ipynb` (audio resampling).
- `Explorations 2.0/` — 3 seed runs of `07.5_Exploration_Text_and_Audio.ipynb`
  (audio + lyric resampling + V-A probe).
- `Documents/` — preflight summary, per-notebook triage notes, changelog.
- `DL_Project_2026_Presentation.pptx` — 18-slide deck for the team talk.
- `DL_Project_2026_Speaker_Notes.docx` — companion verbatim script for each slide.
- `dl_project_2026_report.html` — self-contained HTML report with all figures
  embedded as base64. Best entry point for graders.

**Reproducibility.** Random seed pinned (default `SEED=42`). The
`Explorations 2.0/` runs use seeds 42, 65, 18 — cross-seed standard deviation
on every headline metric is below 0.015, so findings are stable across
random sampling.

---

## 4. Summary of results

**The headline question — yes, cross-modal alignment exists in music.**
Across 150 tracks: mean audio↔visual cosine = **0.180** (max 0.365), mean
audio↔lyric cosine = **0.138**. Audio→image 1-NN retrieval is **8.7% R@1**
(13× chance of 0.7%), 20.7% R@5, 34.0% R@10. Pearson correlation between A↔V
and A↔L per track = **0.255 (t = 3.21, df = 148, p < 0.002)** — convergent
tracks are convergent on both bridges.

**Per-category congruence ranking is sharp and stable:**

| Category | A↔V | A↔L | Master |
|---|---|---|---|
| Tension, Threat & Aggression      | **0.212** | 0.145 | 0.179 |
| Tender & Intimacy                 | 0.192 | **0.162** | 0.177 |
| Vital & Joyful                    | 0.186 | 0.120 | 0.153 |
| Awe, Beauty & Transcendence       | 0.164 | 0.142 | 0.153 |
| Sadness, Loss & Lament            | 0.164 | 0.144 | 0.154 |
| Dreaminess, Curiosity & Ambiguity | 0.159 | 0.116 | 0.137 |

**Cross-encoder space alignment** (CKA / RSA / Procrustes R² between
generalist and specialist):

| Modality pair | CKA | RSA Spearman | Procrustes R² |
|---|---|---|---|
| Image: ImageBind vs CLIP | **0.756** | 0.348 | **0.807** |
| Audio: ImageBind vs MERT | 0.551 | 0.414 | −1.211 |
| Text:  ImageBind vs CLAP | 0.456 | 0.400 | 0.345 |

**Image is the strongest modality** — CLIP and ImageBind-image agree more
than any other encoder pair. Album-cover designers encode emotion intentionally,
and that signal is the most legible to the models.

**The deeper structure is genre, not emotion.** Silhouette by emotion is
**negative across all 14 encoder spaces** (best is image_clip at −0.026).
Block contrast in the 150×150 cosine matrices favors `genre_top` over
`emotion` by ~2× in 9 of 10 encoders. What looks like emotion clustering is
mostly the genre↔emotion correlation in our dataset leaking through.

**Sampling matters where the encoder was windowing.** Replacing ImageBind
audio's mid-clip with energy-peak windows lifts k-means purity on emotion
from +0.136 to **+0.182 (+33%)**. Replacing CLAP's first-77-token lyric slice
with multi-segment K=4 chunks lifts it from +0.116 to **+0.153 (+32%)**. MERT
and ImageBind text — both of which already cover most of the input — barely move.

**V-A regression is uniformly negative.** Best leave-one-out R² across 14
encoder spaces is **−0.142** (text_ib). All encoders predict the anchor V-A
worse than the mean of the targets. Caveat: V-A targets are 6 fixed Russell
anchor coordinates, not human-rated continuous V-A — this measures category
separability projected onto V-A axes, not free continuous valence-arousal
estimation.

**The take-away.** The encoders see genre clearly, emotion only indirectly,
and valence-arousal axes not at all. Cross-modal alignment is real — but
it's the alignment of genre, with emotion as a thin overlay on top.

---

## 5. Team and responsibilities

| Member | Role | Notebooks | Slides |
|---|---|---|---|
| **Bowen** | Project Lead · Data Lead · UMAP & Final Analysis · Exploration Lead | nb01, nb06, nb07, nb07.5 | intro, exploration block, limitations, methods |
| **Jiexin** | Audio Specialist | nb02, nb02b | audio modality + results |
| **Sabria** | Visual Lead | nb03 | visual modality + results |
| **Olivia** | Text / Lyrics Lead | nb04 | text modality + results |
| **Jazlyn** | Cross-Modal Similarity Lead | nb05 | methods + cross-modal results |
| All five | synthesis | — |

The track curation (30 tracks per person × 5 people) gave us a built-in
inter-rater check — contributor `mc_mean` ranged from 0.154 to 0.164, well
within the cross-seed noise floor, so the labels are not contaminated by
contributor-specific style.

---

## License
[MIT](LICENSE) — Code, notebooks, and results may be reused with attribution.
Raw audio, album-cover images, and lyrics are NOT licensed for redistribution
under any terms; they remain the property of their respective copyright holders.
