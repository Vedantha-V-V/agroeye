

## B.M.S. COLLEGE OF ENGINEERING
(Autonomous College under VTU) | Bull Temple Road, Bengaluru – 560019
Department of Computer Science and Engineering (Data Science)
Project Work – Phase II | 23DS7PWPP2 | Review 2
AgroEye: A SAM-Based Synthetic Data Pipeline
for UAV-Style Crop Disease Detection
Presented by
Hemanth R1BM23CD021
Shakthi Jashwanth1BM23CD072
Vedantha Vinay Verneker   1BM23CD069
Under the guidance of
## Prof. Lavanya Naik
## Prof. Manoj Kumar S
Dept. of CSE (Data Science), BMSCE

Table of Contents
- Introduction and Objectives
- Methodology and System
## Architecture
- Implementation and Code Quality
- Results, Validation and
## Benchmarking
- Novelty and Optimization
- Project Planning and Risk
## Management
- Report, Documentation and SDG
## Mapping
## 8. Research Paper Status
- Conclusion and Future Work
## 10. References
Department of Computer Science & Engineering (Data Science)2

Introduction and Problem Statement
- Context: early and late blight cut tomato and
potato yields; UAVs image fields at cm resolution
on demand.
- Problem: no large UAV-view dataset boxes every
diseased leaf; one frame holds dozens of small
targets, so labelling is slow.
- Gap: PlantVillage [1] shows single close-up
leaves and its models degrade in the field [2].
Cut-and-paste [3] and domain randomisation [4]
work elsewhere; agricultural synthetic data uses
generated targets [6, 7].
- Scope: SAM extraction, 7-factor compositor,
automatic labels, two detectors, real-UAV
transfer test. Excluded: drone hardware, flight
planning, cloud deployment, multispectral.
Two imaging regimes
PlantVillageUAV nadir
GeometryOne centred
leaf
## Top-down,
many plants
Background   UniformSoil, weeds,
crop rows
LightingControlled,
diffuse
Direct sun,
shadow
ScaleLeaf fills the
frame
29–74 px in
640 px
OcclusionNoneOverlapping
canopy
Naive pasting gives a “sticker effect”: hard edges,
no contact shadow, wrong scale, wrong colours.
Department of Computer Science & Engineering (Data Science)3

## Objectives
#    Objective (Phase 1 plan)StatusEvidence
O1   Extract background-free leaf cutouts
from PlantVillage without manual masks
Completed18,163 SAM cutouts, 13 classes (6,652
used)
O2   Compose UAV-style scenes with domain
randomisation and automatic YOLO
labels
Completed1,200 composites, 57,771 boxes, 0
manual labels
O3   Train and benchmark a CNN and a
Transformer detector on the generated
data
CompletedYOLOv11m 0.907 vs RT-DETR-L 0.761
mAP@50
O4   Fine-tune on real drone imagery (“reality
loop”)
PartialPublic UAV data used instead of own
flights; AUC 0.59 → 0.68 (3 seeds; gain
on 2 of 4 plots)
O5   Demonstrate the trained detectorCompletedIn-browser ONNX demo (PWA)
O4 changed scope: with no annotated in-house flights, we used the public A. solani UAV dataset [8]
(patch labels, not boxes).
Department of Computer Science & Engineering (Data Science)4

## Proposed Methodology
In plain words
Cut real diseased leaves out of lab photos with SAM,
paste them onto real aerial ground tiles at drone
scale with randomised nuisance factors, and compute
every box from the pasted leaf’s own mask.
Why this approach
- Manual box labelling of UAV frames: too slow
and costly.
- GAN / diffusion targets [6, 7]: synthetic
textures; we keep real photographed lesions.
- Leaf-Only SAM [9] scores green leaves only;
ours also credits yellow–brown diseased tissue.
SAM mask score
s(M) = 0.20A + 0.28C + 0.30G
+ 0.12ˆq + 0.10σ− 0.25B
A: area preference (peak at 30% of image)   C:
centrality
G: HSV plant colour (green and yellow–brown)
ˆq,σ: SAM predicted IoU, stability   B: border
contact
Rotation-aware YOLO label
x
c
## =
x
min
## +w/2
## W
, y
c
## =
y
min
## +h/2
## H
, w
## ′
## =
w
## W
, h
## ′
## =
h
## H
extent of rotated alpha > 20; W = H = 640;
clamped to [0, 1].
Department of Computer Science & Engineering (Data Science)5

## System Architecture
DataPreprocessingModelInterface
PlantVillage (13 classes) +
65 aerial images
SAM ViT-B [10] cutouts;
176 tiles of 640 px sorted by
HSV green ratio
7-factor compositor →
YOLOv11m [11] /
## RT-DETR-L [12]
ONNX export, in-browser
demo (onnxruntime-web)
Department of Computer Science & Engineering (Data Science)6

Implementation and System Integration
Modules, in pipeline order
segment_leaf.pySAM cutouts (RGBA PNG)
backgrounds.pytiling + soil/farm/grass
generate_synthetic.pycompositor + labels
prepare_yolo_dataset.py80/10/10 split, seed 42
train_{yolo11m,rtdetr}.pytraining
test_models.pytest-split evaluation
run_cv_experiments.pyreal-UAV plot-level CV
implementation-app/ONNX demo (PWA)
Integrated: each stage reads the previous stage’s
folder; all parameters live in the scripts.
Still manual: dataset downloads, launching each
stage, ONNX export of the chosen checkpoint.
Live demonstration
python implementation-app/tools/serve.py 8080
YOLOv11m (ONNX) runs in the browser on test and
uploaded images.
Defects found and resolved
- 1 SAM file-write failure → reprocessed (18,163
cutouts).
- Random patch split leaked near-duplicates (0.88
mAP@50) → leave-one-plot-out CV.
- CUDA illegal-memory crash with two jobs on one
GPU → run serially; CV resumes from cache.
- Paper vs. disk audit: label files lack a trailing
newline, so wc -l undercounted by 1 box per
image (56,571 vs 57,771) → recounted by
parsing; paper, thesis and slides corrected.
Department of Computer Science & Engineering (Data Science)7

Tools, Technology Stack and Code Quality
Tool (version)Why
Python 3.13, PyTorch
## 2.11 + CUDA 12.8
GPU training on RTX
## A5000 (24 GB)
Ultralytics 8.4.154One API for YOLO11 and
## RT-DETR
## Segment Anything
(ViT-B)
Zero-shot masks, no
labels
Pillow, NumPy, OpenCVCPU compositing, HSV
tiling
onnxruntime-web 1.20.1Offline in-browser
inference
Git + Git LFSVersioned weights and
runs
- Repository: one script per stage,
requirements.txt, data.yaml, demo
README; commit history on main.
- Reproducibility: fixed seeds (split 42,
training 0); demo numbers are recomputed
from runs/, never typed; an audit
re-checked every compositor and SAM
parameter in the paper against the code.
- Testing: held-out test split, checkpoint
re-evaluation, throughput test (67.7 FPS,
14.8 ms per tile). No automated unit-test
suite yet.
Department of Computer Science & Engineering (Data Science)8

Experimental Setup and Evaluation Metrics
## Datasets
- Synthetic: 1,200 composites, 6 classes balanced
by instance (9.5–9.8k each); 960 / 120 / 120
split, seed 42.
- Real UAV [8]: 3,157 patches (256 px,
0.3 mm/px), 5 plots, 1,027 infected / 2,130
healthy; leave-one-plot-out.
Training (Ultralytics, RTX A5000, seed 0)
YOLOv11m   RT-DETR-L
Batch / LR16 / 10
## −3
## 8 / 10
## −4
Optimiser, epochs   AdamW, 40   AdamW, 40
Input, init640, COCO   640, COCO
Metrics and why
- mAP@50, mAP@50–95: detection quality;
50–95 rewards tight boxes.
- P, R, F1 at the F1-optimal threshold.
- FPS at batch 1, FP32: survey-time feasibility.
- AUC, AP (real data): only patch labels exist;
labelling all patches “infected” already gives
## F1 ≈ 0.65.
Baselines (all retrained, none quoted)
- RT-DETR-L on the same data and budget.
- Real-only YOLOv11m (COCO init) and
zero-shot synthetic model.
Department of Computer Science & Engineering (Data Science)9

Results on the Held-Out Synthetic Test Split
ClassmAP@50   50–95
## Potato Early Blight0.9500.801
## Potato Late Blight0.9120.758
## Potato Healthy0.9550.824
## Tomato Early Blight0.8950.688
## Tomato Late Blight0.8010.584
## Tomato Healthy0.9270.742
Mean (YOLOv11m)0.9070.733
## • Worst: Tomato Late Blight (recall
0.679); 16% missed as background.
- Val – test gap 0.009–0.016: no
overfitting to validation.
- Single seed; test shares assets with
training.
Normalised confusion matrices: (a) YOLOv11m, (b) RT-DETR-L
Department of Computer Science & Engineering (Data Science)10

Validation on Real UAV Imagery (A. solani, potato)
Leave-one-plot-out, mean ± std over runs (4 test plots;
×3 seeds at 100%), patch-level AUC (chance = 0.5).
Real dataReal-only   Syn→real    Gain
## 0% (zero-shot)–0.48±0.01–
## 10%0.47±0.05   0.52±0.04   +0.05
## 25%0.56±0.04   0.56±0.01    0.00
100% (3 seeds)   0.59±0.04   0.68±0.13   +0.09
- Zero-shot fails: chance-level AUC. Real
patches are 8× finer (lesions, not leaves)
and NIR-shifted.
- Pretraining helps with full data, but
unevenly: mean per-plot gains
+0.02,−0.03, +0.25, +0.11; wins 8 of
12 paired runs.
- No gain at 10–25%, where it would
matter most.
- Random patch split gave 0.88 mAP@50,
which did not survive the leakage-free
split.
Statistical status: 100% rows = 4 folds × 3 seeds (gain per seed +0.13, +0.02, +0.11); other rows 4 folds × 1
seed. The single-seed gain (+0.13) shrank to +0.09.
Department of Computer Science & Engineering (Data Science)11

## Comparative Benchmarking
Same 120-image synthetic test split and metrics for both rows; RTX A5000, batch 1, FP32.
ModelParamsPRF1    mAP@50   mAP@50–95   FPS
YOLOv11m (CNN)20.1 M   0.918   0.836   0.8750.9070.73367.7
RT-DETR-L (Transformer)   32.8 M   0.801   0.704   0.7490.7610.54231.2
Where we win
- YOLOv11m: +0.146 mAP@50, +0.191 mAP@50–95 and
2.2× faster – no speed/accuracy trade-off.
- Syn→real beats real-only at 100% real data on average
(AUC 0.68 vs 0.59, 3 seeds), driven by 2 of 4 plots.
Where we do not
- RT-DETR-L was undertrained: below 0.31 mAP@50 for
26 of 40 epochs, still rising at 40 – not a verdict on
## Transformers.
- Zero-shot and 10–25% real data: no benefit from
synthetic data.
Department of Computer Science & Engineering (Data Science)12

Novelty and Research Contribution
In one sentence
An annotation-free pipeline that turns real photographed PlantVillage disease leaves into
UAV-scale, rotation-aware labelled scenes, tested honestly on real UAV imagery under a
leakage-free split.
AreaWhat already existsNew in AgroEye
Leaf segmentationLeaf-Only SAM for phenotyping [9]Mask score crediting diseased hues, used to
harvest labelled detection foregrounds
Synthetic agri dataGenerated targets: GPBD [6], GAN fields [7]Real photographed lesions only
CompositionCut-paste [3], domain randomisation [4, 5]7 factors at UAV scale, canopy-density clusters,
labels from rotated alpha
EvaluationRandom splits, synthetic test onlyPlot-level CV on real UAV data
Own work: mask score, compositor, labelling, CV protocol, demo.   Adapted: SAM, YOLO11, RT-DETR, real
dataset [8].
Department of Computer Science & Engineering (Data Science)13

Optimization and Ablation Study
Optimisations applied
- Native-resolution tiling instead of downscaling
(keeps soil texture).
- IoU guard 0.50: partial canopy overlap without
duplicate boxes.
- RT-DETR-L: batch 8, LR 10
## −4
for attention
stability.
- Mosaic off for the last 10 epochs; AMP training.
Cost of each choice
ParamsLatency
YOLOv11m20.1 M14.8 ms
RT-DETR-L32.8 M32 ms
SAM extraction–41 h (0.12 img/s)
Ablation status
The per-factor ablation has not been run; only the
full compositor has a result (0.907 mAP@50).
Planned runs, one change each, same test data:
- Naive copy-paste (no factors).
- Without feathering; without shadow.
- Without GSD scaling; without sensor blur.
Tried, did not work
- Zero-shot transfer (AUC 0.48); any-blight
scoring (0.50).
- Random patch split (leaky 0.88 mAP@50).
- RT-DETR-L at a 40-epoch budget.
Department of Computer Science & Engineering (Data Science)14

Project Planning: WBS and Critical Path
WP Work packageOwnerPlanned (2026) Weeks
1 Literature, problem definition Hemanth R06–24 Jul3
2 Asset collectionVedantha V V27 Jul–07 Aug2
3 SAM leaf extractionShakthi Jashwanth CH 10–28 Aug3
4 Compositor and labellingHemanth R31 Aug–11 Sep2
5 Dataset packagingShakthi Jashwanth CH 14–18 Sep1
6 Detector trainingVedantha V V21–25 Sep1
7 Evaluation and analysisHemanth R28 Sep–09 Oct2
8 Real-UAV transfer studyShakthi Jashwanth CH 12–30 Oct3
9 Demo application
## ∗
## Vedantha V V28 Sep–09 Oct2
10 Paper and reportHemanth R02–13 Nov2
Critical path total06 Jul–13 Nov    19
One primary owner per WP. Weeks are Mon–Fri; W1 starts 06 Jul 2026.
## ∗
WP9 shown at its earliest start; off the critical path.
## WP1WP2WP3WP4WP5
## WP6
## WP7
## WP8
## WP10
## WP9
Red: critical path (WP3 alone took 41 h of GPU time)
Slack of WP9 (demo, parallel to WP7–8)
Slack = LS− ES = LF − EF
## ES
## 9
## = EF
## 6
= end of W12 (25 Sep)
## LF
## 9
## = LS
## 10
= end of W17 (30 Oct)
d
## 9
= 2 weeks
## Slack
## 9
= 17− (12 + 2) = 3 weeks
Department of Computer Science & Engineering (Data Science)15

Schedule Tracking and Risk Management
Milestones: plan vs actual
MilestonePlanActual
Synthetic dataset18 Sep 2026    17 Sep 2026
Detectors trained25 Sep 2026    18 Sep 2026
Repo + LFS tracking   09 Oct 2026   26 Oct 2026
Real-UAV fine-tuning   30 Oct 2026   27 Oct 2026
Paper revised13 Nov 2026   29 Oct 2026
Multi-seed CV30 Oct 2026   30 Oct 2026
Slip: repo + LFS tracking was set up 17 days late,
during the pre-paper audit. Dataset and training
finished ahead of plan; the paper revision was
pulled forward for the review.
Risk register
RiskL    I    MitigationTrigger
Sim-to-real gapH    H   Real-UAV CV,
fine-tuning
## AUC ≈ 0.5
GPU job crashM   M   One job per GPU,
resumable cache
CUDA error
Data leakageM   H   Plot-level splitsToo-good
scores
Paper  over  page
limit
H   M   Cut text and figures>6 pages
Numbers drift from
code
M   H   Audit; compute,
never type
Count   mis-
match
Materialised: the GPU crash (30 Oct) stopped the multi-seed CV after 4
of 16 runs; it was diagnosed as GPU contention, rerun alone from the
cache and completed the same day. Zero-shot transfer also hit chance
level, which redirected effort to fine-tuning.
Department of Computer Science & Engineering (Data Science)16

Project Report and Documentation Status
## Chapters
- Complete draft in the BMSCE template: 79
pages, 6 chapters, 3 appendices.
## • Ch. 1 Introduction, 2 Literature Review, 3
## Methodology, 4 Implementation, 5 Results
and Discussion, 6 Conclusion.
- 22 figures, 21 tables, 41 references; all
metrics re-checked against runs/ and
results/.
## Formatting
- IEEE citation style, numbered figures and
tables.
- Certificate, declaration, abbreviations, lists
of figures and tables included.
## Appendices
- A: source-code excerpts (mask score,
compositor, folds, evaluation).
- B: dataset configuration, training script,
reproduction commands.
- C: all 48 runs of the real-UAV study.
Datasets documented
- PlantVillage (13 classes, 18,163 images), 176
aerial tiles, 1,200 composites.
- Wieme et al. UAV data (Zenodo
## 10.5281/zenodo.10727413).
Department of Computer Science & Engineering (Data Science)17

SDG Mapping and Societal Impact
TargetLink to AgroEye
SDG 2.4Early disease detection supports
resilient, sustainable food production
SDG 2.3Low-cost scouting for small-scale
producers
SDG 12.3Reduce crop losses at the production
stage
SDG 9.5Open, reproducible agri-AI research
capacity
Stakeholders and needs
- Smallholder farmers: cheap, early warning.
- Agronomists / extension officers: field-wide
coverage.
- Drone service providers: models without heavy
labelling.
Shown by our results
- 57,771 labelled boxes with zero manual
annotation.
- 14.8 ms per 640 px tile: survey flights
processable on one GPU.
- Synthetic pretraining lifted full-data real
AUC 0.59 → 0.68 (3 seeds), mainly on 2
of 4 plots.
Only potential so far
- Yield-loss and fungicide reductions: not
measured.
- Real-field use: one disease, one season,
patch labels.
- Annotation savings in the low-data regime:
not shown.
Department of Computer Science & Engineering (Data Science)18

## Research Paper Status
## Paper
AgroEye: A SAM-Based Synthetic Data Pipeline for
UAV-Style Crop Disease Detection, with a Transfer
Study on Real UAV Imagery
Target venue: CSITSS (IEEE, hosted by RVCE) –
applied computer vision and IT systems; IEEEtran
conference format.
Status: Drafted and internally reviewed
Revised 29–30 Oct 2026 after a structured review. Open
items before submission:
- Length: current build is 10 pages; to be checked against
the venue limit.
- Done 30 Oct: annotation counts corrected; Table VIII
updated with 3-seed results.
## Manuscript
IEEEtran, 10 pages, 9 figures, 9 tables, 22
references.
Verified results in the paper
Synthetic test re-evaluated from the
checkpoints; real-UAV study with 3 seeds
at full data.
## Funding
BMSCE Faculty Research Promotion
Scheme, R&D/FRPS-3/2025-26/CS/1-20
Department of Computer Science & Engineering (Data Science)19

Conclusion and Future Work
## Achieved
- O1–O3: annotation-free pipeline from
PlantVillage to labelled UAV-style scenes;
detectors trained and compared.
- O4 (partial): first real-UAV transfer test,
leakage-free.
- O5: working in-browser demo.
Key result
YOLOv11m: 0.907 mAP@50 at 67.7 FPS on synthetic
test; on real UAV data synthetic pretraining lifts mean
AUC 0.59 → 0.68 with full real data (3 seeds,
plot-dependent).
## Limitations
No zero-shot or low-data gain; no ablation; shared
assets; one seed for synthetic training.
Future work (from those limitations)
- Camera-matched synthesis: render lesions at
the target GSD with hue and channel jitter.
- Factor ablation against naive copy-paste.
- Asset-disjoint splits for honest in-domain
scores.
- Real box labels on a few hundred UAV frames;
PlantDoc [13] test.
- Fair RT-DETR comparison: train to
convergence, 3+ seeds.
- Single-crop scenes with clustered infection.
Department of Computer Science & Engineering (Data Science)20

## References
[1] D. P. Hughes and M. Salathé, “An open access
repository of images on plant health to enable the
development of mobile disease diagnostics,”
arXiv:1511.08060, 2015.
[2] S. P. Mohanty, D. P. Hughes, and M. Salathé, “Using
deep learning for image-based plant disease detection,”
Front. Plant Sci., vol. 7, 1419, 2016.
[3] D. Dwibedi, I. Misra, and M. Hebert, “Cut, paste and
learn: Surprisingly easy synthesis for instance
detection,” in Proc. ICCV, 2017, pp. 1301–1310.
[4] J. Tobin et al., “Domain randomization for transferring
deep neural networks from simulation to the real world,”
in Proc. IROS, 2017, pp. 23–30.
[5] J. Tremblay et al., “Training deep networks with
synthetic data: Bridging the reality gap by domain
randomization,” in Proc. CVPRW, 2018, pp. 969–977.
[6] N. Giakoumoglou, E. M. Pechlivani, and D. Tzovaras,
“Generate-Paste-Blend-Detect: Synthetic dataset for
object detection in the agriculture domain,” Smart
Agric. Technol., vol. 5, 100258, 2023.
[7] A. Prasad, N. Mehta, M. Horak, and W. D. Bae, “A
two-step machine learning approach for crop disease
detection: An application of GAN and UAV
technology,” arXiv:2109.11066, 2021.
[8] J. Wieme et al., “Ultra-high-resolution UAV-imaging
and supervised deep learning for accurate detection of
Alternaria solani in potato fields,” Front. Plant Sci., vol.
## 15, 2024.
[9] D. Williams, F. Macfarlane, and A. Britten, “Leaf Only
SAM: A Segment Anything pipeline for zero-shot
automated leaf segmentation,” arXiv:2305.09418, 2023.
[10] A. Kirillov et al., “Segment Anything,” in Proc. ICCV,
2023, pp. 4015–4026.
[11] G. Jocher and J. Qiu, “Ultralytics YOLO11,” v11.0.0,
- [Online]. Available:
https://github.com/ultralytics/ultralytics
[12] Y. Zhao et al., “DETRs beat YOLOs on real-time object
detection,” in Proc. CVPR, 2024, pp. 16965–16974.
[13] D. Singh et al., “PlantDoc: A dataset for visual plant
disease detection,” in Proc. CoDS-COMAD, 2020, pp.
## 249–253.
Department of Computer Science & Engineering (Data Science)21

## THANK YOU
## Questions?