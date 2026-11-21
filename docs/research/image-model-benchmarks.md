# Image model benchmarks and leaderboards (design-vault#51)


Tags: [measured-independent] = a third party measured it. [measured-self-reported] = the model maker measured it. [opinion] = no measurement.

## 1. LMArena (now arena.ai) text-to-image leaderboard

Source: https://arena.ai/leaderboard/text-to-image (lmarena.ai redirects here). Page date: 24 Sep 2026. Total 6,478,738 votes, 80 models. Method: anonymous pairwise human votes, Bradley-Terry score, 95% CI. [measured-independent]


| Rank | Model id on arena | Score | CI | Votes |
|---|---|---|---|---|
| 1 | gpt-image-2.5-sunburst (OpenAI) | 1424 | ±8 | 10,884 |
| 2 | gpt-image-2.5-flare (OpenAI) | 1401 | ±8 | 10,058 |
| 3 | gpt-image-2 (medium) | 1383 | ±4 | 88,744 |
| 6 | grok-imagine-image-2.0 (low) (xAI/"SpaceXAI") | 1301 | ±8 | 7,257 |
| 10 | seedream-5.0-pro | 1256 | ±4 | 85,690 |
| 11 | qwen-image-3.0-pro | 1256 | ±6 | 11,520 |
| 14 | gemini-3-pro-image-2k (Nano Banana Pro) | 1247 | ±3 | 168,447 |
| 16 | gemini-3-pro-image-preview (Nano Banana Pro) | 1234 | ±5 | 86,451 |
| 18 | ideogram-4.0-quality | 1205 | ±4 | 53,371 |
| 23 | grok-imagine-image | 1170 | ±3 | 262,132 |
| 24 | recraft-v4.1-utility-pro | 1169 | ±11 | 2,618 |
| 26 | grok-imagine-image-pro | 1162 | ±4 | 99,444 |
| 27 | flux-2-max | 1162 | ±3 | 123,187 |
| 28 | flux-2-flex | 1157 | ±3 | 156,912 |
| 30 | flux-2-pro | 1154 | ±3 | 205,540 |
| 35 | seedream-4.5 | 1147 | ±3 | 287,128 |
| 38 | seedream-5.0-lite | 1138 | ±3 | 123,178 |
| 40 | recraft-v4.1-pro | 1133 | ±10 | 2,795 |
| 42 | qwen-image-2512 | 1125 | ±3 | 98,363 |
| 47 | gpt-image-1 | 1116 | ±3 | 268,466 |
| 48 | recraft-v4 | 1115 | ±3 | 129,674 |
| 55 | recraft-v4.1-flash | 1100 | ±9 | 3,533 |
| 57 | z-image-turbo | 1084 | ±5 | 24,291 |
| 64 | qwen-image (Aug 2025) | 1057 | ±3 | 84,555 |
| 65 | ideogram-v3-quality | 1048 | ±4 | 118,542 |
| 70 | recraft-v3 | 1021 | ±4 | 195,623 |

Not listed on this board: Midjourney (any version), Higgsfield SOUL / SOUL V2 / SOUL Cinema, Higgsfield Marketing Studio Image 2.0 Alpha. Other high rows for context: mai-image-2.6 (Microsoft) #4, 1335; reve-2.1 #5, 1302; gemini-3.1-flash-image (Nano Banana 2) #9, 1261.

Notes:
- "gpt-image-2.5-sunburst" and "-flare" are arena names. The page does not map them to a public API name. Treat them as GPT Image 2.5 variants, not confirmed. Their vote counts (about 10k) are low; the CI is ±8.
- Grok Imagine Image 2.0 is on the board only at "(low)" setting, with 7,257 votes.
- Recraft V4.1 rows have fewer than 3,600 votes; CI ±9 to ±11.
- Ranks inside overlapping CIs are ties. Example: seedream-5.0-pro and qwen-image-3.0-pro both 1256.

## 2. LMArena (arena.ai) image-edit leaderboard

Source: https://arena.ai/leaderboard/image-edit. Page date: 21 Sep 2026. 56 models, 29,902,508 votes. [measured-independent]

| Rank | Model id | Score | CI | Votes |
|---|---|---|---|---|
| 1 | gpt-image-2.5-sunburst | 1526 | ±6 | 29,252 |
| 2 | gpt-image-2.5-flare | 1482 | ±6 | 27,048 |
| 3 | gpt-image-2 (medium) | 1461 | ±3 | 259,008 |
| 4 | grok-imagine-image-2.0 (low) | 1430 | ±6 | 16,842 |
| 8 | seedream-5.0-pro | 1394 | ±3 | 226,513 |
| 9 | gemini-3-pro-image-2k (Nano Banana Pro) | 1390 | ±3 | 582,162 |
| 10 | grok-imagine-image-quality (20260519) | 1390 | ±6 | 35,596 |
| 13 | gemini-3-pro-image-preview (Nano Banana Pro) | 1385 | ±3 | 518,488 |
| 19 | grok-imagine-image | 1329 | ±3 | 663,764 |
| 25 | seedream-4.5 | 1302 | ±2 | 1,151,587 |
| 27 | seedream-5.0-lite | 1294 | ±3 | 398,767 |
| 30 | flux-2-max | 1262 | ±3 | 352,875 |
| 33 | flux-2-pro | 1245 | ±3 | 566,119 |
| 34 | qwen-image-edit | 1241 | ±3 | 1,981,076 |
| 35 | qwen-image-edit-2511 | 1235 | ±3 | 452,569 |
| 39 | flux-2-flex | 1225 | ±3 | 415,733 |
| 51 | gpt-image-1 | 1139 | ±3 | 2,853,037 |

Not on the edit board: Qwen Image 3 (no row found), Ideogram (any), Recraft (any), Z-Image Turbo, Midjourney, Higgsfield SOUL, Marketing Studio.

## 3. Artificial Analysis (AA) text-to-image arena, "AA-Image-T2I v2.0"

Source: https://artificialanalysis.ai/image/leaderboard/text-to-image. Fetched 30 Sep 2026. The page shows no date; the newest model on it has release date 8 Sep 2026. The figures come from the data that the page embeds (166 models overall). [measured-independent]

Method (quoted from the page): "Models are ranked using an Elo rating system derived from blind comparisons judged by our recruited human panel, together with public Image Arena votes cast before 1 January 2026. Voters compare two images generated from the same prompt without knowing which model created each image." Overall = "All use cases and capabilities, each weighted equally". FLUX.2 [dev] is the fixed reference at 1000.

Categories: 9 capabilities (Text Rendering, Layout, Complex Compositions, Human Anatomy, Reasoning, Knowledge, Lighting, Material, Physics) and 10 use cases (Marketing & Advertising, Animation & Gaming, UIUX Design, Social Media & Creator Content, Productivity & Knowledge Work, Consumer, Retail & Ecommerce, Live-Action Film, Architecture & Real Estate, Frontier). There is NO style, illustration, palette, colour-binding or animal-anatomy category.

Overall figures (rank of 166 / Elo / ±CI / samples):

| Model | Rank | Elo | CI | Samples | Released |
|---|---|---|---|---|---|
| GPT Image 2.5 Sunburst (max) | 1 | 1197 | ±9 | 14,023 | Sep 2026 |
| GPT Image 2.5 Flare (max) | 2 | 1190 | ±9 | 13,393 | Sep 2026 |
| GPT Image 2 (high) | 3 | 1172 | ±9 | 15,346 | Apr 2026 |
| Grok Imagine Image 2.0 | 4 | 1155 | ±11 | 6,879 | Aug 2026 |
| Nano Banana Pro (Gemini 3 Pro Image) | 11 | 1101 | ±8 | 17,037 | Nov 2025 |
| Qwen-Image-3.0-Pro | 14 | 1089 | ±10 | 6,353 | Jul 2026 |
| Qwen-Image-3.0 | 16 | 1075 | ±10 | 6,077 | Jul 2026 |
| grok-imagine-image-quality | 17 | 1045 | ±7 | 18,986 | May 2026 |
| FLUX.2 [flex] | 22 | 1028 | ±9 | 6,182 | Nov 2025 |
| Seedream 4.5 | 25 | 1023 | ±9 | 6,615 | Dec 2025 |
| Recraft V4.1 Utility | 26 | 1023 | ±8 | 7,751 | May 2026 |
| FLUX.2 [max] | 27 | 1021 | ±8 | 12,111 | Dec 2025 |
| Recraft V4.1 Utility Pro | 31 | 1018 | ±7 | 17,519 | May 2026 |
| GPT Image 1 (high) | 35 | 1011 | ±9 | 5,375 | Apr 2025 |
| Seedream 5.0 Lite | 36 | 1011 | ±9 | 5,574 | Feb 2026 |
| Ideogram 4.0 (Quality) | 37 | 1011 | ±7 | 12,176 | Jun 2026 |
| Ideogram 4.0 | 39 | 1004 | ±8 | 10,921 | Jun 2026 |
| FLUX.2 [pro] | 40 | 1004 | ±8 | 11,756 | Nov 2025 |
| Recraft V4.1 | 50 | 990 | ±9 | 6,303 | May 2026 |
| Recraft V4.1 Pro | 58 | 985 | ±9 | 6,216 | May 2026 |
| Recraft V4 | 61 | 983 | ±9 | 5,474 | - |
| Z-Image Turbo | 80 | 941 | ±8 | 8,627 | Dec 2025 |
| Ideogram 3.0 | 100 | 897 | ±8 | 3,855 | Mar 2025 |
| Qwen Image (Aug 2025) | 105 | 889 | ±7 | 4,976 | Aug 2025 |
| Midjourney v7 Alpha | 112 | 878 | ±10 | 1,868 | - |
| Recraft V3 | 120 | 868 | ±7 | 7,348 | Oct 2024 |

Not on AA: Higgsfield SOUL (any), Higgsfield Marketing Studio Image 2.0 Alpha, any Midjourney later than "v7 Alpha". Midjourney v7 Alpha has only 1,868 samples; most Midjourney votes are probably from the public pool before 1 Jan 2026 (Midjourney has no public API) — this is an inference, not stated by AA.

Per-category ranks (rank / Elo). Category CIs are wide: about ±20 to ±34 Elo, from 600 to 1,900 samples per model. So a gap below about 40 Elo inside one category is not a clear difference.

| Model | Text Rendering | Layout | Complex Comp. | Human Anatomy | Marketing & Adv. | Animation & Gaming | UIUX Design |
|---|---|---|---|---|---|---|---|
| GPT Image 2.5 Sunburst | #4 1162 | #1 1240 | #2 1230 | #1 1220 | #2 1172 | #2 1183 | #2 1223 |
| GPT Image 2 (high) | #1 1205 (±26) | #2 1226 | #3 1216 | #2 1194 | #3 1170 | #4 1177 | #3 1207 |
| Grok Imagine Image 2.0 | #3 1167 (±31) | #5 1187 | #4 1192 | #4 1149 | #5 1142 | #3 1179 | #4 1184 |
| Nano Banana Pro | #11 1087 (±22) | #11 1143 | #13 1128 | #8 1114 | #13 1080 | #14 1093 | #9 1131 |
| Qwen-Image-3.0-Pro | #10 1092 (±27) | #6 1180 | #8 1152 | #17 1052 | #12 1087 | #13 1114 | #15 1085 |
| Qwen-Image-3.0 | #12 1079 | #8 1158 | #18 1060 | #14 1071 | #14 1078 | #15 1071 | #17 1083 |
| FLUX.2 [flex] | #23 1014 | #26 1046 | #52 1003 | #25 1027 | #28 1018 | #32 1037 | #21 1058 |
| FLUX.2 [max] | #26 1000 | #35 1034 | #39 1024 | #40 1009 | #40 1004 | #30 1037 | #24 1046 |
| FLUX.2 [pro] | #42 978 | #48 1007 | #46 1016 | #39 1010 | #31 1016 | #44 1011 | #49 997 |
| Seedream 4.5 | #32 992 | #30 1039 | #40 1023 | #23 1029 | #41 1003 | #36 1031 | #35 1013 |
| Seedream 5.0 Lite | #45 973 | #42 1023 | #23 1048 | #50 999 | #43 1001 | #28 1043 | #41 1009 |
| Ideogram 4.0 (Quality) | #41 980 (±22) | #21 1071 | #44 1020 | #34 1016 | #32 1016 | #46 1006 | #22 1052 |
| Recraft V4.1 Utility Pro | #28 998 (±21) | #22 1067 | #42 1021 | #37 1011 | #33 1013 | #35 1032 | #28 1030 |
| Recraft V4.1 | #56 957 | #51 1003 | #34 1031 | #55 989 | #42 1003 | #52 1000 | #34 1014 |
| Z-Image Turbo | #66 923 | #75 930 | #84 931 | #91 924 | #73 952 | #89 930 | #69 944 |
| Midjourney v7 Alpha | - | - | - | - | #142 773 | #104 907 | - |

Category sizes: Text Rendering 125 models, Layout 125, Complex Compositions 138, Human Anatomy 156, Marketing 165, Animation & Gaming 164, UIUX 133.

Key facts from AA categories:
- GPT Image 2 (high) is #1 on Text Rendering (1205), above GPT Image 2.5. Grok Imagine Image 2.0 is #3 (1167).
- Ideogram 4.0 (Quality) is #41 on Text Rendering (980) and Recraft V4.1 Utility Pro is #28 (998). Their best category is Layout (#21, #22).
- Qwen-Image-3.0-Pro is strong on Layout (#6, 1180).

## 4. Artificial Analysis image-editing arena

Source: https://artificialanalysis.ai/image/leaderboard/editing. Fetched 30 Sep 2026. 79 models. Same method text as section 3. Use-case categories only (no capability categories). [measured-independent]

| Model | Rank | Elo | CI | Samples |
|---|---|---|---|---|
| GPT Image 2.5 Sunburst (max) | 1 | 1182 | ±8 | 17,745 |
| GPT Image 2.5 Flare (max) | 2 | 1163 | ±8 | 18,452 |
| GPT Image 2 (high) | 5 | 1122 | ±8 | 14,058 |
| Grok Imagine Image 2.0 | 10 | 1107 | ±9 | 7,117 |
| Seedream 5.0 Pro | 11 | 1106 | ±8 | 12,654 |
| Nano Banana Pro | 13 | 1099 | ±8 | 14,448 |
| Qwen-Image-3.0-Pro | 17 | 1076 | ±8 | 12,812 |
| Seedream 5.0 Lite | 23 | 1058 | ±9 | 5,742 |
| Qwen-Image-3.0 | 24 | 1055 | ±8 | 7,560 |
| Seedream 4.5 | 30 | 1037 | ±9 | 4,811 |
| FLUX.2 [pro] | 40 | 1007 | ±7 | 7,553 |
| FLUX.2 [flex] | 41 | 1007 | ±7 | 5,753 |
| FLUX.2 [max] | 48 | 996 | ±9 | 6,061 |
| GPT Image 1 (high) | 52 | 980 | ±7 | 7,479 |

Not on the AA editing board: Ideogram, Recraft, Z-Image Turbo, Midjourney, Higgsfield. MAI-Image-2.6 (Microsoft, not in scope) is #3.

## 5. LMArena (arena.ai) text-to-image categories

Source: https://arena.ai/leaderboard/text-to-image/<category>, snapshot "latest", fetched 30 Sep 2026 (overall page dated 24 Sep 2026). Figures read from the data the page embeds. The arena has "hasStyleControl": false for images. Categories: Product, Branding & Commercial Design; 3D Imaging & Modeling; Cartoon, Anime & Fantasy; Photorealistic & Cinematic; Art; Portraits; Text Rendering. The page does not say how a prompt is put in a category. [measured-independent]

Format: rank / score ±CI (votes). 80 models in each category.

| Model | Text Rendering | Art | Cartoon, Anime & Fantasy | Commercial Design |
|---|---|---|---|---|
| gpt-image-2.5-sunburst | #1 1467 ±12 (3,699) | #1 1391 ±16 (1,544) | #1 1441 ±12 (4,090) | #1 1415 ±12 (3,669) |
| gpt-image-2 (medium) | #3 1425 ±6 (32,795) | #3 1367 ±8 (11,641) | #3 1402 ±6 (35,954) | #3 1387 ±6 (33,677) |
| grok-imagine-image-2.0 (low) | #5 1341 ±13 (2,354) | #6 1288 ±18 (1,048) | #6 1311 ±12 (2,529) | #6 1297 ±12 (2,369) |
| qwen-image-3.0-pro | #10 1283 ±10 (3,643) | #12 1255 ±14 (1,685) | #8 1277 ±10 (4,314) | #11 1256 ±10 (3,653) |
| seedream-5.0-pro | #15 1255 ±6 | #8 1266 ±7 | #10 1270 ±6 | #15 1237 ±6 |
| gemini-3-pro-image-2k (Nano Banana Pro) | #13 1271 ±5 (55,545) | #16 1224 ±6 | #14 1244 ±5 | #13 1246 ±4 |
| ideogram-4.0-quality | #18 1238 ±6 (17,299) | #18 1203 ±8 | #18 1196 ±6 | #18 1223 ±6 |
| recraft-v4.1-utility-pro | #28 1162 ±18 (956) | #22 1178 ±27 (402) | #24 1178 ±18 | #27 1167 ±16 |
| recraft-v4.1-pro | #30 1156 ±17 | #30 1161 ±25 (430) | #42 1125 ±17 | #37 1141 ±15 |
| flux-2-max | #27 1166 ±5 | #27 1169 ±6 | #27 1168 ±5 | #28 1164 ±5 |
| flux-2-flex | #26 1172 ±5 | #34 1155 ±6 | #29 1164 ±5 | #25 1173 ±5 |
| flux-2-pro | #31 1155 ±4 | #31 1161 ±5 | #31 1160 ±4 | #29 1156 ±4 |
| seedream-4.5 | #37 1143 ±4 | #33 1157 ±5 | #32 1149 ±4 | #36 1142 ±4 |
| seedream-5.0-lite | #41 1135 ±5 | #40 1139 ±6 | #36 1143 ±5 | #40 1131 ±5 |
| recraft-v4 | #40 1139 ±5 | #45 1125 ±6 | #49 1113 ±5 | #45 1128 ±5 |
| gpt-image-1 | #50 1115 ±5 | #50 1116 ±6 | #48 1115 ±5 | #49 1114 ±4 |
| z-image-turbo | #60 1061 ±7 | #60 1073 ±10 | #59 1068 ±7 | #64 1064 ±7 |
| qwen-image (Aug 2025) | #64 1048 ±5 | #64 1055 ±7 | #63 1053 ±4 | #62 1069 ±5 |
| ideogram-v3-quality | #58 1071 ±6 | #68 1039 ±7 | #65 1027 ±5 | #59 1082 ±5 |
| recraft-v3 | #74 1005 ±5 | #76 991 ±7 | #75 976 ±5 | #70 1027 ±5 |

Notes:
- Category ranks are very close to overall ranks for almost every model. A category rank adds little new data on LMArena. Exceptions: Ideogram v3 and Recraft V4 rank higher on Text Rendering and Commercial Design than on Art and Cartoon. Seedream 5.0 Pro ranks higher on Art (#8) than on Text Rendering (#15).
- Recraft V4.1 has fewer than 1,000 votes per category (Art: about 400). Its CIs are ±16 to ±27. Do not rank it finely.

## 6. Z-Image technical report (Alibaba Tongyi), arXiv:2511.22699v1, 27 Nov 2025

Source: https://arxiv.org/html/2511.22699v1. Tables 5 to 15 read in full. All figures are [measured-self-reported] for Z-Image and Z-Image-Turbo. Baseline figures for other models carry citations to their own papers, so they are copied, not re-run (the paper does not say it re-ran them). The baselines are 2025 models only (GPT Image 1, Seedream 3.0, Qwen-Image, FLUX.1, Imagen 4, Recraft V3). No current model (GPT Image 2, Nano Banana Pro, Seedream 4.5, FLUX.2 Pro) is in a table.

| Benchmark (metric) | Z-Image-Turbo | Z-Image | Qwen-Image | GPT Image 1 [High] | Seedream 3.0 | Recraft V3 | FLUX.1 [dev] |
|---|---|---|---|---|---|---|---|
| CVTG-2K word accuracy (avg, 2-5 text regions) | 0.8585 | 0.8671 | 0.8288 | 0.8569 | 0.5924 | - | 0.4965 |
| CVTG-2K NED | 0.9281 | 0.9367 | 0.9116 | 0.9478 | 0.8537 | - | 0.6879 |
| LongText-Bench EN / ZH | 0.917 / 0.926 | 0.935 / 0.936 | 0.943 / 0.946 | 0.956 / 0.619 | 0.896 / 0.878 | - | 0.607 / 0.005 |
| OneIG-EN overall | 0.528 | 0.546 | 0.539 | 0.533 | 0.530 | 0.502 | 0.434 |
| OneIG-EN text | 0.994 | 0.987 | 0.891 | 0.857 | 0.865 | 0.795 | 0.523 |
| OneIG-EN style | 0.368 | 0.387 | 0.418 | 0.462 | 0.413 | 0.378 | 0.368 |
| OneIG-EN alignment | 0.840 | 0.881 | 0.882 | 0.851 | 0.818 | 0.810 | 0.786 |
| OneIG-EN diversity | 0.139 | 0.194 | 0.197 | 0.151 | 0.277 | 0.205 | 0.238 |
| GenEval overall | 0.82 | 0.84 | 0.87 | 0.84 | 0.84 | - | 0.66 |
| GenEval colors / position / attribute binding | 0.89 / 0.65 / 0.68 | 0.93 / 0.62 / 0.77 | 0.88 / 0.76 / 0.77 | 0.92 / 0.75 / 0.61 | 0.93 / 0.47 / 0.80 | - | 0.79 / 0.22 / 0.45 |
| GenEval counting | 0.77 | 0.78 | 0.89 | 0.85 | 0.91 | - | 0.74 |
| DPG-Bench overall | 84.86 | 88.14 | 88.32 | 85.15 | 88.27 | - | 83.84 |
| PRISM-Bench EN overall (Qwen2.5-VL-72B judge) | 77.4 | 75.6 | 74.1 | 80.7 | 76.2 | - | 68.5 |

Other figures in the same report:
- Imagen 4 on OneIG-EN: overall 0.515, text 0.805, style 0.377.
- PRISM-Bench EN: Gemini 2.5 Flash Image 80.4 (#2).
- Alibaba AI Arena (Alibaba's own arena, Table 3): Z-Image-Turbo Elo 1025, #4 of 9; Imagen 4 Ultra 1048, Gemini 2.5 Flash Image 1046, Seedream 4.0 1039, Qwen-Image 1008, FLUX.1 Pro 950. The arena is run by the same company as the model. Treat as [measured-self-reported].
- Editing (Z-Image-Edit, not Turbo): GEdit-Bench-EN overall 7.57; GPT-Image-1 [High] 7.53; Qwen-Image-Edit-2509 7.54. ImgEdit overall 4.30; GPT-Image-1 4.20.

Meaning for brand art: on these 2025-era tables, Z-Image-Turbo renders short text very well (OneIG text 0.994) but has the lowest style score and low diversity of the group.

## 7. Qwen-Image-Bench (Alibaba Qwen team), arXiv:2605.28091v1, 27 May 2026

Source: https://arxiv.org/html/2605.28091v1. Read in full (method, Tables 1-4, sections 4.3-4.9). 1,000 bilingual prompts; 5 pillars, 23 sub-capabilities, 56 facets. A fine-tuned judge (Q-Judger, from Qwen3.6-27B, trained on 130,000 expert-labelled pairs from 80 art-academy annotators) scores each image. Judge-to-human Spearman rank correlation: 0.92 overall (Table 1). Table 4 also gives direct human expert scores (1-10) on 1,000 prompts per pillar.

Evidence tag: the authors make Qwen models. For Qwen models the figures are [measured-self-reported]. For the other models the figures are [measured-independent], but by a competitor. The paper predates Qwen Image 3.0 (July 2026), so Qwen Image 3 is not in it. Ideogram, Recraft, Z-Image, Grok, Midjourney and Higgsfield are not in it.

| Model | Judge overall (0-100) | Judge Aesthetics | Judge Alignment | Judge Creative Generation | Human expert overall (1-10) |
|---|---|---|---|---|---|
| GPT Image 2 | 64.69 | 67.53 | 65.85 | 75.23 | 9.10 |
| Nano Banana 2.0 | 59.82 | 61.08 | 62.40 | 67.05 | 8.71 |
| GPT Image 1.5 | 59.65 | 60.88 | 61.72 | 66.35 | 7.43 |
| Nano Banana Pro | 59.45 | 60.26 | 61.25 | 66.23 | 8.63 |
| Qwen Image 2.0 Pro | 57.84 | 58.67 | 59.28 | 64.94 | 6.99 |
| Seedream 5.0 | 57.22 | 58.40 | 58.90 | 65.29 | 6.44 |
| Seedream 4.5 | 56.78 | 58.72 | 57.31 | 60.64 | 5.50 |
| FLUX 2 Max | 55.33 | 56.85 | 57.35 | 56.50 | 4.49 |
| FLUX 2 Pro | 54.57 | 56.94 | 57.01 | 56.18 | 4.33 |
| GPT Image 1 | 54.07 | 55.09 | 56.28 | 55.78 | 5.25 |
| Qwen Image (2025) | 49.23 | 52.25 | 50.72 | 47.30 | 2.70 |

Per-facet facts relevant to brand art (from the text of sections 4.4-4.8; the per-model facet numbers are in figures only, not read):
- GPT Image 2's highest facets: Text Layout, Storyboard Creation, Graphic Design, Game Design, Information Visualization (all above 84; Graphic Design and Game Design above 90).
- Text Accuracy is the single facet that separates models most. Only GPT Image 2, Seedream 5.0, Qwen Image 2.0 Pro and Nano Banana 2.0 score above 60 on it.
- Graphic Design: gap from rank 1 to the median model is more than 30 points.
- Art Design: ranks 2-4 are within about one point. The authors say "artistic style transfer is relatively mature".
- Animals: the best model scores 42.6 of 100. Anatomical Fidelity: best 20.9. These are among five facets where all 18 models fail.
- Colour Harmony has an industry mean above 60 ("mature").
- Seedream 4.5 scores higher than Seedream 5.0 on Quality and Aesthetics; 5.0 is more than 4 points higher on Creative Generation.

## 8. FEPBench: natural-science illustration (Shanghai AI Lab, Shanghai Innovation Institute, USTC), arXiv:2606.05949v1, 4 Jun 2026

Source: https://arxiv.org/html/2606.05949v1. Table 2 and method read. 1,300 illustrations from natural-science papers; PhD experts wrote the prompts; an MLLM scores each output against human-audited "atom sets" (visual, textual, relation, layout elements). The paper reports agreement with human judgement (figure not read). Authors do not make any model in the table. [measured-independent]

Scores 0-1. IF = instruction faithfulness; t = text elements; l = layout elements; SP = semantic precision (no unsupported additions).

| Model | IF overall | IF text | IF layout | RE overall | SP overall |
|---|---|---|---|---|---|
| GPT Image 2 | 0.664 | 0.389 | 0.886 | 0.334 | 0.703 |
| Nano Banana Pro | 0.629 | 0.333 | 0.870 | 0.281 | 0.733 |
| GPT Image 1.5 | 0.598 | 0.361 | 0.710 | 0.294 | 0.693 |
| Seedream 5.0 | 0.575 | 0.362 | 0.685 | 0.255 | 0.716 |
| Qwen-Image-2.0 Pro | 0.515 | 0.234 | 0.641 | 0.234 | 0.747 |
| FLUX.2 [dev] | 0.531 | 0.289 | 0.686 | 0.244 | 0.655 |
| Z-Image-Turbo | 0.390 | 0.179 | 0.562 | 0.165 | 0.606 |

Meaning: for dense diagrams with many labels, all models get less than 40% of the required text right. GPT Image 2 leads on faithfulness; Nano Banana Pro and Qwen-Image-2.0 Pro add fewer unrequested elements (higher SP). Z-Image-Turbo is last on faithfulness.

## 9. "Benchmarking Frontier Text-to-Image Models on Image-Description Prompts", arXiv:2608.14976, 15 Aug 2026

Source: https://arxiv.org/abs/2608.14976 (abstract and method headings read). 48 hard prompts from the DataSeeds.AI dataset (counts, attribute binding, embedded text, spatial rules). GPT-5.4-Pro writes a rubric per image; a second model grades it. No human scores. Small sample, LLM judge, only 4 models; weak evidence. [measured-independent]

| Model | Score /100 |
|---|---|
| Gemini 3 Pro Image (Nano Banana Pro) | 84.8 |
| FLUX.2 (variant not given in abstract) | 82.3 |
| Ideogram 3.0 | 65.7 |
| Hunyuan 3.0 | 63.3 |

The authors say the top two fail mostly on object counts and geometric artefacts; Ideogram 3.0 fails by garbled text and by leaving out requested elements.

## 10. Arena-T2I Hard (Arena Intelligence Inc + UCLA), arXiv:2606.31711v1, 30 Jun 2026

Source: https://arxiv.org/html/2606.31711 (abstract, Tables 1, 5, 6 read). 310 hard prompts taken from real arena votes; each prompt is split into a graph of yes/no questions (about 10 per prompt); a VLM judge (gemini-3-flash) answers them; a failed parent question fails its children. Figure = share of questions answered "yes" (faithfulness). The ranking holds when a second decomposer (GPT-5.4) is used: Spearman 0.982. The judge is a Google model; the paper checks decomposer bias, not judge bias. Authors make no model in the table. [measured-independent]

| Model | Arena-T2I Hard | DPG-Bench (same judge) | DSG | Arena rank at the time |
|---|---|---|---|---|
| gemini-3-pro-image-preview-2k (Nano Banana Pro) | 0.855 | 0.970 | 0.946 | #3 |
| grok-imagine-image-20260306 | 0.849 | 0.965 | 0.934 | #8 |
| gpt-image-1.5-high-fidelity | 0.796 | 0.970 | 0.942 | #4 |
| recraft-v4 | 0.787 | 0.956 | 0.914 | #29 |
| gemini-2.5-flash-image | 0.768 | 0.954 | 0.921 | #14 |
| gpt-image-1 | 0.722 | 0.959 | 0.938 | #27 |
| imagen-4.0-ultra | 0.680 | 0.961 | 0.928 | #17 |
| ideogram-v3-quality | 0.523 | 0.894 | - | #42 |

Per-category faithfulness (Table 5; prompts per category: Art 56, Cartoon 53, Commercial 30, Text 21):

| Model | Art | Cartoon | Commercial design | Text-heavy prompts |
|---|---|---|---|---|
| Nano Banana Pro | 0.896 | 0.816 | 0.842 | 0.906 |
| grok-imagine-image (Mar 2026) | 0.889 | 0.803 | 0.855 | 0.881 |
| gpt-image-1.5-high-fidelity | 0.811 | 0.767 | 0.753 | 0.744 |
| recraft-v4 | 0.766 | 0.737 | 0.812 | 0.817 |
| gpt-image-1 | 0.778 | 0.686 | 0.658 | 0.726 |
| ideogram-v3-quality | 0.515 | 0.508 | 0.450 | 0.570 |

Key claims by the authors:
- DPG-Bench and DSG are saturated: most current models score above 0.95, so they no longer separate top models.
- Public arena rank does not predict faithfulness: "holistic Bradley-Terry preference scores prioritize aesthetics over fine-grained prompt adherence". Recraft V4 is #29 on the arena but #4 on faithfulness. Ideogram v3 is last.
- GPT Image 2, GPT Image 2.5, Qwen Image 3, Ideogram 4.0, Recraft V4.1, Seedream, FLUX.2 and Midjourney are NOT in this test.

## 11. Ideogram 4.0 technical blog (Ideogram), 3 Jun 2026

Source: https://ideogram.ai/blog/ideogram-4.0/ (read via summary tool, not in full). All figures [measured-self-reported]. Ideogram 4.0 is open-weight (9.3B parameters).
- Internal designer arena: 4,366 votes by graphic designers, blind, nine pipelines. GPT Image 2 Elo 1141 (#1), Ideogram 4.0 Elo 1062 (#2, first among open-weight models). The full list of the nine pipelines was not read.
- X-Omni English OCR accuracy: 0.97.
- 7Bench layout mIoU: 0.69. SpatialGenEval: 0.76 (judge: gemini-2.5-flash). PRISM-Bench alignment: 0.89.
The public arenas use general voters; Ideogram's arena uses graphic designers. This is a real difference in voter pool, not only a conflict of interest.

## 12. Gemini 3 Pro Image (Nano Banana Pro) model card (Google DeepMind), Nov 2025

Source: https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-Pro-Image-Model-Card.pdf (read in full, 6 pages). Human side-by-side ratings on Google's own prompt sets; Elo ± CI. Rater pool and vote counts are not given. [measured-self-reported]

| Capability | Gemini 3 Pro Image (Search on) | Gemini 2.5 Flash Image | GPT-Image 1 | Seedream v4 4k | FLUX Pro Kontext Max |
|---|---|---|---|---|---|
| Text Rendering | 1198 ±18 | 997 ±10 | 1150 ±14 | 1019 ±13 | 854 ±13 |
| Stylization | 1098 ±11 | 933 ±7 | 1069 ±9 | 991 ±9 | 908 ±11 |
| General Text-to-Image | 1094 ±16 | 1037 ±8 | 1025 ±9 | 1011 ±9 | 907 ±9 |
| Visual design | 1104 ±16 | 1083 ±7 | 1028 ±11 | 1038 ±12 | 907 ±11 |
| Infographics | 1268 ±17 | 1162 ±11 | 1087 ±12 | 1049 ±12 | 824 ±15 |
| General Image Editing | 1127 ±13 | 996 ±8 | 1011 ±13 | 965 ±12 | 902 ±13 |
| Text editing | 1202 ±23 | 1001 ±10 | 996 ±14 | 860 ±15 | 943 ±12 |

Limits that Google states in the card: "Text rendering: poor in small text (often blurry in 1k model), long paragraphs, page length"; "Occasional confusion around spatial localisation (e.g. left/right etc.)"; character consistency between input and output "not always perfect".
The comparison models are all 2025 models. GPT Image 2, FLUX.2 and Seedream 4.5 are not in the card.

## 13. Makers that publish no benchmark figures (checked)

- FLUX.2 (Black Forest Labs), https://bfl.ai/blog/flux-2: the launch post claims leading performance but gives no figures, no voter count, no method (read via summary tool). [opinion]
- Seedream 4.5 (https://seed.bytedance.com/en/seedream4_5) and Seedream 5.0 Lite (https://seed.bytedance.com/en/seedream5_0_lite): each page shows radar charts from ByteDance's internal "MagicBench" but gives no numbers in text and no competitor names. [measured-self-reported, figures not readable]
- Qwen-Image-2.0 technical report, arXiv:2605.10730 (May 2026): reports only LMArena (rank #9, Elo 1168, accessed 22 Apr 2026). It reports no GenEval, DPG, OneIG, LongText or CVTG figures.
- Qwen Image 3.0 (released 21 Jul 2026): no technical report found on arXiv, Hugging Face or GitHub. The qwen.ai blog page is rendered by script and I could not read its body. Status of maker figures: unknown.
- Recraft V4.1: the only figure found is a press release (30 May 2026) that says Recraft V4.1 Utility Pro was #5 on the AA arena at that date. On the current AA board (v2.0, section 3) it is #31. [opinion/marketing]
- GPT Image 2 / 2.5 (OpenAI): the launch page returned HTTP 403; no OpenAI eval table was found. Unknown.

## 14. UniGenBench++ leaderboard (UnifiedReward team; paper arXiv:2508.20751 and arXiv:2510.18701), English short prompts

Source: https://huggingface.co/spaces/CodeGoat24/UniGenBench_Leaderboard, file leaderboard_data.json, last modified 22 Feb 2026 (63 models). 600 prompts, 10 dimensions and 27 sub-dimensions; an MLLM judge (Gemini 2.5 Pro; an offline Qwen judge agrees 94%) checks each test point. The benchmark team runs every model (README: "send an Email ... we will help with the evaluation"). The team makes no in-scope model. [measured-independent, MLLM judge]

| Rank of 63 | Model (release) | Overall | Style | Color | Animal | Text | Layout | Quantity |
|---|---|---|---|---|---|---|---|---|
| 1 | "GPT-4o-1.5" (Dec 2025; probably GPT Image 1.5, name not confirmed) | 95.77 | 99.19 | 100.0 | 95.59 | 97.39 | 94.56 | 90.71 |
| 2 | Nano Banana Pro | 92.72 | 99.30 | 99.17 | 90.44 | 95.65 | 93.28 | 90.28 |
| 3 | GPT-4o (image, Mar 2025) | 92.48 | 98.98 | 99.17 | 87.88 | 89.24 | 91.35 | 89.29 |
| 5 | FLUX.2 [max] | 90.85 | 99.09 | 99.17 | 86.03 | 89.38 | 95.26 | 90.28 |
| 6 | Seedream 4.5 (251128) | 89.70 | 99.20 | 100.0 | 91.91 | 91.67 | 92.54 | 87.50 |
| 7 | FLUX.2 [flex] | 89.35 | 98.59 | 100.0 | 87.50 | 88.24 | 92.23 | 88.19 |
| 8 | FLUX.2 [pro] | 88.35 | 99.29 | 99.17 | 80.88 | 82.35 | 94.13 | 84.72 |
| 16 | Qwen-Image (Aug 2025) | 78.36 | 94.70 | 99.17 | 86.76 | 72.13 | 86.57 | 84.03 |
| 18 | Z-Image | 78.10 | 96.80 | 97.50 | 82.35 | 68.39 | 84.89 | 81.25 |
| 25 | Z-Image-Turbo | 71.40 | 90.00 | 95.83 | 78.68 | 70.69 | 78.36 | 75.00 |
| 43 | "Recraft" (Dec 2024; probably Recraft V3) | 62.63 | 87.20 | 95.83 | 76.47 | 61.78 | 57.84 | 68.06 |

Not on this board: GPT Image 2 / 2.5, Qwen Image 2 or 3, Seedream 5, Ideogram (any), Recraft V4/V4.1, Grok, Midjourney, Higgsfield.
Saturation: Style and Color are at 97-100 for every frontier model, so these columns no longer separate them. Text, Animal and Quantity still separate them.

## 15. T2I-CoReBench (Kuaishou Kling research + co-authors; ICLR 2026; arXiv:2509.03516)

Source: https://t2i-corebench.github.io/ leaderboard, read 30 Sep 2026; last model update 2026-03 (Nano Banana 2). Judge: Gemini 2.5 Flash (default evaluator; human-alignment balanced accuracy 81.1% per README). 12 dimensions: composition (MI multi-instance, MA multi-attribute, MR multi-relation, TR text rendering) and 8 reasoning dimensions. The benchmark team runs each model. The team makes Kling models, none in scope. [measured-independent, MLLM judge]

| Model | MI | MA (attribute binding) | MR | TR (text) | Composition mean | Reasoning mean | Overall |
|---|---|---|---|---|---|---|---|
| Nano Banana Pro | 91.9 | 85.5 | 83.4 | 98.1 | 89.7 | 82.7 | 85.0 |
| GPT-Image-1.5 | 87.0 | 83.4 | 76.9 | 94.7 | 85.5 | 74.6 | 78.2 |
| Seedream 4.5 | 92.0 | 87.1 | 77.7 | 96.2 | 88.3 | 71.3 | 77.0 |
| Seedream 4.0 | 91.5 | 84.5 | 75.0 | 93.6 | 86.1 | 69.9 | 75.3 |
| GPT-Image (gpt-image-1) | 84.1 | 75.9 | 72.7 | 86.4 | 79.8 | 69.0 | 72.6 |
| FLUX.2-dev | 89.5 | 83.4 | 72.7 | 93.3 | 84.7 | 54.2 | 64.4 |
| Qwen-Image-2512 | 88.5 | 82.5 | 71.9 | 91.9 | 83.7 | 51.7 | 62.4 |
| Z-Image | 86.6 | 80.3 | 70.8 | 90.1 | 81.9 | 50.6 | 61.1 |
| Qwen-Image (Aug 2025) | 81.4 | 79.6 | 65.6 | 85.5 | 78.0 | 49.3 | 58.9 |
| Z-Image-Turbo | 79.5 | 72.2 | 62.7 | 83.9 | 74.6 | 47.3 | 56.4 |

Not on this board: GPT Image 2 / 2.5, FLUX.2 Pro / Flex / Max (only dev and klein), Qwen Image 2 / 3, Seedream 5, Ideogram, Recraft, Grok, Midjourney, Higgsfield.
Note: Seedream 4.5 leads on multi-attribute binding (87.1), the closest academic proxy for "use exactly these colours on these objects". Composition scores for frontier models are 84-90; reasoning scores separate them more.

## 16. GEditBench v2 / OpenEdit leaderboard (Nanyang Technological University), arXiv:2603.28547v1, 30 Mar 2026

Source: https://arxiv.org/html/2603.28547 (Table 3 read). About 1,200 edit tasks per model; pairwise Elo. Instruction following and visual quality judged by GPT-4o; visual consistency (does the edit keep what it should keep) judged by the authors' PVC-Judge. The "Arena" column is the public arena Elo at that time. Authors make no model in the table. [measured-independent, model judges]

| Model (date run) | Instruction following | Visual quality | Visual consistency | Overall Elo ±CI |
|---|---|---|---|---|
| Nano Banana Pro (4 Mar 2026) | 1126 | 1066 | 1108 | 1096 ±6 |
| Seedream 4.5 (11 Mar 2026) | 1111 | 1142 | 1030 | 1089 ±7 |
| GPT Image 1.5 (4 Mar 2026) | 1260 | 1149 | 846 | 1071 ±7 |
| Qwen-Image-Edit-2511 | 1095 | 1060 | 972 | 1038 ±6 |
| FLUX.2 [dev] | 1037 | 965 | 1018 | 1006 ±7 |

Meaning for matched sets: GPT Image 1.5 follows the edit instruction best but has the lowest visual consistency of the top group (846): it changes parts of the image it should keep. Nano Banana Pro keeps the rest of the image best. GPT Image 2 / 2.5, FLUX.2 Pro / Max, Grok and Qwen Image 3 are not in this table.

## 17. CPI-Bench: real-world image editing (Alibaba Group), arXiv:2608.14546v2, 18 Aug 2026

Source: https://arxiv.org/html/2608.14546 (Tables 3 and 5 read). A VLM judge scores each edit 1-5 on instruction adherence, visual quality and consistency, with per-category prompts. The authors report that their ranking has the highest Spearman correlation with the Arena image-edit leaderboard of the benchmarks they compared. Evidence tag: Alibaba makes Qwen, so Qwen rows are [measured-self-reported]; other rows are [measured-independent] but run by a competitor.

| Model | General single-image edit, overall (1-5) | Stylize | Text edit | Practical bench overall | Ad Create | Style & creative gen. |
|---|---|---|---|---|---|---|
| GPT-Image-2 | 4.74 | 4.78 | 4.53 | 4.69 | 4.74 | 4.85 |
| Seedream 5 Pro | 4.71 | 4.84 | 4.87 | 4.73 | 4.98 | 4.92 |
| Nano Banana Pro | 4.61 | 4.86 | 4.81 | 4.58 | 4.90 | 4.81 |
| Qwen Image 2.0 Pro | 4.55 | 4.89 | 4.71 | 4.39 | 4.08 | 4.73 |
| Qwen-Image-Edit-2511 | 4.30 | 4.79 | 4.39 | 3.85 | 2.73 | 3.90 |
| FLUX.2-klein-9B | 4.18 | 4.83 | 3.69 | 3.86 | 2.38 | 4.38 |

Top scores are close to the 5.0 ceiling (4.6-4.7). Differences of under 0.1 between the top three are small. Seedream 5 Lite, FLUX.2 Pro / Max, Grok, Ideogram, Recraft are not in the table.

## 18. IGenBench: text-to-infographic reliability (Zhejiang Univ., UESTC, UVA, HKUST-GZ, Cornell), arXiv:2601.04498v2, 8 Jun 2026

Source: https://arxiv.org/html/2601.04498 (Table 1 read). Infographic prompts; Gemini-2.5-Pro answers fact questions about each output. Q-ACC = share of questions correct; I-ACC = share of images with every question correct. Authors make no model in the table. [measured-independent, MLLM judge]

| Model | Title Q-ACC | Legend | Overall Q-ACC | I-ACC (whole image correct) |
|---|---|---|---|---|
| Nano Banana Pro | 0.98 | 0.96 | 0.90 | 0.49 |
| Seedream 4.5 | 0.95 | 0.81 | 0.61 | 0.06 |
| GPT-Image-1.5 | 0.60 | 0.57 | 0.55 | 0.12 |
| Qwen-Image (2025) | 0.56 | 0.51 | 0.36 | 0.01 |
| Z-Image-Turbo | 0.61 | 0.58 | 0.35 | 0.00 |

The paper says Seedream 4.5 ranks 4th on LMArena but 2nd here. GPT Image 2, FLUX.2, Ideogram, Recraft and Grok are not in the table.

## 19. HEIM (Stanford CRFM), arXiv:2311.04287

Source: https://crfm-helm.readthedocs.io/en/latest/heim/ and the paper. HEIM v1.1.0 evaluates 26 models from 2023 over 12 aspects. None of the models in scope is in it. The docs say the full HEIM run "is not currently reproducible with standard instructions". [not applicable]

## 20. Colour obedience (palette, hex codes)

No arena or benchmark found that measures hex-code or palette obedience for the current closed models (GPT Image 2/2.5, Nano Banana Pro, Seedream 4.5/5, Ideogram 4.0, Recraft V4.1, Grok, Midjourney). Nearest evidence:

a) ACBench / CompColor in "Paint-Anything" (ByteDance Seed + Zhejiang Univ. + Nanjing Univ.), arXiv:2609.20816, Sep 2026. Source: https://arxiv.org/html/2609.20816 (Table 1 and section 4.3 read). SAM3 masks the named object; the mean sRGB colour is compared with the requested hex value; MAE ≤16 = full score, ≥64 = zero. Open models only; the authors re-ran them. The authors' own model is not in scope. [measured-independent]

| Model | ACBench-T2I overall (0-100, hex colour of the object) | ACBench-Edit (recolour to hex) | CompColor single (named colours, 0-1) |
|---|---|---|---|
| FLUX.2-dev (56B total) | 51.70 | 68.87 | 0.73 |
| FLUX.2-klein-9B | 38.15 | 64.53 | 0.75 |
| Z-Image-Turbo | 33.56 | - | 0.65 |
| Qwen-Image / Qwen-Image-Edit | 25.21 | 54.40 | 0.59 |

Key fact (section 4.3): for FLUX.2-4B, writing the colours as raw hex strings instead of colour names drops the CompColor score from 0.72 to 0.38. Base models do not map hex codes to colours well. A prompt should name colours in words as well as hex. This is measured on one open FLUX.2 model only; do not assume it holds for the closed models.

b) UniGenBench++ "Color" and OneIG/GenEval "colors" columns (sections 6, 14): frontier models score 97-100 on named-colour binding. These test "a red cube", not a brand palette.

d) GenColorBench (Computer Vision Center, UAB; CVPR 2026; arXiv:2510.20586): tests only older open models (SD family, FLUX.1). No in-scope model.

## 21. Per-model summary

Evidence strength scale: STRONG = two or more independent sources with human or checked-judge method; MEDIUM = independent arenas only, or one independent benchmark; WEAK = maker figures only; NONE = no figure.

- **GPT Image 2.5** (Sunburst / Flare, Sep 2026). #1 and #2 on both arenas (LMArena T2I 1424, edit 1526; AA T2I 1197, edit 1182). #1 in every LMArena category and in most AA categories. Only about 10,000-14,000 votes; released weeks ago. No benchmark paper includes it yet. Evidence: MEDIUM (arenas only).
- **GPT Image 2** (Apr 2026). #3 on both arenas. #1 on AA Text Rendering (1205). #1 on Qwen-Image-Bench (judge 64.69; human experts 9.10/10). #1 on FEPBench faithfulness. #1 on CPI-Bench general editing (4.74). #1 in Ideogram's own designer arena. Evidence: STRONG.
- **gpt-image-1** (lineage, Apr 2025). LMArena #47, AA #35. Mid-table on 2025 benchmarks (GenEval 0.84, OneIG-EN 0.533, CVTG-2K 0.8569, all copied). Superseded.
- **Grok Imagine Image 2.0** (Aug 2026). LMArena T2I #6 (low setting only, 7,257 votes), edit #4; AA T2I #4, edit #10. AA Text Rendering #3, Animation & Gaming #3. No benchmark paper includes 2.0. Its predecessor grok-imagine-image (Mar 2026) is #2 on Arena-T2I Hard faithfulness (0.849). Evidence: MEDIUM.
- **Nano Banana Pro** (Gemini 3 Pro Image, Nov 2025). Arena rank is lower than its benchmark rank: LMArena T2I #14, edit #9; AA T2I #11, edit #13. It leads or is near the top on most faithfulness benchmarks: Arena-T2I Hard #1 (0.855), T2I-CoReBench top of those tested (85.0; text 98.1), UniGenBench #2 (92.72), IGenBench #1 by a wide gap (0.90 vs 0.61), GEditBench v2 #1 (best at keeping the unedited parts), FEPBench #2, Qwen-Image-Bench human experts 8.63 (#3). Caution: four of those benchmarks use a Google Gemini judge. Two non-Gemini sources (Qwen-Image-Bench human scores; GEditBench v2 with GPT-4o judge) also rank it high. Evidence: STRONG.
- **Qwen Image 3.0 / 3.0 Pro** (Jul 2026). LMArena #11 (Pro, 1256, 11,520 votes); AA #14 (Pro) and #16 (standard). AA Layout #6 (Pro), Text Rendering #10. No maker report and no benchmark paper found. Lineage: Qwen-Image-2.0 Pro is #5 on Qwen-Image-Bench (self-reported) and weak on text in FEPBench (0.234). Evidence: MEDIUM (arenas only).
- **Ideogram 4.0** (Jun 2026). LMArena #18 (1205, 53,371 votes); AA #37 (Quality) and #39. AA Text Rendering #41 (980); Layout #21. Maker figures: #2 in its own designer arena, 0.97 X-Omni OCR. No independent benchmark includes 4.0. Ideogram 3.0 is last of 11 on Arena-T2I Hard (0.523). Evidence: MEDIUM for arena rank; WEAK for its text-rendering lead claim.
- **Recraft V4.1** (May 2026). LMArena: Utility Pro #24 (only 2,618 votes, ±11), Pro #40, Flash #55. AA: Utility #26, Utility Pro #31, V4.1 #50, Pro #58. Recraft V4 is #4 of 11 on Arena-T2I Hard (0.787; commercial design 0.812), far above its arena rank. Recraft V3: OneIG-EN 0.502, UniGenBench 62.63. No independent benchmark includes V4.1. Evidence: MEDIUM.
- **Z-Image Turbo** (Nov 2025). LMArena #57, AA #80. Maker report: top short-text scores (CVTG-2K 0.8585, OneIG text 0.994). Independent tests place it low: UniGenBench #25 (71.4), T2I-CoReBench 56.4, FEPBench last, IGenBench 0.35, ACBench hex 33.56. Evidence: STRONG that it is below the frontier; its text lead is WEAK (self-reported only).
- **Higgsfield SOUL / SOUL V2 / SOUL Cinema**. Not on LMArena or AA. No benchmark or maker figure found. Evidence: NONE.
- **Higgsfield Marketing Studio Image 2.0 Alpha** (released 1 Sep 2026 per Higgsfield API docs). Not on any board; underlying model not named. Evidence: NONE.
- **FLUX.2 Pro / Flex / Max** (Nov-Dec 2025). LMArena T2I #27-30 (1154-1162); AA #22 (Flex), #27 (Max), #40 (Pro). UniGenBench #5 (Max), #7 (Flex), #8 (Pro). Qwen-Image-Bench: Max 55.33, Pro 54.57 (human 4.49, 4.33 of 10: low). 48-prompt study: FLUX.2 82.3, #2 of 4. Edit arenas: #30-#48. No maker figures. Evidence: STRONG that it is upper-mid, not frontier.
- **Seedream 4.5** (Dec 2025). LMArena #35 (1147); AA #25. Benchmarks rank it higher than arenas: T2I-CoReBench best multi-attribute binding (87.1); UniGenBench #6; IGenBench #2; GEditBench v2 #2; Qwen-Image-Bench 56.78 (human 5.50). Evidence: STRONG.
- **Seedream 5.0 Lite** (Feb 2026). LMArena #38 (1138); AA #36; edit LMArena #27, AA #23. Few benchmarks name it. The "Seedream 5.0" in Qwen-Image-Bench and FEPBench is probably Lite (Pro came in Jul 2026), but the papers do not say. Seedream 5.0 Pro (not on the founder's list) is LMArena #10 and AA #15. Evidence: MEDIUM.
- **Midjourney**. Not on LMArena. On AA only as v7 Alpha (#112 of 166, 878 Elo, 1,868 samples) and v6/v6.1. V8 alpha (17 Mar 2026), V8.1 and V8.2 (24 Jul 2026) are on no board and in no benchmark found. Evidence: NONE for the current version.

## 22. What the benchmarks say for brand art

**Text in the image.** GPT Image 2 leads on independent human measures (AA Text Rendering #1; LMArena Text Rendering #3 behind two GPT Image 2.5 variants). Nano Banana Pro leads the faithfulness benchmarks on text (T2I-CoReBench 98.1; UniGenBench 95.65; Arena-T2I Hard 0.906; IGenBench titles 0.98). Grok Imagine 2.0 is #3 on AA Text Rendering. Ideogram 4.0's claim to lead typography is supported only by its own tests; on AA it is #41 of 125 for text. For small text, long paragraphs and dense diagrams every model still fails often (FEPBench: best text faithfulness 0.389; IGenBench: best whole-image correct 0.49; Google's own card lists small and long text as a limit).

**Palette and colour binding.** Simple colour tests are saturated (UniGenBench Color 97-100; GenEval colors 0.88-0.93). On multi-attribute binding, Seedream 4.5 (87.1), Nano Banana Pro (85.5), GPT-Image-1.5 (83.4) and FLUX.2-dev (83.4) are close. No test covers hex-code palette obedience for any closed model. For one open FLUX.2 model, hex strings in the prompt halve the colour score compared with colour names (0.72 to 0.38).

**Style range and illustration.** No arena has a dedicated flat-illustration or painterly category. LMArena "Art" and "Cartoon, Anime & Fantasy" rank models almost exactly as "Overall": GPT Image 2.5 and 2 lead; Grok 2.0 #6; Qwen Image 3.0 Pro #8 on Cartoon; Seedream 5.0 Pro #8 on Art. On AA "Animation & Gaming", GPT Image 2.5 Flare is #1 and Grok 2.0 is #3. Qwen-Image-Bench finds "Art Design" mature: ranks 2-4 differ by about one point. Style columns in UniGenBench and OneIG do not separate frontier models.

**Headline space and layout.** No benchmark tests "leave empty space for a headline". The nearest is AA "Layout": GPT Image 2.5 Sunburst #1, GPT Image 2 #2, Grok 2.0 #5, Qwen Image 3.0 Pro #6, Nano Banana Pro #11, Ideogram 4.0 #21, Recraft V4.1 Utility Pro #22. Google's card lists left/right confusion as a limit of Nano Banana Pro. Unknown for the specific task.

**Animal anatomy (manta mascot).** Qwen-Image-Bench: the best of 18 models scores 42.6/100 on "Animals" and 20.9 on anatomical fidelity; the authors call these industry-wide ceilings. UniGenBench's easier "Animal" column: GPT-Image-1.5 95.6, Seedream 4.5 91.9, Nano Banana Pro 90.4, FLUX.2 Pro 80.9, Z-Image-Turbo 78.7. No data on rays or other uncommon animals. Plan to check anatomy by eye on every render.

**Editing and matched sets.** Both edit arenas put GPT Image 2.5, GPT Image 2 and Grok 2.0 at the top, then Seedream 5.0 Pro and Nano Banana Pro. GEditBench v2 adds a key split: GPT Image 1.5 follows edit instructions best but changes most of what it should keep (consistency 846); Nano Banana Pro keeps the rest of the image best (1108). For a set that must stay consistent, this favours Nano Banana Pro among the models that test covers; GPT Image 2 and 2.5 were not in it.

**Where arena and benchmark disagree.**
- LMArena and AA agree on the top four (GPT Image 2.5 x2, GPT Image 2, Grok 2.0) and disagree lower down (Ideogram 4.0 #18 vs #37).

**Saturated or gameable measures.**
- DPG-Bench and DSG: frontier models score above 0.95; they no longer separate the leaders (Arena-T2I Hard). GenEval overall is 0.82-0.87 for all 2025 frontier models. UniGenBench Style and Color: 97-100.
- Makers now report arenas, not academic benchmarks (Qwen-Image-2.0 report: LMArena only). Figures for GPT Image 2.5, Qwen Image 3, Ideogram 4.0 and Recraft V4.1 on academic benchmarks do not exist yet.
- Arenas: new entries have few votes and wide CIs (Recraft V4.1 ±10; Grok 2.0 ±8). "The Leaderboard Illusion" (arXiv:2504.20879) shows private pre-release testing and unequal data access on LMArena's text arena; it does not study the image arenas, so the effect there is unknown.
- MLLM judges: Arena-T2I Hard, UniGenBench, T2I-CoReBench and IGenBench use Google Gemini judges; Nano Banana Pro (Google) leads all four. None measured judge self-preference. The size of its lead is uncertain.

## 23. Bound

Read in full or table-by-table: arena.ai text-to-image, image-edit and 4 category boards (raw page data, snapshot 21-24 Sep 2026); Artificial Analysis text-to-image board with all 19 categories and editing board (raw page data, fetched 30 Sep 2026); Z-Image report (Tables 5-15); Qwen-Image-Bench (Tables 1-4 and sections 4.3-4.9); Arena-T2I Hard (Tables 1, 5, 6); FEPBench (Table 2); GEditBench v2 (Table 3); CPI-Bench (Tables 3, 5); IGenBench (Table 1); UniGenBench++ leaderboard JSON (63 models); T2I-CoReBench leaderboard (Gemini 2.5 Flash evaluator block); ACBench/Paint-Anything (Table 1, section 4.3); Gemini 3 Pro Image model card (full PDF); Qwen-Image-2.0 report (evaluation section).
Sampled only (via summary tool or abstract): Ideogram 4.0 blog; FLUX.2 blog; Seedream 4.5 and 5.0 Lite pages; xAI Imagine Image 2.0 post; Midjourney V8 alpha page; Recraft press release; "Benchmarking Frontier T2I Models on Image-Description Prompts" (abstract and method headings); Leaderboard Illusion (abstract); GenColorBench (tables list); HEIM docs; OneIG-Bench site (last update 19 Sep 2025; leaderboard embed not readable). Per-facet numbers in Qwen-Image-Bench figures were not read.
Could not reach: OpenAI's Images 2.0 page (HTTP 403); the qwen.ai blog body for Qwen Image 3.0 (script-rendered); Artificial Analysis and arena.ai method pages beyond the text on the leaderboards; the AA X post on the v2.0 taxonomy (HTTP 402). Not found anywhere: any figure for Higgsfield SOUL, SOUL V2, SOUL Cinema or Marketing Studio Image 2.0 Alpha; any figure for Midjourney V8.x; any technical report for GPT Image 2/2.5, Qwen Image 3.0, Ideogram 4.0 (beyond its blog), Recraft V4.1, Grok Imagine 2.0 or FLUX.2 Pro/Max; any hex-palette test of a closed model; any test of "empty space for a headline".
