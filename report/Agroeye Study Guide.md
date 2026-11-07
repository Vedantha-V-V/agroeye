PROJECT WORK PHASE II · REVIEW 2 · 23DS7PWPP2 

# AgroEye review prep 

Built from the thesis and the 22-slide review deck. Every number here matches the corrected documents (30 Oct 2026): 57,771 boxes, re-measured FPS, three-seed real-UAV results. 

THE 30-SECOND ANSWER TO "WHAT DID YOU DO?" 

Drone disease detectors need aerial images with a box around every diseased leaf, and almost none exist. We built AgroEye: SAM cuts real diseased leaves out of PlantVillage lab photos, a seven-factor compositor pastes them onto real aerial field tiles at drone scale, and every box is computed from the leaf's own mask, so 1,200 images and 57,771 boxes needed no manual labelling. 

YOLOv11m reaches 0.907 mAP@50 on the synthetic test split and beats RT-DETR-L (0.761). On real UAV images of potato early blight, the synthetic-only model is at chance (AUC 0.48). Used as pretraining it lifts AUC from 0.59 to 0.68 with all real data, mainly on two of four plots, and gives no help with little real data. The main open problem is matching the camera's scale and colour. 

## Numbers to know cold 

Examiners test whether you know your own figures. These are the ones that appear on the slides and in the thesis. 

|Data generation||Split (seed 42, 80/10/10)||
|---|---|---|---|
|PlantVillage images (13<br>classes)|18,163|Train images / boxes<br>Val images / boxes|960 / 46,561<br>120 / 5,285|
|Cutouts used (6 classes)|6,652|Test images / boxes|120 / 5,925|
|SAM: automatic / centre<br>|12,881 / 5,281|Boxes per class|9,488–9,770|
|prompt||Distinct cutouts per class|152–1,909|
|SAM speed, total time|0.12 img/s,~41 h|Training||
|Aerial sources→tiles<br>|65→176<br>|Epochs, optimiser, input|40, AdamW, 640|
|Soil / farm / grass tiles<br>Composites, boxes<br>|47 / 25 / 104<br>1,200, 57,771|YOLOv11m batch / LR<br>RT-DETR-L batch / LR|16 / 1e-3<br>8 / 1e-4|
|Mean leaves per image<br>|48.1|Training time|9.3 / 37.2 min|
|Leaf size on 640 px tile|29–74 px|Parameters|20.1 M / 32.8 M|



|Real UAV data (Wie|me et al.)|||||||||
|---|---|---|---|---|---|---|---|---|---|
|Resolution||0.|3 mm/px|||||||
|Patches (256 px)|||3,157|||||||
|Infected / healthy||1,027|/ 2,130|||||||
|Drone images, plots|||281, 5|||||||
|Scale gap vs ours|||~8×|||||||
|Leaky random split (dis|carded)|0.88|mAP@50|||||||
|SYNTHETIC TEST|P|R|F1|MAP@50||MAP@50|–95|FPS|MS/TILE|
|SPLIT||||||||||
|YOLOv11m|0.918|0.836|0.875|0.907||0.733||67.7|14.8|
|RT-DETR-L|0.801|0.704|0.749|0.761||0.542||31.2|32.0|
|Validation (YOLO /<br>DETR)|val–test|gap 0.0|09–0.016|0.916 /|0.777|0.747 /|0.557|2.2×|faster|
|PER CLASS (YOLOV11M)|||M|AP@50|MAP@5|0–95|RT-DET|R-L MAP|@50|
|Potato Early Blight|||0|.950|0.801||0.850|||
|Potato Late Blight|||0|.912|0.758||0.753|||
|Potato Healthy|||0|.955|0.824||0.867|||
|Tomato Early Blight|||0|.895|0.688||0.731|||
|Tomato Late Blight (hard|est; recall 0.|679)|0|.801|0.584||0.564|||
|Tomato Healthy|||0|.927|0.742||0.798|||



|REAL|REAL-ONLY|SYNTHETIC**→**REAL|GAIN|RUNS|
|---|---|---|---|---|
|UAV,<br>PATCH<br>AUC<br>(CHANCE<br>0.5)|||||
|0%|–|0.48±0.01|–|4|
|(zero-|||||
|shot)|||||
|10% of<br>real|0.47±0.05|0.52±0.04|+0.05|4 + 4|
|images|||||
|25% of<br>real<br>images|0.56±0.04|0.56±0.01|0.00|4 + 4|
|100% (3<br>seeds)|0.59±0.04|0.68±0.13|+0.09±0.13|12 + 12|
|100%,<br>per test<br>plot 1 / 2|gain +0.02 / −|0.03 / +0.25 / +0.11|8 of 12 wins|per seed +0.13 / +0.02 / +0.11|
|/ 3 / 4|||||



## Slide by slide 

What to say on each slide of the review deck, the rubric item it scores, and the question it is most likely to draw. 

01 Title 

_Say: Introduce the team and guides; state the title in one line._ 

Title: AgroEye, a SAM-based synthetic data pipeline for UAV-style crop disease detection. 

Review 2 of Project Work Phase II, course 23DS7PWPP2. 

02 Table of contents 

_Say: Ten sections; spend most time on results and validation._ 

Do not read the list. One sentence: we go from problem to pipeline to results, then planning and paper status. 

Recap 

### 03 Introduction and problem statement 

_Say: Drone detectors need a box on every diseased leaf, and such data barely exists._ 

- Context: early and late blight cut potato and tomato yields; UAVs image fields at centimetre resolution. 

- Problem: one 640 px tile holds dozens of small leaves, so box labelling is slow and needs an expert. 

- Gap: PlantVillage is close-up lab photos and its models degrade in the field; agricultural synthetic data so far uses generated (GAN/diffusion) targets. 

- Scope: extraction, compositor, labels, two detectors, real-UAV test. Excluded: drone hardware, flight planning, cloud, multispectral. 

Sticker effect: hard edges, no contact shadow, wrong scale, wrong colour. 

Expect: Why not just label real drone images? 

### 04 Objectives Implementation 

_Say: Four of five objectives complete; O4 is partial and we say why._ 

- O1 cutouts: 18,163 (6,652 used). O2 composites: 1,200 with 57,771 boxes, no manual labels. 

- O3 detectors: YOLOv11m 0.907 vs RT-DETR-L 0.761 mAP@50. 

- O4 partial: no annotated in-house flights, so we used the public A. solani UAV dataset; AUC 0.59 → 0.68 over 3 seeds, gain on 2 of 4 plots. 

- O5: in-browser ONNX demo. 

Expect: Why is O4 only partial? 

### 05 Proposed methodology 

Implementation 

_Say: Cut real diseased leaves out with SAM, paste them onto real aerial ground at drone scale, compute every box from the leaf's own mask._ 

Mask score s(M) = 0.20A + 0.28C + 0.30G + 0.12q̂ + 0.10σ − 0.25B. 

- G credits yellow–brown diseased tissue as well as green, unlike Leaf-Only SAM. 

- Label: extent of rotated alpha > 20, normalised to YOLO format, clamped to [0, 1]. 

Expect: Why does the colour term include brown and yellow? 

### 06 System architecture 

Implementation 

_Say: Data, preprocessing, model, interface, in that order._ 

Data: PlantVillage (13 classes) and 65 aerial images. 

- Preprocessing: SAM ViT-B cutouts; 176 native-resolution tiles sorted by HSV green ratio. 

- Model: seven-factor compositor feeding YOLOv11m and RT-DETR-L. 

- Interface: ONNX export, in-browser demo. 

Expect: Why tile at native resolution instead of resizing? 

Integration 

### 07 Implementation and system integration 

_Say: One script per stage, connected by files on disk; each stage can be re-run alone._ 

- Chain: segment_leaf → backgrounds → generate_synthetic → prepare_yolo_dataset → train → test_models → prepare_real_cv → run_cv_experiments → web app. 

- Live demo: python implementation-app/tools/serve.py 8080. 

- Defects found: 1 SAM write failure (reprocessed); leaky random split (0.88 mAP@50) replaced by plot-level CV; CUDA crash with two GPU jobs; label count off by one per image, corrected to 57,771. 

Expect: What broke during integration and how did you fix it? 

08 Tools, technology stack and code quality 

Tool usage 

_Say: Open-source stack, fixed seeds, numbers computed from the stored runs._ 

- Python 3.13, PyTorch 2.11 (CUDA 12.8), Ultralytics 8.4.154, SAM ViT-B, OpenCV, Pillow, onnxruntime-web 1.20.1, Git + LFS. 

- RTX A5000 24 GB, Xeon W-2295, 128 GB RAM. 

- Testing: held-out split, checkpoint re-evaluation, throughput test (67.7 FPS, 14.8 ms per tile). No automated unit-test suite yet: say so. 

Expect: How do you know your reported numbers are correct? 

### 09 Experimental setup and evaluation metrics 

Results 

_Say: Two datasets, identical training settings, metrics chosen for each task._ 

- Synthetic: 1,200 images, 960/120/120, seed 42, classes balanced (9.5–9.8k boxes each). 

- Real: 3,157 patches, 5 plots, leave-one-plot-out. 

- mAP@50 and mAP@50–95 for boxes; AUC and AP for real patches because only patch labels exist; labelling every patch infected already gives F1 ≈ 0.65. 

- Baselines are retrained, not quoted from papers. 

Expect: Why AUC instead of mAP on the real data? 

### 10 Results on the held-out synthetic test split 

Results 

_Say: YOLOv11m 0.907 mAP@50; Tomato Late Blight is the weak class._ 

- Per class mAP@50 from 0.801 (Tomato LB) to 0.955 (Potato Healthy). 

- Tomato LB: recall 0.679, 16% missed as background; dark lesions look like moist soil and shadow. 

- Val–test gap 0.009–0.016: no overfitting to the validation split. 

- Caveat: single seed, test shares tiles and cutouts with training. 

Expect: Why does Potato Healthy score highest with only 152 cutouts? 

11 Validation on real UAV imagery 

Validation 

_Say: Zero-shot fails; pretraining helps on average with full data; no help with little data._ 

Zero-shot AUC 0.48: real patches are 8× finer (lesions, not whole leaves) and the camera is NIR-shifted. 

- 100% real data, 3 seeds: 0.59 → 0.68, 8 of 12 paired wins, per plot +0.02 / −0.03 / +0.25 / +0.11. 

- 10–25% real data: no gain, which is where it would matter most. 

- Random patch split gave 0.88 mAP@50 and did not survive the leakage-free split. 

Expect: Is the +0.09 gain statistically significant? 

### 12 Comparative benchmarking Benchmarking 

_Say: Same split, same metrics, same hardware for both detectors._ 

- YOLOv11m: +0.146 mAP@50, +0.191 mAP@50–95, 2.2× faster (67.7 vs 31.2 FPS). No speed/accuracy tradeoff. 

- Synthetic → real beats real-only at 100% real data on average (0.68 vs 0.59). 

- Where we do not win: RT-DETR-L was undertrained (below 0.31 for 26 of 40 epochs); zero-shot and lowdata show no benefit. 

Expect: Is it fair to say CNNs beat Transformers here? 

13 Novelty and research contribution 

Novelty 

_Say: The parts exist; the contribution is their combination for UAV-scale disease detection plus an honest realdata test._ 

Mask score crediting diseased hues, used to harvest detection foregrounds. 

- Real photographed lesions, not GAN or diffusion targets. 

- Seven factors at UAV scale, canopy clusters, labels from the rotated alpha. 

- Plot-level cross-validation on real UAV data. 

- Own work: mask score, compositor, labelling, CV protocol, demo. Adapted: SAM, YOLO11, RT-DETR, real dataset. 

Expect: What exactly is new, given cut-paste and SAM already exist? 

### 14 Optimization and ablation study 

Optimization 

_Say: Optimisations were applied; the per-factor ablation has not been run, and we say so._ 

- Native-resolution tiling, IoU guard 0.50, RT-DETR batch 8 / LR 1e-4, mosaic off for the last 10 epochs, AMP. Cost: YOLOv11m 20.1 M params, 14.8 ms; RT-DETR-L 32.8 M, 32 ms; SAM extraction 41 h. 

- Ablation rows are planned: naive copy-paste, minus feathering, minus shadow, minus GSD scaling, minus blur. 

- Tried and failed: zero-shot (0.48), any-blight scoring (0.50), random split (leaky 0.88), RT-DETR at 40 epochs. 

Expect: Without an ablation, how do you know the seven factors help? 

15 Project planning: WBS and critical path 

Planning 

_Say: Ten work packages, one owner each; WP3 (SAM, 41 h) dominates the critical path._ 

- WP1 literature → WP2 assets → WP3 SAM → WP4 compositor → WP5 packaging → WP6 training → WP7 evaluation → WP8 real-UAV → WP10 paper/report. 

- WP9 (demo) runs in parallel with WP7–8 and has slack. 

- Slack = LS − ES = LF − EF. Fill in the owner, effort and slack values before the review. 

Expect: What is the critical path and how much slack does the demo have? 

16 Schedule tracking and risk management Planning 

_Say: Milestones with actual dates, and the risks that actually happened._ 

- Actual: synthetic dataset 17 Sep; detectors trained 17–18 Sep; LFS tracking 26 Oct; real-UAV fine-tuning 27 Oct; paper revised 29 Oct; multi-seed CV 30 Oct. 

- Risks: sim-to-real gap (H/H), GPU crash (M/M), data leakage (M/H), page limit (H/M), numbers drifting from code (M/H). 

- Materialised: GPU crash stopped the CV after 4 of 16 runs; rerun alone from the cache and finished the same day. Zero-shot at chance redirected effort to fine-tuning. 

Expect: Which risk materialised and what did you do? 

### 17 Project report and documentation status 

Report 

_Say: The thesis is written in the BMSCE template; state chapters, appendices and the similarity score._ 

- The thesis is complete in draft: 6 chapters, 3 appendices, 79 pages. Update the slide's 'completed / remaining' placeholders. 

- Appendices: dataset sources, PO/SDG mapping, similarity report. 

- Similarity: Drillbit, references excluded, must be ≤ 20%. 

Expect: What is your similarity score? 

18 SDG mapping and societal impact 

SDG 

_Say: Separate what the results show from what is only potential._ 

Shown: 57,771 boxes with no manual labels; 14.8 ms per tile; full-data AUC 0.59 → 0.68. 

- Only potential: yield-loss and fungicide reduction not measured; one disease, one season; no low-data saving. 

Stakeholders: smallholder farmers, agronomists and extension officers, drone service providers. 

Expect: Which SDG targets, and what evidence links the project to them? 

19 Research paper status 

Paper 

_Say: Drafted and internally reviewed for IEEE CSITSS; numbers corrected 30 Oct._ 

Venue: CSITSS (IEEE, hosted by RVCE), IEEEtran format. 

- Open item: length. The current build is 10 pages; check the venue limit. 

- Funding: BMSCE Faculty Research Promotion Scheme, R&D/FRPS-3/2025-26/CS/1-20. 

- Attach submission acknowledgement and similarity score if available. 

Expect: Has the paper been submitted? 

### 20 Conclusion and future work Conclusion 

_Say: Reproducible labelled UAV-style data, strong in-domain results, limited real-world benefit so far._ 

- Headline numbers: 0.907 mAP@50 synthetic; 0.59 → 0.68 real-UAV AUC with synthetic pretraining (3 seeds). 

- Limitations: no zero-shot or low-data gain, no ablation, shared assets across splits, one seed for synthetic training. 

- Future: camera-matched synthesis, factor ablation, asset-disjoint splits, real box labels and PlantDoc, fair RT-DETR training, single-crop scenes, mask quality control. 

Expect: If you had three more months, what would you do first? 

21 References 

_Say: Be able to name the four key references._ 

- PlantVillage (Hughes & Salathé); SAM (Kirillov et al.); RT-DETR (Zhao et al., CVPR 2024); real UAV data (Wieme et al., Frontiers in Plant Science 2024). 

## Question bank 

Likely examiner questions with model answers. Cover the answer and say it aloud before reading it. 

What problem does AgroEye solve, in one sentence? Problem Drone disease detectors need aerial images with a box on every diseased leaf, which barely exist; AgroEye generates them automatically from labelled close-up PlantVillage photos and real aerial background tiles. 

Why not just annotate real drone images? Problem 

One 640 px tile at low altitude holds 50 or more small leaves, each needing a tight box and a disease label from someone who can recognise the disease. Data is cropand region-specific. We had no annotated in-house flights, and the public UAV data we found has patch labels only. 

What is the sticker effect? Problem The artefacts of naive pasting: hard alpha edges, no contact shadow, implausible leaf size and studio colours. A detector can learn the artefacts instead of the disease. Factors 1–5 target edges, scale, shadows and layout; colour is only partly covered because factor 6 varies brightness and saturation but not hue or white balance. 

Why potato and tomato, and why six classes? Problem 

Both crops share the two most damaging foliar diseases: early blight (Alternaria solani) and late blight (Phytophthora infestans). Six classes are early blight, late blight and healthy for each crop. All 13 tomato and potato classes were extracted, so the other seven are ready for later. 

Why SAM, and not a colour threshold? PlantVillage has no masks. A green threshold removes the yellow–brown lesions, which carry the disease signal. SAM segments zero-shot. We did not compare against GrabCut or Otsu, and masks were not audited against manual masks; both are listed as limitations. Watch out: Do not claim SAM masks are perfect; there is no measured mask IoU. 

Method 

Explain the SAM mask score. Method 

s(M) = 0.20A + 0.28C + 0.30G + 0.12q̂ + 0.10σ − 0.25B. A prefers masks covering about 30% of the image (zero outside 3–95%); C rewards a central centroid; G scores plant colour in HSV and counts yellow–brown (hue 5–25 with saturation ≥ 0.2) as well as green (hue 25–95); q̂ and σ are SAM's predicted IoU and stability; B penalises masks touching the image border. The weights were set by hand, not tuned. 

Why two pools of SAM candidates? 

Method 

The automatic generator sometimes splits a diseased leaf into healthy and lesion parts; a single centre prompt fails when the centre falls on a lesion or on background. We pool both: the selected mask came from the automatic generator for 12,881 images and from centre prompts for 5,281. 

Does the SAM stage reject bad images? Method 

No. It selects the best mask for every image, so every image yields one cutout (18,163). One image failed on a file-write error and was reprocessed. Every cutout is non-empty and a single connected component, but mask quality was not measured. 

Why tile aerial images at native resolution? Method 

Downscaling a large aerial image to 640 px erases ground texture such as furrows and clods, and makes the pasted leaves inconsistent in scale with the background. 65 sources gave 176 tiles: 47 soil, 25 farm, 104 grass by HSV green ratio (<0.15, 0.15– 0.70, >0.70). The compositor samples all tiles uniformly. 

List the seven randomisation factors with values. 

Method 

1 GSD scaling: leaf width 4.5–11.5% of 640 px (29–74 px). 2 Rotation 0–360°. 3 Alpha feathering, Gaussian 0.8 px. 4 Drop shadow, offset (2,3) px, blur 2, opacity 0.30. 5 Clustering around 2–5 plant centres (80% of leaves, σ 40–95 px) plus an IoU guard of 0.50. 6 Photometric jitter: leaf brightness 0.85–1.20, saturation 0.80–1.20, tile brightness 0.85–1.15. 7 Sensor blur with probability 0.25, radius 0.4–0.9 px. 

How are the bounding boxes computed? 

Method 

After rotation and feathering, the alpha channel is thresholded at 20 to find the extent of visible leaf pixels, offset by the paste position, converted to YOLO centre/width/height normalised by 640 and clamped to [0, 1]. Boxes are not shrunk when a later leaf covers part of an earlier one; the IoU guard limits that. 

How was the leaf scale chosen? Is it from a camera model? Method 

No camera model. We assumed about 0.25 cm per pixel (around 5 m altitude), so 8– 18 cm leaves become 29–74 px. The background tiles come from sources of unknown resolution. This is a limitation, and the scale mismatch is the main reason zero-shot transfer fails. 

Why are there 48.1 leaves per image when the target is 15–95? The target comes from a three-mode canopy mix (15–28 with p 0.2, 35–65 with p 0.6, 66–95 with p 0.2). Placements that overlap an existing leaf with IoU above 0.50 are skipped, not retried, so the realised count is lower. 

Method 

Describe the synthetic dataset and split. Dataset 1,200 composites with 57,771 boxes, shuffled with seed 42 and split 80/10/10: 960/120/120 images with 46,561/5,285/5,925 boxes. Instances per class are balanced (9,488–9,770), but distinct cutouts range from 152 (Potato Healthy) to 1,909 (Tomato Late Blight). 

Why did the annotation count change from 56,574 to 57,771? Dataset 

The label files have no trailing newline. Counting with cat and wc -l merged the last line of each file with the next file's first line, so the count was one box short per image. We recounted by parsing every file and corrected the paper, thesis and slides. 

Is your test split really independent? 

Dataset 

Only partly. Test images are new arrangements, but they reuse the same 176 tiles and 6,652 cutouts as training: each cutout appears about 8 times in the dataset, each Potato Healthy cutout about 60 times. So 0.907 measures generalisation within the synthetic distribution, not to new fields. That is why we ran the real-UAV study. 

What training configuration did you use? Both from COCO weights at 640 px, AdamW, 40 epochs, linear LR decay to 1%, weight decay 5e-4, 3 warm-up epochs, AMP, seed 0, mosaic off for the last 10 epochs. YOLOv11m batch 16, LR 1e-3; RT-DETR-L batch 8, LR 1e-4. Early stopping (patience 15) never triggered. Training took 9.3 and 37.2 minutes. 

Results 

Give the main synthetic results. Results YOLOv11m: P 0.918, R 0.836, F1 0.875, mAP@50 0.907, mAP@50–95 0.733, 67.7 FPS. RT-DETR-L: 0.801, 0.704, 0.749, 0.761, 0.542, 31.2 FPS. YOLOv11m is ahead by 0.146 mAP@50 and 0.191 mAP@50–95, and is 2.2× faster. 

Why does RT-DETR-L underperform? Mainly undertraining. It stayed below 0.31 validation mAP@50 for 26 of 40 epochs, jumped at epochs 27–28 and was still improving at epoch 40 (mAP@50–95 0.535 at epoch 32, 0.557 at 39). One-to-one Hungarian matching gives each object a single positive query, a sparser signal than YOLO's one-to-many assigner. Its LR was 10× lower, and each image has about 48 small targets. This is a result at a 40-epoch budget, not a verdict on Transformers. 

Results 

Which class is hardest and why? Results Tomato Late Blight: mAP@50 0.801, recall 0.679, and 16% of its leaves missed as background by YOLOv11m. Its dark, water-soaked lesions look like moist soil and shadow. RT-DETR-L also confuses it with Potato Late Blight (15%) and confuses Tomato Early Blight with Tomato Late Blight (16%). 

Why does Potato Healthy score highest with only 152 cutouts? Because the test split reuses the same small pool of cutouts the model saw during training, each about 60 times. It is evidence of the shared-asset split, not of strong generalisation. 

Results 

Did the model overfit? Not to the validation split: validation beats test by only 0.009–0.016 mAP. It probably does overfit to the synthetic assets, which is why the synthetic numbers are treated as an upper bound. 

Results 

How was FPS measured, and why did the number change from 74.7? 

Results 

Inference only, batch 1, FP32, on the RTX A5000: median of five rounds over the 120 test images after 30 warm-up images; rounds varied by under 0.7 ms. YOLOv11m 67.7 FPS (14.8 ms), RT-DETR-L 31.2 FPS (32.0 ms). The earlier 74.7 and 33.6 had no stored log and could not be reproduced, so we replaced them with the re-measured values. The 2.2× ratio is unchanged. Watch out: Do not quote 74.7 or 33.6. 

How sensitive is YOLOv11m to the confidence threshold? Results 

Not very. The class-averaged F1 curve peaks at 0.874 at a threshold of about 0.43 and stays above 0.85 over a broad range. RT-DETR-L peaks at 0.748 at about 0.55. 

Which real dataset did you use? 

Validation 

Wieme et al. (Frontiers in Plant Science, 2024), 2022 subset: potato early blight (A. solani), flown at 10 m with a 42 MP camera, 135 mm lens and the NIR-blocking filter removed, giving 0.3 mm per pixel. 3,157 patches of 256 px from 281 drone images, 5 plots, 4 dates; 1,027 infected and 2,130 healthy; plot 5 is 96% healthy. Patch labels only, no boxes. 

Why leave-one-plot-out instead of a random split? Patches from the same drone image, and images of the same plot, are nearduplicates. A random patch split put copies of training patches in the test set: YOLOv11m reported 0.88 mAP@50 and RT-DETR-L 0.916 after 120 epochs. Under the plot-level split the same pipeline reaches only 0.59–0.68 AUC. Each fold tests one plot, validates on the next and trains on the rest plus plot 5. 

Validation 

How do you evaluate a detector when you only have patch labels? Validation For training, each infected patch gets a weak box over its central 70%. For evaluation, a patch's score is the highest confidence of any blight detection in it. We report AUC (threshold-free, chance 0.5), AP, and F1 at a threshold chosen on the validation plot. Labelling every patch infected already gives F1 ≈ 0.65, so F1 alone means little. 

Give the real-UAV results. Validation 

Zero-shot: AUC 0.48 ± 0.01 (0.50 counting any blight class). With 10% of real images: 0.47 real-only vs 0.52 pretrained; 25%: 0.56 vs 0.56. With 100% over 3 seeds: 0.59 ± 0.04 vs 0.68 ± 0.13; synthetic pretraining wins 8 of 12 paired runs, mean gain +0.09 ± 0.13. 

Why does zero-shot transfer fail? Validation 

Scale: the real data are about 8× finer (0.3 mm/px), so a patch shows lesions on part of one leaf, while our composites show whole leaves at about 2.5 mm/px. Colour: the camera's red channel is partly NIR-sensitive. The synthetic model has never seen anything like those patches. 

Is the +0.09 AUC gain significant? Validation 

We do not claim significance. With all real data, plot 3 gains in all three seeds (mean +0.25), plot 4 in two of three (+0.11), and plots 1 and 2 show no consistent difference (+0.02, −0.03). Per seed the mean gain is +0.13, +0.02 and +0.11. It is positive on average but depends on the plot and seed. With one seed it looked like +0.13. 

Watch out: Avoid the words 'significant' or 'proves'. 

Did synthetic data reduce how much real data you need? No. With 10% or 25% of the real images both initialisations stay near chance and differ by at most 0.05 AUC. That is the regime where it would matter most, and the current pipeline does not deliver it. 

Validation 

What is the leaf-level PlantDoc experiment in the thesis? 

Validation 

An EfficientNet-B0 classifier trained on the same SAM cutouts scores 0.99 accuracy on PlantVillage test images but 0.45 on 468 PlantDoc field photos, which were segmented the same way. Crop recognition holds up better (0.72–0.73). A cropthen-disease hierarchy gave no gain. It confirms the lab-to-field gap independently of the detector. It is in the thesis, not on the slides. 

What is actually new, given that cut-paste, domain randomisation and SAM all exist? 

Novelty 

The combination for UAV-scale disease detection plus an honest evaluation: a mask score that keeps diseased tissue; real photographed lesions instead of GAN or diffusion targets; seven factors at UAV scale with canopy clustering and rotationaware labels from the alpha mask; and a leakage-free, multi-seed real-UAV test that reports negative results. 

Did you run an ablation of the seven factors? 

Novelty 

No. It is planned: compare against naive copy-paste and remove one factor at a time, evaluated on the same data. Without it, the contribution of each factor is unmeasured. Watch out: Do not quote any copy-paste baseline number; none was produced under the final protocol. 

What optimisations did you apply? 

Novelty 

Native-resolution tiling; IoU guard 0.50; a smaller batch and 10× lower LR for RTDETR-L; mosaic off for the last 10 epochs; mixed precision; ONNX export and WebAssembly inference in a Web Worker for the demo. 

What is your technology stack and hardware? Python 3.13, PyTorch 2.11 with CUDA 12.8, Ultralytics 8.4.154 (YOLO11 and RTDETR), Segment Anything ViT-B, OpenCV 5.0, Pillow 12.3, NumPy 2.5, onnxruntimeweb 1.20.1, Git with LFS. One RTX A5000 (24 GB), Xeon W-2295, 128 GB RAM. 

Implementation 

How do the modules communicate? Implementation Through files on disk in standard formats: RGBA PNG cutouts per class folder, JPEG tiles per category folder, YOLO text labels, data.yaml, fold list files, and a JSON result cache that makes interrupted experiment batches resume. 

#### How did you test the code? 

Implementation 

Checks on the outputs against the specification: 18,163 non-empty singlecomponent cutouts; 57,771 label lines with 0 invalid; no image in two splits; no plot in two parts of any fold; budget subsets keep whole drone images; training arguments match the paper; checkpoints re-evaluated reproduce every accuracy number. There is no automated unit-test suite yet. Watch out: Admit the missing unit tests rather than overstate testing. 

How does the demo work? Implementation 

The YOLOv11m checkpoint is exported to ONNX (77 MB) and run in the browser with onnxruntime-web in a Web Worker; NMS is done in JavaScript. A service worker caches it for offline use, and the user's image never leaves the device. It can tile large photos into 640 px crops. Because the model is trained only on synthetic data, expect misses on real photos. 

What is the critical path? 

Planning 

WP1 → WP2 → WP3 (SAM, 41 h of GPU) → WP4 → WP5 → WP6 → WP7 → WP8 → WP10. The demo (WP9) runs in parallel with WP7–8 and has slack: Slack = LF − (ES + duration). Know the filled-in day values. 

Which risks materialised? Planning 

The GPU crash: running two jobs on one GPU caused a CUDA illegal-memory-access error that stopped the multi-seed CV after 4 of 16 runs. We now run one GPU job at a time and resume from the cache; the CV finished on 30 Oct. Also the sim-to-real gap: zero-shot hit chance, so effort moved to fine-tuning. 

Which SDGs does the project support? 

Impact 

SDG 2 (Zero Hunger), target 2.4: earlier disease detection supports resilient food production. SDG 12: targeted spraying could reduce fungicide use, and the slide maps 12.3 (reducing losses). SDG 9.5: open, reproducible agri-AI research. Yield and fungicide savings were not measured. Watch out: The slide (2.4, 2.3, 12.3, 9.5) and the thesis (2.4, 12.4, 9.5) list different targets; align them before the review. 

Who would use this and what do they need? Impact 

Smallholder farmers need cheap early warning; agronomists and extension officers need field-wide coverage; drone service providers need models without heavy labelling. Today the system supplies training data and a prototype detector, not a field-ready service. 

#### What is the status of the paper? 

Paper 

Drafted and internally reviewed for IEEE CSITSS (hosted by RVCE), revised 29–30 Oct with corrected counts, re-measured FPS and 3-seed real-UAV results. The open item is length: the current build is 10 pages. Funded by BMSCE FRPS, R&D/FRPS-3/202526/CS/1-20. 

What would you do next, in order? 

Future 

1 Camera-matched synthesis: lesions at the target resolution, hue and channel jitter. 2 Factor ablation against naive copy-paste. 3 Asset-disjoint splits. 4 Real box labels on a few hundred UAV frames, and PlantDoc as a test. 5 Train RT-DETR-L to convergence over 3+ seeds. 6 Single-crop scenes with clustered infection. 7 Mask quality control. 

## Tough questions and how to answer them 

The project has real limitations. Reviewers reward a team that names them first and explains what the evidence does and does not show. Never claim more than the numbers. 

##### THEY SAY 

Your synthetic test score is inflated. 

##### YOU ANSWER 

Agree, and say it first: test images reuse the training tiles and cutouts, so 0.907 is an upper bound within the synthetic distribution. That is exactly why we tested on real UAV data, where zero-shot is at chance. 

##### THEY SAY 

So the synthetic data doesn't work on real images? 

##### YOU ANSWER 

Not on its own, and not with little real data. As pretraining with all real data it raised mean AUC from 0.59 to 0.68 over three seeds, winning 8 of 12 runs, mostly on two plots. The cause we identify is an 8× scale gap and NIR-shifted colours, which points to the next step: camera-matched synthesis. 

##### THEY SAY 

Your RT-DETR comparison isn't fair. 

##### YOU ANSWER 

Correct: the 40-epoch budget suited YOLOv11m, and RT-DETR-L was still improving at epoch 40. We compare the two at that budget only; a fair comparison needs training to convergence and an LR sweep. 

##### THEY SAY 

Why no ablation study? 

##### YOU ANSWER 

It was not run under the final protocol, so we report none rather than an unverified number. The plan is naive copy-paste plus onefactor-removed runs on the same test data. 

##### THEY SAY 

Why did your numbers change between versions? 

##### YOU ANSWER 

We audited every figure against the data on disk. The box count was undercounted by one per image (a line-counting error), the old FPS values had no log and could not be reproduced, and the real-UAV gain shrank from +0.13 to +0.09 once three seeds finished. All documents now use the verified values. 

##### THEY SAY 

Only one seed for the synthetic detectors? 

##### YOU ANSWER 

Yes, one run each. The real-UAV full-data conditions have three seeds per fold; the 10%, 25% and zero-shot conditions have one. 

##### THEY SAY 

You never flew your own drone. 

##### YOU ANSWER 

True. Objective O4 changed scope: without annotated in-house flights we used public UAV data with plot and date metadata, which made the leakage-free protocol possible. 

##### THEY SAY 

The SAM masks might be wrong. 

##### YOU ANSWER 

They might. Every image yields its best-scoring mask; masks are non-empty and single-component, but mask IoU against manual masks was not measured and no GrabCut baseline was run. It is listed as future work. 

## Concepts you may be asked to explain 

#### IoU 

Intersection over union of two boxes: overlap area divided by combined area. Used to match predictions to ground truth and in the compositor's 0.50 overlap guard. 

#### mAP@50 and mAP@50–95 

Mean over classes of the area under the precision– recall curve. @50 counts a box correct at IoU ≥ 0.5; @50–95 averages thresholds 0.50 to 0.95, so it rewards tight boxes. 

#### AUC (ROC) 

Probability that a random infected patch scores higher than a random healthy one. 0.5 is chance, 1.0 perfect. Threshold-free; computed as the Mann– Whitney statistic. 

#### Average precision (AP) for patches 

Area under the precision–recall curve of ranked patch scores. Chance equals the infected fraction, 0.44–0.54 per test plot. 

#### Domain randomisation 

Randomising nuisance factors so widely that the real domain looks like one more variation (Tobin et al., Tremblay et al.). 

#### Ground sampling distance (GSD) 

Ground distance covered by one pixel. Ours is assumed at about 2.5 mm/px; the real data is 0.3 mm/px. 

#### NMS 

Non-maximum suppression: removes overlapping duplicate boxes after a dense detector such as YOLO. RT-DETR does not need it. 

#### Hungarian matching 

One-to-one assignment of predictions to groundtruth objects used to train DETR models. Each object gets one positive query, which slows early training. 

#### Task-aligned assigner 

YOLO11's one-to-many assignment: several highquality predictions per object are trained as positives. 

#### CIoU, DFL, GIoU, VFL 

Losses: Complete-IoU and Distribution Focal Loss for YOLO boxes; Generalised IoU, L1 and varifocal loss for RT-DETR. 

#### Leave-one-plot-out CV 

Each fold tests on one whole field plot never seen in training, so correlated patches cannot leak between train and test. 

#### Data leakage 

Test data that is a near-copy of training data. It inflates metrics, as the 0.88 random-split result showed. 

#### SAM ViT-B 

Segment Anything with its smallest image encoder (Vision Transformer, base). Segments from point prompts or automatically from a point grid. 

#### Weak box label 

A box that marks the patch as infected, not the lesion: here the central 70% of each infected patch. 

#### ONNX / WebAssembly 

Portable model format, run in the browser by onnxruntime-web compiled to WebAssembly. 

#### Critical path, slack 

The longest chain of dependent tasks sets the finish date. Slack = LS − ES = LF − EF is how far a task can slip without delaying it. 

## Before the review 

Gaps still open in the deck and the documents. The orange placeholders on the slides must be filled, and the inconsistencies below should be fixed or explained. 

- ±0 Fill the WBS owners and effort for WP1–WP10. 

Slide: Project planning (orange placeholders) 

- ±0 Fill the critical-path slack calculation for WP9 (ES, LF, duration, slack). 

Slide: Project planning 

- ±0 Fill the planned milestone dates and insert the baseline-vs-actual Gantt chart. Slide: Schedule tracking. The thesis already has a Gantt chart (Figure 3.3). 

- ±0 Update the report slide: the thesis is drafted in full (6 chapters, 3 appendices, 79 pages). Slide: Project report and documentation status 

- ±0 Add the similarity score, tool, date and exclusions (target ≤ 20%). Slides: Report status and Research paper status 

- ±0 Fix the paper length: the slide says 9 pages, the current paper build is 10. 

Slide: Research paper status 

- ±0 Align the SDG targets: slide has 2.4, 2.3, 12.3, 9.5; thesis has 2.4, 12.4, 9.5. Slide: SDG mapping vs thesis Section 6.4 

- ±0 Attach submission or review evidence for the paper, if any. 

Slide: Research paper status 

- ±0 Fill in the guide's and co-guide's designations in the thesis (still marked in red). thesis/main.tex macros 

- ±0 Rehearse the live demo and have screenshots ready in case the browser model is slow to load (77 MB). Slide: Implementation and integration 

- ±0 Agree who answers which rubric area, so all three members speak. Team 

Sources: AgroEye thesis (79 pp.), review deck PPT/pp2-ppt.tex, results/cv/summary.md, results/synthetic_eval/. Team: Hemanth R (1BM23CD021), Shakthi Jashwanth (1BM23CD072), Vedantha Vinay Verneker (1BM23CD069). Guides: Prof. Lavanya Naik, Prof. Manoj Kumar S. 

