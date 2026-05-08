# Exploration run · 2026-05-05_14-38

- N tracks: **150**
- Encoder spaces analysed: **10**  (audio_ib_orig, audio_ib_random, audio_ib_energy, audio_mert_orig, audio_mert_random, audio_mert_energy, image_ib, image_clip, text_ib, text_clap)
- Label schemes: **6**  (emotion, subcategory, contributor, genre_top, vocal, duration_bucket)
- Re-extraction: **enabled**  (K=5 clips per track)

## What does each encoder actually organize by?
Per encoder, we report the top label scheme by silhouette and by block contrast.  When both methods agree, that's a strong signal.

| Encoder | Top label by silhouette | silhouette | Top label by block contrast | Δ |
|---|---|---|---|---|
| `audio_ib_orig` | contributor | -0.037 | genre_top | +0.085 |
| `audio_ib_random` | contributor | -0.026 | genre_top | +0.081 |
| `audio_ib_energy` | contributor | -0.033 | genre_top | +0.090 |
| `audio_mert_orig` | contributor | -0.046 | genre_top | +0.011 |
| `audio_mert_random` | contributor | -0.049 | genre_top | +0.011 |
| `audio_mert_energy` | contributor | -0.046 | genre_top | +0.011 |
| `image_ib` | contributor | -0.026 | genre_top | +0.023 |
| `image_clip` | contributor | -0.025 | genre_top | +0.014 |
| `text_ib` | contributor | -0.021 | genre_top | +0.023 |
| `text_clap` | contributor | -0.063 | subcategory | +0.013 |

## Did the new audio sampling change anything?
Compare the silhouette by emotion across the three audio_ib variants and three audio_mert variants:

### audio_ib
| Variant | silhouette by emotion | silhouette by genre_top | Δ block-contrast emotion |
|---|---|---|---|
| `audio_ib_orig` | -0.047 | -0.127 | +0.033 |
| `audio_ib_random` | -0.057 | -0.114 | +0.037 |
| `audio_ib_energy` | -0.057 | -0.096 | +0.042 |

### audio_mert
| Variant | silhouette by emotion | silhouette by genre_top | Δ block-contrast emotion |
|---|---|---|---|
| `audio_mert_orig` | -0.077 | -0.150 | +0.005 |
| `audio_mert_random` | -0.083 | -0.145 | +0.005 |
| `audio_mert_energy` | -0.086 | -0.161 | +0.005 |

## Does any modality align with our subjective emotional labeling?
| Encoder | silhouette by emotion |
|---|---|
| `image_clip` | -0.026 |
| `text_ib` | -0.029 |
| `image_ib` | -0.036 |
| `audio_ib_orig` | -0.047 |
| `audio_ib_random` | -0.057 |
| `audio_ib_energy` | -0.057 |
| `audio_mert_orig` | -0.077 |
| `text_clap` | -0.078 |
| `audio_mert_random` | -0.083 |
| `audio_mert_energy` | -0.086 |

**Best encoder for emotion: `image_clip` with silhouette -0.026.**
Interpretation: ❌ no meaningful clustering by emotion (rule of thumb: silhouette > 0.10 = real clustering, > 0.25 = strong).

## Cross-encoder disagreement (top-5 neighbor Jaccard)
Lower = encoders see different things.

| Encoder pair | Jaccard |
|---|---|
| `image_ib`  ×  `text_clap` | 0.02 |
| `image_clip`  ×  `text_ib` | 0.02 |
| `audio_mert_orig`  ×  `text_clap` | 0.02 |
| `audio_mert_energy`  ×  `text_clap` | 0.02 |
| `audio_ib_random`  ×  `text_ib` | 0.02 |
| `audio_mert_orig`  ×  `text_ib` | 0.02 |
| `audio_mert_random`  ×  `text_clap` | 0.02 |
| `audio_mert_energy`  ×  `text_ib` | 0.03 |
| `image_ib`  ×  `text_ib` | 0.03 |
| `audio_mert_random`  ×  `text_ib` | 0.03 |

## Output files in this run
### `embeddings/`
- `audio_ib_energy.npy`
- `audio_ib_random.npy`
- `audio_mert_energy.npy`
- `audio_mert_random.npy`
- `labels.csv`

### `results/`
- `method1_kmeans_purity.csv`
- `method2_diagnostic_neighbors.txt`
- `method2_neighbors_full.csv`
- `method3_silhouette_heatmap.csv`
- `method4_disagreement_topK.csv`
- `method4_jaccard_matrix.csv`
- `method5_blocksort_summary.csv`

### `figures/`
- `method1_purity_heatmap.png`
- `method3_silhouette_heatmap.png`
- `method4_jaccard_heatmap.png`
- `method5_blocksort_audio_ib_orig.png`
- `method5_blocksort_audio_mert_orig.png`
- `method5_blocksort_image_clip.png`
- `method5_blocksort_image_ib.png`
- `method5_blocksort_text_ib.png`
