# Exploration run · 2026-05-06_04-53

- N tracks: **150**
- Encoder spaces analysed: **14**  (audio_ib_orig, audio_ib_random, audio_ib_energy, audio_mert_orig, audio_mert_random, audio_mert_energy, image_ib, image_clip, text_ib, text_ib_chorus, text_ib_multi, text_clap, text_clap_chorus, text_clap_multi)
- Label schemes: **6**  (emotion, subcategory, contributor, genre_top, vocal, duration_bucket)
- Re-extraction: **enabled**  (K=5 clips per track)

## What does each encoder actually organize by?
Per encoder, we report the top label scheme by silhouette and by block contrast.  When both methods agree, that's a strong signal.

| Encoder | Top label by silhouette | silhouette | Top label by block contrast | Δ |
|---|---|---|---|---|
| `audio_ib_orig` | contributor | -0.037 | genre_top | +0.085 |
| `audio_ib_random` | contributor | -0.037 | genre_top | +0.084 |
| `audio_ib_energy` | contributor | -0.033 | genre_top | +0.090 |
| `audio_mert_orig` | contributor | -0.046 | genre_top | +0.011 |
| `audio_mert_random` | contributor | -0.050 | genre_top | +0.009 |
| `audio_mert_energy` | contributor | -0.046 | genre_top | +0.011 |
| `image_ib` | contributor | -0.026 | genre_top | +0.023 |
| `image_clip` | contributor | -0.025 | genre_top | +0.014 |
| `text_ib` | contributor | -0.021 | genre_top | +0.023 |
| `text_ib_chorus` | contributor | -0.032 | subcategory | +0.012 |
| `text_ib_multi` | contributor | -0.024 | genre_top | +0.024 |
| `text_clap` | contributor | -0.063 | subcategory | +0.013 |
| `text_clap_chorus` | contributor | -0.041 | subcategory | +0.011 |
| `text_clap_multi` | contributor | -0.066 | subcategory | +0.019 |

## Did the new audio + lyric sampling change anything?
Compare the silhouette by emotion across the three audio_ib variants and three audio_mert variants:

### audio_ib
| Variant | silhouette by emotion | silhouette by genre_top | Δ block-contrast emotion |
|---|---|---|---|
| `audio_ib_orig` | -0.047 | -0.127 | +0.033 |
| `audio_ib_random` | -0.049 | -0.128 | +0.042 |
| `audio_ib_energy` | -0.057 | -0.096 | +0.042 |

### audio_mert
| Variant | silhouette by emotion | silhouette by genre_top | Δ block-contrast emotion |
|---|---|---|---|
| `audio_mert_orig` | -0.077 | -0.150 | +0.005 |
| `audio_mert_random` | -0.076 | -0.159 | +0.005 |
| `audio_mert_energy` | -0.086 | -0.161 | +0.005 |

### text_ib
| Variant | silhouette by emotion | silhouette by genre_top | Δ block-contrast emotion |
|---|---|---|---|
| `text_ib` | -0.029 | -0.059 | +0.006 |
| `text_ib_chorus` | -0.048 | -0.070 | +0.005 |
| `text_ib_multi` | -0.032 | -0.075 | +0.008 |

### text_clap
| Variant | silhouette by emotion | silhouette by genre_top | Δ block-contrast emotion |
|---|---|---|---|
| `text_clap` | -0.078 | -0.179 | +0.009 |
| `text_clap_chorus` | -0.065 | -0.196 | +0.009 |
| `text_clap_multi` | -0.083 | -0.171 | +0.014 |

## Does any modality align with our subjective emotional labeling?
| Encoder | silhouette by emotion |
|---|---|
| `image_clip` | -0.026 |
| `text_ib` | -0.029 |
| `text_ib_multi` | -0.032 |
| `image_ib` | -0.036 |
| `audio_ib_orig` | -0.047 |
| `text_ib_chorus` | -0.048 |
| `audio_ib_random` | -0.049 |
| `audio_ib_energy` | -0.057 |
| `text_clap_chorus` | -0.065 |
| `audio_mert_random` | -0.076 |
| `audio_mert_orig` | -0.077 |
| `text_clap` | -0.078 |
| `text_clap_multi` | -0.083 |
| `audio_mert_energy` | -0.086 |

**Best encoder for emotion: `image_clip` with silhouette -0.026.**
Interpretation: ❌ no meaningful clustering by emotion (rule of thumb: silhouette > 0.10 = real clustering, > 0.25 = strong).

## Cross-encoder disagreement (top-5 neighbor Jaccard)
Lower = encoders see different things.

| Encoder pair | Jaccard |
|---|---|
| `audio_mert_random`  ×  `text_clap` | 0.02 |
| `image_ib`  ×  `text_clap` | 0.02 |
| `image_clip`  ×  `text_ib` | 0.02 |
| `audio_ib_orig`  ×  `text_clap_chorus` | 0.02 |
| `audio_mert_orig`  ×  `text_clap` | 0.02 |
| `audio_mert_random`  ×  `text_ib` | 0.02 |
| `audio_mert_energy`  ×  `text_ib_chorus` | 0.02 |
| `audio_mert_energy`  ×  `text_clap` | 0.02 |
| `image_ib`  ×  `text_clap_chorus` | 0.02 |
| `audio_ib_orig`  ×  `text_ib_chorus` | 0.02 |

## V-A regression — anchor-based, leave-one-out R²
Targets are the 6 Russell anchors, so this measures how well each encoder separates emotion categories along V-A axes (NOT free continuous V-A).

| Encoder | R² valence | R² arousal | R² overall | mean anchor err |
|---|---|---|---|---|
| `text_ib` | -0.275 | -0.009 | -0.142 | 0.918 |
| `text_ib_multi` | -0.284 | -0.288 | -0.286 | 0.967 |
| `text_ib_chorus` | -0.684 | -0.420 | -0.552 | 1.090 |
| `image_clip` | -0.548 | -0.623 | -0.586 | 1.091 |
| `audio_mert_orig` | -0.762 | -0.647 | -0.704 | 1.114 |
| `image_ib` | -0.901 | -0.573 | -0.737 | 1.169 |
| `audio_mert_energy` | -0.673 | -0.887 | -0.780 | 1.134 |
| `audio_mert_random` | -0.678 | -1.137 | -0.907 | 1.176 |
| `audio_ib_orig` | -1.171 | -0.894 | -1.033 | 1.221 |
| `audio_ib_energy` | -1.574 | -0.663 | -1.118 | 1.251 |
| `audio_ib_random` | -1.093 | -1.404 | -1.248 | 1.281 |
| `text_clap_multi` | -1.720 | -1.301 | -1.510 | 1.362 |
| `text_clap_chorus` | -1.513 | -2.119 | -1.816 | 1.422 |
| `text_clap` | -3.114 | -1.163 | -2.138 | 1.520 |

**Best V-A encoder: `text_ib` (R² overall = -0.142) — weak V-A signal — barely above category-mean prediction.**

Pre vs post sampling on V-A R²:
- `audio_ib` baseline R² = -1.033 →  audio_ib_energy: -1.118 (Δ -0.086) · audio_ib_random: -1.248 (Δ -0.215)
- `audio_mert` baseline R² = -0.704 →  audio_mert_energy: -0.780 (Δ -0.076) · audio_mert_random: -0.907 (Δ -0.203)
- `text_ib` baseline R² = -0.142 →  text_ib_multi: -0.286 (Δ -0.143) · text_ib_chorus: -0.552 (Δ -0.410)
- `text_clap` baseline R² = -2.138 →  text_clap_multi: -1.510 (Δ +0.628) · text_clap_chorus: -1.816 (Δ +0.322)

## Output files in this run
### `embeddings/`
- `audio_ib_energy.npy`
- `audio_ib_random.npy`
- `audio_mert_energy.npy`
- `audio_mert_random.npy`
- `labels.csv`
- `lyric_chorus_log.csv`
- `text_clap_chorus.npy`
- `text_clap_multi.npy`
- `text_ib_chorus.npy`
- `text_ib_multi.npy`

### `results/`
- `VA1_regression_loocv.csv`
- `method1_kmeans_purity.csv`
- `method2_diagnostic_neighbors.txt`
- `method2_neighbors_full.csv`
- `method3_silhouette_heatmap.csv`
- `method4_disagreement_topK.csv`
- `method4_jaccard_matrix.csv`
- `method5_blocksort_summary.csv`

### `figures/`
- `VA2_R2_bar_per_encoder.png`
- `VA2_pre_post_audio_ib_orig_vs_audio_ib_energy.png`
- `VA2_pre_post_text_clap_vs_text_clap_chorus.png`
- `method1_purity_heatmap.png`
- `method3_silhouette_heatmap.png`
- `method4_jaccard_heatmap.png`
- `method5_blocksort_audio_ib_orig.png`
- `method5_blocksort_audio_mert_orig.png`
- `method5_blocksort_image_clip.png`
- `method5_blocksort_image_ib.png`
- `method5_blocksort_text_ib.png`
