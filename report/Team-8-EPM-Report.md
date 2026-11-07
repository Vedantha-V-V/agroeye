**B.M.S. COLLEGE OF ENGINEERING (Autonomous College under VTU)** 

**Bull Temple Road, Basavangudi, Bangalore - 560019** 



<!-- Start of picture text -->
EGEOFOF Evy<br>oe QD<br>C ss<br>5 a<br>By G)<br>ee<br>2‘ay. ><br>GALORE . cS<br><!-- End of picture text -->

_a Report on_ 

**CFTR Mutation Pathogenicity Detection Using DNABERT2 Embeddings and Downstream Classification** 

_submitted as the Project Management Capstone Report for the course_ 

**Entrepreneurship & Project Management** 

**(Course Code: 23DC7PCEPM)** 

_in fulfillment of the requirements for the award of degree_ 

**BACHELOR OF ENGINEERING** 

_in_ 

**Computer Science & Engineering (Data Science)** 

_by_ 

**Nazeef Ahsan Rafiqui (1BM23CD040) Yasser Ahmed Mohammed (1BM23CD071) Ayush Khanuja (1BM23CD075)** 

**Under the Guidance of** 

**Dr. B R Shambhavi** 

Professor 

**Department of CSE (Data Science)** , 

**B.M.S. College of Engineering** 

**AY 2026-2027** 

## **Contents** 

|**.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 2**<br>**1. Executive Summary**|
|---|
|**.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 2**<br>**2. Project Foundation**|
|.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 2<br>2.1 Project Attributes|
|.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 2<br>2.2 Balancing Project Constraints|
|.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 3<br>2.3 Project Identification and Selection|
|.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 3<br>2.4 Stakeholder Engagement|
|.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 4<br>2.5 Project Charter|
|.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 4<br>2.6 Request for Proposal and Soliciting Proposals|
|.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 4<br>2.7 Life Cycle and Planning Process|
|**.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 5**<br>**3. Project Planning**|
|.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 5<br>3.1 Project Objective|
|.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 5<br>3.2 Project Scope Document|
|.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 5<br>3.3 Plan for Quality|
|.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 5<br>3.4 Work Breakdown Structure|
|.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 6<br>3.5 Responsibility Assignment Matrix|
|**.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 6**<br>**4. Developing the Schedule**|
|.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 6<br>4.1 Activity List, Resources and Durations|
|.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 7<br>4.2 Network Diagram and Schedule Calculations|
|.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 8<br>4.3 Milestones|
|.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 8<br>4.4 Baseline Schedule|
|.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 8<br>4.5 Project Control Process|
|.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 8<br>4.6 Effects of Actual Schedule Performance|
|.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 9<br>4.7 Incorporating Changes and Updating the Schedule|
|**.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 9**<br>**5. Determining Cost and Budget**|
|.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 9<br>5.1 Estimate Activity Costs and the Total Budgeted Cost|
|.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 10<br>5.2 Time-Phased Budget (Cumulative Budgeted Cost)|
|<br>.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 10<br>5.3 Actual Cost and Committed Cost|
|.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 11<br>5.4 Earned Value of the Work Performed|
|.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 11<br>5.5 Analyse Cost Performance|
|.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 12<br>5.6 Forecast the Cost at Completion|
|**.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 12**<br>**6. Managing Risk**|
|.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 12<br>6.1 Identify and Assess Risks|
|.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 13<br>6.2 Plan Risk Responses|
|.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 13<br>6.3 Monitor Risks|
|**.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 14**<br>**7. The Project Team**|
|.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 14<br>7.1 Team Effectiveness|
|.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 14<br>7.2 Conflict and Problem Solving|
|**.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 15**<br>**8. Lessons Learned and Conclusion**|
|**.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 15**<br>**9. Individual Contribution and Reflection**|
|**.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 17**<br>**Consistency Checks**|
|**.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 18**<br>**Appendices**|
|.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 18<br>Appendix A: Work breakdown structure|
|.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 19<br>Appendix B: Network diagram|
|.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 19<br>Appendix C: Sample weekly status reviews|
|.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 19<br>Appendix D: Effort and cost log|
|<br>.  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . 20<br>Appendix E: Test results and repository|



#### **PROJECT MANAGEMENT** 

# **Capstone Project Report** 

### Application of Project Management Concepts 

|**Field**|**Details**|
|---|---|
|Project Title|CFTR Mutation Pathogenicity Detection Using DNABERT2 Embeddings and Downstream<br>Classification|
|Team Name / ID|Team CFTR-DNABERT2 / CFTR-01|
|Team Members (Name, Roll No.,<br>Role)|Nazeef Ahsan Rafiqui, 1BM23CD040, Team Lead (validation, baselines, embeddings, release)<br>Yasser Ahmed Mohammed, 1BM23CD071, Data engineer and evaluator<br>Ayush Khanuja, 1BM23CD075, Modelling and documentation|
|Course / Section|Project Management (Capstone), B.E. CSE (Data Science), Section A, B.M.S. College of<br>Engineering|
|Faculty Mentor|B R Shambhavi (Dept. of CSE – Data Science); domain co-guide: Hadagali Ashoka (Dept. of<br>Biotechnology)|
|Submission Date|26 Oct 2026|
|Report Status Date (the date all<br>actual figures are as of)|16 Oct 2026 (project closure)|
|Project Start – Planned Finish|2 Feb 2026 – 16 Oct 2026 (Day 185); actual finish 16 Oct 2026, on plan|



_All costs are in Indian Rupees (₹). A working day is 8 hours, Monday to Friday; Day 1 = Monday 2 Feb 2026, holidays not removed. Effort is valued at the course rate card (student ₹200/h = ₹1,600/day; mentor/expert ₹1,000/h). Only a lab PC with GPU was used, so no cash was spent._ 

Project Management Capstone Report – CFTR Mutation Pathogenicity Detection 

Page 1 

### **1. Executive Summary** 

This project built an AI system that classifies mutations in the CFTR gene, the cause of cystic fibrosis, as pathogenic or benign from the DNA sequence around each mutation. It serves genomic researchers, clinicians and genetic counsellors who must triage many rare or uncertain variants (VUS), where expert curation and lab assays are slow and costly. The objective was to deliver, in 185 working days (2 Feb – 16 Oct 2026) and a total budgeted cost (TBC) of ₹1,99,000 plus a ₹19,900 reserve, a genome-validated, leakage-safe classifier on frozen DNABERT2 embeddings with ROC-AUC ≥ 0.65 and pathogenic recall ≥ 80%. Only a lab PC with GPU was used, so no cash was spent. 

**Position at the Status Date (16 Oct 2026):** all 13 work packages are 100% complete. The project finished on the planned date, Day 185, so the schedule variance is 0 days. Cumulative actual cost is ₹2,17,000 against earned value of ₹1,99,000: CPI 0.917 and cost variance −₹18,000, inside the ₹19,900 reserve. Technically, 1,972 of 2,301 variants passed validation, and the tuned XGBoost reached ROC-AUC 0.698, PR-AUC 0.806 and 84.2% pathogenic recall. 

**Top two risks** by likelihood and impact: R3, mutation signal diluted in long windows (ROC-AUC 0.42–0.51 in three phases), and R1, reference or coordinate mismatches (329 variants removed; an FASTA offset error). **Most important lesson:** check quality early. The signal problem and the data-quality problem both cost effort because they were confirmed only after full experimental phases. 

### **2. Project Foundation** 

##### **2.1 Project Attributes** 

|**Attribute**|**Evidence from your project**|
|---|---|
|1. Clear objective|Classify CFTR variants as pathogenic/benign from DNA context with ROC-AUC ≥ 0.65 and recall<br>≥ 80% (achieved 0.698 / 84.2%).|
|2. Interdependent activities|Validation needs the unified schema; embeddings need validated windows; classifiers need<br>embeddings; evaluation needs a leakage-safe split (Table 4.1).|
|3. Various resources|3 students, 2 faculty guides, one lab PC with GPU, 3 databases (CFTR2, ClinVar, gnomAD),<br>GRCh38.p14, Python 3.10, PyTorch 2.7.1, Transformers 4.36.2, pyfaidx, scikit-learn 1.7.2,<br>XGBoost.|
|4. Specific time frame|Capstone with a fixed end date: 2 Feb – 16 Oct 2026; baseline 185 working days.|
|5. Unique, one-time effort|A one-off pipeline for CFTR combining three databases, genome validation,<br>mutation-highlighted 15-nt windows and DNABERT2.|
|6. Customer|Genomic researchers, clinicians and genetic counsellors (variant pre-screening); evaluators and<br>the domain co-guide as proxies.|
|7. Degree of uncertainty|High: it was unknown whether frozen DNA-language-model embeddings could separate the<br>classes; early phases scored ROC-AUC 0.42–0.58.|



_Table 2.1 – Project attributes evidenced_ 

##### **2.2 Balancing Project Constraints** 

|**Constraint**|**Priority**<br>**(1–8)**|**Target / limit**|**Justification**|
|---|---|---|---|
|Quality|1|ROC-AUC ≥ 0.65; recall ≥ 80%; zero<br>train/test overlap; 100% reference-allele<br>match|A pathogenicity tool built on leaked or<br>mislabelled data is worthless; a missed<br>pathogenic variant is the costly error.|
|Schedule|2|Planned and required finish 16 Oct 2026<br>(Day 185)|Fixed academic submission window.|
|Scope|3|CFTR only; 4-stage pipeline; frozen<br>DNABERT2; LogReg + XGBoost|Keeps work within what 3 students can finish<br>and validate.|
|Customer<br>satisfaction|4|Mentor and co-guide acceptance of<br>method and results|Guides reviewed each phase.|



Project Management Capstone Report – CFTR Mutation Pathogenicity Detection 

Page 2 

|**Constraint**|**Priority**<br>**(1–8)**|**Target / limit**|**Justification**|
|---|---|---|---|
|Resources|5|3 students, 1 lab PC with GPU, ~15 mentor<br>hours|Fixed; drove the decision not to fine-tune.|
|Budget (₹)|6|TBC ₹1,99,000 + ₹19,900 reserve =<br>₹2,18,900|Notional effort value; no cash purchases.|
|Risks|7|Reserve ≤ ₹19,900 allocated across 6 risks|Managed through Section 6.|
|Stakeholder<br>support|8|Weekly mentor review|Support was never in doubt.|



_Table 2.2 – Constraint prioritisation_ 

**Trade-off actually made (scope vs. resources/quality):** LoRA fine-tuning of the 117M-parameter model on ~1,500 examples gave a degenerate predictor (every variant called pathogenic, ROC-AUC 0.582, zero true negatives). The team dropped fine-tuning from scope and used frozen DNABERT2 with lightweight classifiers, saving GPU time on a single lab PC and cutting overfitting risk. A second trade-off cut the window from 50 bp to 15 bp, giving up flanking context for mutation-signal density. 

##### **2.3 Project Identification and Selection** 

**Need.** Cystic fibrosis affects about 1 in 2,500–3,500 European-descent newborns; more than 2,000 CFTR variants are catalogued, and F508del alone accounts for ≈65% of alleles, so many rare variants remain unclassified. Tools such as SIFT, PolyPhen-2, CADD and REVEL need handcrafted or pre-computed annotations that rare variants lack. Public sources gave 2,301 labelled variants to learn from. 

|**Criterion**|**Weight (%)**|**A: CFTR classifier**|**B: BRCA1/2 classifier**|**C: Multi-gene**<br>**classifier**|
|---|---|---|---|---|
|Public data availability|25|5|5|4|
|Clinical relevance / need|25|5|5|4|
|Feasibility (3 students, 1 lab PC, ~8<br>months)|20|4|3|2|
|Novelty / research gap|20|4|3|4|
|Domain-guide expertise available|10|5|3|2|
|**Weighted score (max 5)**|100|**4.60**|**4.00**|**3.40**|



_Table 2.3 – Project selection scoring (A = 0.25×5 + 0.25×5 + 0.20×4 + 0.20×4 + 0.10×5 = 4.60)_ 

|**Option**|**Key assumptions made**|**Data gathered to test them**|
|---|---|---|
|A: CFTR|Enough labelled variants exist publicly; a DNA<br>language model carries useful signal|CFTR2 1,128; ClinVar 793; gnomAD 1,036 labelled<br>variants (2,301 after de-duplication)|
|B: BRCA1/2|A larger gene would still be manageable|Not tested: judged larger and harder to validate on<br>one lab PC; kept as future work|
|C: Multi-gene|One model could generalise across genes|Not tested: needs far more data and compute; kept<br>as future work|



_Table 2.4 – Assumptions behind each option_ 

##### **2.4 Stakeholder Engagement** 

|**Stakeholder**|**Interest in the project**|**Influence**<br>**(H/M/L)**|**How they were engaged**|
|---|---|---|---|
|Project team (3 students)|Deliver a working pipeline and<br>report|H|Weekly meeting, shared repository|
|Faculty mentor (B R Shambhavi)|Academic rigour, on-time delivery|H|Weekly review; approved charter and<br>baseline|
|Domain co-guide (Hadagali<br>Ashoka)|Biological validity of labels and<br>interpretation|H|Consulted on database labels and on<br>results|



Project Management Capstone Report – CFTR Mutation Pathogenicity Detection 

Page 3 

|**Stakeholder**|**Interest in the project**|**Influence**<br>**(H/M/L)**|**How they were engaged**|
|---|---|---|---|
|Department / evaluators|Meets capstone standards|H|Reviews and final submission|
|Genomic researchers, clinicians,<br>genetic counsellors|High-recall pre-screening of VUS|M|Requirements taken from literature;<br>recall prioritised|
|Database providers (CFTR2,<br>ClinVar, gnomAD)|Correct citation and use|L|Public data used under their terms and<br>cited|
|Open-source / research<br>community|Reproducible code|L|Code released on GitHub with filtering<br>rules|



_Table 2.5 – Stakeholder register. Support that had to be won: the domain co-guide accepted the frozen-embedding approach only after the LoRA results (ROC-AUC 0.582, zero true negatives) were shown._ 

##### **2.5 Project Charter** 

|**Field**|**Details**|
|---|---|
|Project title and purpose (business<br>case)|CFTR Mutation Pathogenicity Detection using DNABERT2. A low-cost, scalable pre-screening<br>tool that flags likely disease-causing CFTR variants for expert review, in place of slow, costly<br>manual curation for first-pass triage.|
|Project manager, with authority<br>level|Nazeef Ahsan Rafiqui (Team Lead): allocates tasks and makes day-to-day decisions; scope or<br>deadline changes need mentor approval.|
|Measurable objective|Deliver by Day 185 (16 Oct 2026) a validated classifier with ROC-AUC ≥ 0.65 and pathogenic<br>recall ≥ 80% on a leakage-safe split, within TBC ₹1,99,000 (+ ₹19,900 reserve).|
|High-level scope and what is out<br>of scope|In: data integration from CFTR2, ClinVar, gnomAD; GRCh38.p14 validation; 15-nt<br>mutation-highlighted windows; frozen DNABERT2 embeddings; LogReg and XGBoost;<br>evaluation; paper and code. Out: clinical deployment, external clinical-cohort validation,<br>other genes, DNABERT2 fine-tuning, web interface, comparison with other DNA foundation<br>models.|
|Key deliverables and acceptance<br>criteria|Cleaned dataset; embedding pipeline; trained model; evaluation report; IEEE paper; public<br>code. Criteria in Table 3.1.|
|Milestone schedule|13 Feb, 28 Apr, 29 May, 3 Jul, 18 Aug, 29 Sep, 16 Oct 2026 (Table 4.3).|
|Budget and funding limit (₹)|TBC ₹1,99,000 + 10% reserve ₹19,900 = ₹2,18,900. No cash purchases.|
|Assumptions|Public databases stay accessible; the lab PC with GPU is available; GRCh38.p14 can be<br>downloaded; each member works on assigned days at about 8 h/day of effort.|
|Constraints|Fixed end date; small labelled dataset (≈2,000 variants); one lab PC with GPU; 3 members.|
|Major risks known at<br>authorisation|Coordinate/genome-build mismatches; class imbalance; overfitting from a small dataset;<br>leakage from overlapping windows.|
|Approval requirements and<br>success criteria|Mentor sign-off on baseline; success = Table 3.1 criteria met and report accepted.|
|Project Manager signature and<br>date|Nazeef Ahsan Rafiqui, 13 Feb 2026|



_Table 2.6 – Project charter_ 

##### **2.6 Request for Proposal and Soliciting Proposals** 

Not applicable: all data came from free public databases and open-source tools (DNABERT2, PyTorch, scikit-learn, XGBoost, pyfaidx), and processing ran on an existing lab PC with GPU, so nothing was bought or contracted. 

##### **2.7 Life Cycle and Planning Process** 

|**Life-cycle phase**|**Your dates**|**What happened in this phase**|
|---|---|---|
|Initiating|2–13 Feb 2026 (Day 1–10)|Need identified, options scored, charter drafted and<br>approved|
|Planning|2 Feb – 13 Mar 2026 (Day 1–30)|Scope, WBS, schedule, budget and risks defined; literature<br>review and data planning|
|Performing|16 Feb – 29 Sep 2026 (Day 11–172)|Data integration, validation, four experimental phases, final<br>model, evaluation, paper|



Project Management Capstone Report – CFTR Mutation Pathogenicity Detection 

Page 4 

|**Life-cycle phase**|**Your dates**|**What happened in this phase**|
|---|---|---|
|Closing|30 Sep – 16 Oct 2026 (Day 173–185)|Code release, final report, lessons learned|



_Table 2.7 – The project on its life cycle_ 

### **3. Project Planning** 

##### **3.1 Project Objective** 

Deliver, by 16 Oct 2026 (Day 185) and within a total budgeted cost of ₹1,99,000 (reserve ₹19,900 held separately), a genome-validated CFTR pathogenicity classifier built on frozen DNABERT2 embeddings that achieves ROC-AUC ≥ 0.65 and pathogenic recall ≥ 80% on a genomic-bin-held-out test set, with code and an IEEE-format paper. _Expected benefit:_ a reproducible, high-recall pre-screening tool that cuts the number of variants experts must review manually. 

##### **3.2 Project Scope Document** 

|**Section of the scope document**|**Your project**|
|---|---|
|1. Customer requirements|High-recall pathogenic/benign classification from sequence alone; reproducible;<br>leakage-free evaluation; no reliance on pre-computed annotations.|
|2. Statement of work (major tasks)|Collect and standardise three databases; validate against GRCh38.p14; design the sequence<br>representation; extract DNABERT2 embeddings; train and tune classifiers; evaluate;<br>document.|
|3. Deliverables|Unified dataset (1,972 validated variants); embedding and classification code; trained<br>XGBoost model; results (tables, confusion matrix, threshold analysis); IEEE paper; this report.|
|4. Acceptance criteria<br>(quantitative)|100% of retained variants match reference; zero bin overlap between train/test; ROC-AUC ≥<br>0.65; pathogenic recall ≥ 80% at threshold 0.5 (≥ 95% at 0.3); CV std ≤ 0.03.|
|5. Work breakdown structure|See 3.4 and Appendix A.|
|Out of scope|Clinical use; external clinical validation; fine-tuning; other genes; protein-level features; web<br>interface.|
|Assumptions and constraints|As in Table 2.6.|



_Table 3.1 – Project scope document_ 

##### **3.3 Plan for Quality** 

|**Quality measure**|**Target**|**How measured**|**When checked**|
|---|---|---|---|
|Reference-allele validity|100% of retained variants match<br>GRCh38.p14|pyfaidx check: genome[chr][pos−1 :<br>pos−1+len(ref)] == ref|Apr 2026, before any<br>embedding|
|Label integrity|No duplicate (chr, pos, ref, alt)|De-duplication count (2,301 merged)|Mar–Apr 2026|
|Leakage control|Zero overlap of 1-kb bins between<br>train and test|GroupShuffleSplit (1,572 train / 400<br>test)|Before every training run|
|Discrimination|ROC-AUC ≥ 0.65; PR-AUC ≥ 0.80|scikit-learn on 400 test variants|After each experimental<br>phase|
|Sensitivity|Pathogenic recall ≥ 80% at 0.5; ≥<br>95% at 0.3|Confusion matrix, threshold sweep|Final evaluation (Aug<br>2026)|
|Stability|5-fold GroupKFold std ≤ 0.03|Mean ± std ROC-AUC|Aug 2026|
|Reproducibility|Code and filtering rules public,<br>versions pinned|Repository review|Oct 2026|



_Table 3.2 – Quality plan_ 

##### **3.4 Work Breakdown Structure** 

|**WBS number**|**Deliverable / work package**|**Owner (one person)**|**TBC (₹)**|
|---|---|---|---|
|1.1|Planning and charter|Nazeef|16,400|
|1.2|Literature review|Ayush|17,000|
|2.1|Data collection (CFTR2, ClinVar, gnomAD)|Yasser|14,800|



Project Management Capstone Report – CFTR Mutation Pathogenicity Detection 

Page 5 

|**WBS number**|**Deliverable / work package**|**Owner (one person)**|**TBC (₹)**|
|---|---|---|---|
|2.2|Schema standardisation and de-duplication|Yasser|6,400|
|2.3|GRCh38.p14 reference validation|Nazeef|13,800|
|3.1|LoRA fine-tuning baseline (200 bp)|Nazeef|9,600|
|3.2|Stacked and paired embedding experiments (50/25 bp)|Yasser|9,000|
|3.3|Mutation-highlighted 15-nt representation design|Ayush|21,200|
|3.4|DNABERT2 embedding extraction|Nazeef|4,800|
|4.1|Leakage-safe split, classifier training and tuning|Ayush|19,200|
|4.2|Evaluation (CV, threshold, confusion matrix)|Yasser|14,800|
|5.1|IEEE paper writing|Ayush|42,400|
|5.2|Code release and PM report|Nazeef|9,600|
||**Total budgeted cost (TBC)**||**1,99,000**|



_Table 3.3 – WBS with work-package budgets (reserve ₹19,900 shown separately in Table 5.1). WBS diagram in Appendix A._ 

##### **3.5 Responsibility Assignment Matrix** 

|**WBS work package**|**Nazeef**|**Yasser**|**Ayush**|**Mentor / expert**|**Client (end-user**<br>**proxy)**|
|---|---|---|---|---|---|
|1.1 Planning and charter|P|S|S|S||
|1.2 Literature review||S|P|S||
|2.1 Data collection||P|S|S|S|
|2.2 Schema standardisation||P||||
|2.3 Reference validation|P|S||S||
|3.1 LoRA baseline|P|||||
|3.2 Stacked/paired experiments||P||S||
|3.3 Highlighted representation|S|S|P|S||
|3.4 Embedding extraction|P|||||
|4.1 Split, train, tune|S||P|||
|4.2 Evaluation||P|S|S||
|5.1 Paper writing|S|S|P|S|S|
|5.2 Code release and report|P|S|S|||



_Table 3.4 – Responsibility assignment matrix (P = primary, S = support); exactly one P per row_ 

### **4. Developing the Schedule** 

##### **4.1 Activity List, Resources and Durations** 

Estimating method: each activity was estimated by its primary owner (Table 3.4), aggressive yet realistic, and checked at the weekly mentor review. Durations are elapsed working days (members worked part-time alongside coursework); resources show effort in person-days × 8 h. 

|**#**|**Activity**|**Predecesso**<br>**rs**|**Resources (effort hours)**|**Duration**<br>**(days)**|**Estimated by**|
|---|---|---|---|---|---|
|A|Planning and charter|–|Nazeef, Yasser, Ayush × 3 d = 72 h;<br>mentor 2 h|10|Nazeef|
|B|Literature review|A|Ayush, Yasser × 5 d = 80 h; mentor 1 h|20|Ayush|
|C|Data collection|A|Yasser 5 d + Ayush 3 d = 64 h; expert 2 h|20|Yasser|
|D|Schema standardisation and<br>de-duplication|C|Yasser 4 d = 32 h|15|Yasser|
|E|GRCh38.p14 reference validation|D|Nazeef, Yasser × 4 d = 64 h; mentor 1 h|17|Nazeef|
|F|LoRA fine-tuning baseline|E|Nazeef 6 d = 48 h|23|Nazeef|



Project Management Capstone Report – CFTR Mutation Pathogenicity Detection 

Page 6 

|**#**|**Activity**|**Predecesso**<br>**rs**|**Resources (effort hours)**|**Duration**<br>**(days)**|**Estimated by**|
|---|---|---|---|---|---|
|G|Stacked and paired embedding<br>experiments|E|Yasser 5 d = 40 h; mentor 1 h|18|Yasser|
|H|Highlighted 15-nt representation<br>design|F, G|Nazeef, Yasser, Ayush × 4 d = 96 h;<br>mentor 2 h|20|Ayush|
|I|DNABERT2 embedding extraction|H|Nazeef 3 d = 24 h|5|Nazeef|
|J|Split, classifier training and tuning|I|Nazeef, Ayush × 6 d = 96 h|20|Ayush|
|K|Evaluation (CV, threshold, confusion<br>matrix)|J|Yasser, Ayush × 4 d = 64 h; mentor 2 h|12|Yasser|
|L|IEEE paper writing|K, B|Nazeef, Yasser, Ayush × 8 d = 192 h;<br>mentor 4 h|30|Ayush|
|M|Code release and PM report|L|Nazeef, Yasser × 3 d = 48 h|13|Nazeef|



_Table 4.1 – Activities (A=1.1, B=1.2, C=2.1, D=2.2, E=2.3, F=3.1, G=3.2, H=3.3, I=3.4, J=4.1, K=4.2, L=5.1, M=5.2). Planned effort 920 h (115 person-days) + 15 mentor/expert hours._ 

##### **4.2 Network Diagram and Schedule Calculations** 

|**#**|**Activity**|**Duration**|**ES**|**EF**|**LS**|**LF**|**Total**<br>**slack**|**Free slack**|**Critical?**|
|---|---|---|---|---|---|---|---|---|---|
|A|Planning and charter|10|0|10|0|10|0|0|Yes|
|B|Literature review|20|10|30|122|142|112|112|No|
|C|Data collection|20|10|30|10|30|0|0|Yes|
|D|Schema standardisation|15|30|45|30|45|0|0|Yes|
|E|Reference validation|17|45|62|45|62|0|0|Yes|
|F|LoRA baseline|23|62|85|62|85|0|0|Yes|
|G|Stacked/paired experiments|18|62|80|67|85|5|5|No|
|H|Highlighted representation|20|85|105|85|105|0|0|Yes|
|I|Embedding extraction|5|105|110|105|110|0|0|Yes|
|J|Split, train, tune|20|110|130|110|130|0|0|Yes|
|K|Evaluation|12|130|142|130|142|0|0|Yes|
|L|Paper writing|30|142|172|142|172|0|0|Yes|
|M|Code release and report|13|172|185|172|185|0|0|Yes|



_Table 4.2 – Forward and backward pass. Critical path: A → C → D → E → F → H → I → J → K → L → M. Network diagram: Appendix B._ 

**Proof of critical path.** 10 + 20 + 15 + 17 + 23 + 20 + 5 + 20 + 12 + 30 + 13 = 185 days = planned project duration, and every activity on it has total slack LS − ES = 0. 

**Worked calculation (activity G).** Forward pass: ES(G) = EF(E) = 62, so EF(G) = 62 + 18 = 80. Backward pass: LF(G) = LS of its successor H = 85, so LS(G) = 85 − 18 = 67. Total slack = LS − ES = 67 − 62 = 5 days. Free slack = ES(H) − EF(G) = 85 − 80 = 5 days. For B: LF(B) = LS(L) = 142, LS = 122; total slack = 122 − 10 = 112; free slack = ES(L) − EF(B) = 142 − 30 = 112. 

**(a) Most total slack.** The literature review (B) has 112 days of total slack because it only feeds the paper at Day 142. We would use it as a buffer: if validation (E) or representation design (H) ran late, a member could be moved from B to the critical path, finishing the review during evaluation instead. 

**(b) Longest critical activity slipping 5 days.** Paper writing (L, 30 days) is the longest critical activity. A 5-day slip moves L's finish to Day 177 and the project finish to Day 190 (23 Oct), 5 days after the required 16 Oct, because the critical path has zero slack. Slack on the other paths (B = 112, G = 5) is unchanged because both end before L starts. In practice the team added effort to the paper (Table 5.3) so L finished on Day 172. 

Project Management Capstone Report – CFTR Mutation Pathogenicity Detection 

Page 7 

##### **4.3 Milestones** 

|**Milestone**<br>~~e~~|**Planned date**<br>|**Actual / forecast date**<br>|**Status**<br>|
|---|---|---|---|
|M1 Charter approved|Day 10, 13 Feb 2026|13 Feb 2026|Met|
|M2 Validated dataset ready (1,972 variants)|Day 62, 28 Apr 2026|28 Apr 2026|Met|
|M3 Baseline experiments complete (ROC-AUC 0.582 /<br>0.493 / 0.509)|Day 85, 29 May 2026|29 May 2026|Met|
|M4 Embeddings generated (768-d)|Day 110, 3 Jul 2026|3 Jul 2026|Met|
|M5 Final model and evaluation complete|Day 142, 18 Aug 2026|18 Aug 2026|Met|
|M6 Paper complete|Day 172, 29 Sep 2026|29 Sep 2026|Met|
|M7 Project closure|Day 185, 16 Oct 2026|16 Oct 2026|Met|



_Table 4.3 – Milestones (a milestone has zero duration)_ 

##### **4.4 Baseline Schedule** 



<!-- Start of picture text -->
Baseline Gantt chart: filled = critical path (zero slack), outlined = slack<br>Alanning and charter ti oet2026)|<br>Buiteraturereview | [7] sack 1s24 '<br>C Data collection | H<br>D Schema standardisation a i<br>F LoRA baseline a H<br>G Stacked/paired experiments [OT stacks a |<br>H Highlighted representation a |<br>| Embedding extraction | \<br>J Split, train, tune Fe H<br>K Evaluation || '<br>L Paper writing lt<br>Feb Mar Apr May Jun Jul ‘Aug Sep Oct<br><!-- End of picture text -->

_Figure 4.1 – Baseline schedule (Gantt chart), critical path filled, slack shown on non-critical activities. Planned finish: Day 185 (16 Oct 2026), equal to the required completion date, so total slack on the critical path is zero at baseline._ 

##### **4.5 Project Control Process** 

Reporting period: weekly, chosen because phases lasted two to six weeks and the mentor met the team once a week. Each period the team recorded actual start and finish, effort hours, percent complete per work package, and the latest experiment metrics (ROC-AUC, PR-AUC). The three members and the faculty mentor attended; the domain co-guide joined at result reviews. Corrective action was triggered by: schedule variance > 5 days on a critical activity, CPI < 0.90, or an experimental phase with ROC-AUC < 0.55. Baseline fixed on 13 Feb 2026 with the charter. 

##### **4.6 Effects of Actual Schedule Performance** 

|**Activity**|**Planned**<br>**finish**|**Actual finish**|**Varianc**<br>**e (days)**|**Cause**|**Effect on total slack**|
|---|---|---|---|---|---|
|E Reference<br>validation|Day 62 (28<br>Apr)|Day 62 (28<br>Apr)|0|CFTR-only FASTA with a hard-coded offset<br>caused mismatches and near-random<br>results; rebuilt with the full GRCh38.p14<br>genome (+3 person-days)|None: extra effort<br>held the date; slack<br>stays 0|
|F LoRA baseline|Day 85 (29<br>May)|Day 85 (29<br>May)|0|Degenerate output (all pathogenic, 93% class<br>imbalance); extra runs (+1 person-day)|None|
|G Stacked/paired|Day 80 (22<br>May)|Day 80 (22<br>May)|0|Repeated runs at 50 bp and 25 bp (+1<br>person-day)|None: its 5-day<br>slack unchanged|



Project Management Capstone Report – CFTR Mutation Pathogenicity Detection 

Page 8 

|**Activity**|**Planned**<br>**finish**|**Actual finish**|**Varianc**<br>**e (days)**|**Cause**|**Effect on total slack**|
|---|---|---|---|---|---|
|H Highlighted<br>representation|Day 105 (26<br>Jun)|Day 105 (26<br>Jun)|0|Iteration on window size and token format<br>(+2 person-days, +1 mentor hour)|None|
|K Evaluation|Day 142 (18<br>Aug)|Day 142 (18<br>Aug)|0|GroupKFold and threshold analysis added<br>inside the planned 12 days|None|
|L Paper writing|Day 172 (29<br>Sep)|Day 172 (29<br>Sep)|0|Revisions after mentor review (+2<br>person-days, +1 mentor hour)|None|
|M Release and<br>report|Day 185 (16<br>Oct)|Day 185 (16<br>Oct)|0|As planned|Total slack to<br>required date stays<br>0|



_Table 4.4 – Schedule variance analysis: every planned finish was met (variance 0). The cost of holding the dates is the extra effort in Table 5.3._ 

##### **4.7 Incorporating Changes and Updating the Schedule** 

|**Change**<br>**ID**|**Description**|**Impact (scope / days / ₹)**|**Decision**|**Approved by**|
|---|---|---|---|---|
|C1|Drop LoRA fine-tuning; use frozen DNABERT2<br>embeddings with LogReg/XGBoost|Scope: method changed; 0 days;<br>₹1,600|Approved|Mentor, 29 May<br>2026|
|C2|Add gnomAD benign variants (720) to fix class<br>imbalance|Scope: +1 data source; 0 days; ₹0|Approved|Mentor|
|C3|Replace CFTR-only FASTA with full GRCh38.p14<br>and direct pyfaidx queries|Scope: none; 0 days; ₹4,800|Approved|Team lead, 28 Apr<br>2026|
|C4|Reduce window 50 → 25 → 15 bp and use<br>[REF>ALT] highlighting|Scope: representation changed;<br>0 days; ₹4,200|Approved|Mentor, 12 Jun<br>2026|
|C5|Add GroupKFold cross-validation and threshold<br>analysis|Scope: +2 analyses; 0 days; ₹0|Approved|Mentor|



_Table 4.5 – Change request log. Updated finish date: 16 Oct 2026 (Day 185), unchanged. Critical path unchanged (A → C → D → E → F → H → I → J → K → L → M). New total slack to the required date: 0 days. Each change was absorbed by extra effort, shown as cost in Table 5.3._ 

### **5. Determining Cost and Budget** 

Basis: student labour at ₹1,600 per person-day (₹200/h × 8 h) from the rate card; mentor and domain expert at ₹1,000 per hour used. All processing ran on an existing lab PC with GPU, so there were no cash purchases, invoices, cloud or licence costs; equipment and electricity were not charged to the project. 

##### **5.1 Estimate Activity Costs and the Total Budgeted Cost** 

|**WBS**|**Work package**|**Labour (₹)**|**Materials /**<br>**other (₹)**|**Basis of estimate**|**TBC (₹)**|
|---|---|---|---|---|---|
|1.1|Planning and charter|14,400|2,000|9 person-days × 1,600; 2 h ×<br>1,000|16,400|
|1.2|Literature review|16,000|1,000|10 pd; 1 h|17,000|
|2.1|Data collection|12,800|2,000|8 pd; 2 h|14,800|
|2.2|Schema standardisation|6,400|0|4 pd|6,400|
|2.3|Reference validation|12,800|1,000|8 pd; 1 h|13,800|
|3.1|LoRA baseline|9,600|0|6 pd|9,600|
|3.2|Stacked/paired experiments|8,000|1,000|5 pd; 1 h|9,000|
|3.3|Highlighted representation|19,200|2,000|12 pd; 2 h|21,200|
|3.4|Embedding extraction|4,800|0|3 pd|4,800|
|4.1|Split, train, tune|19,200|0|12 pd|19,200|
|4.2|Evaluation|12,800|2,000|8 pd; 2 h|14,800|
|5.1|Paper writing|38,400|4,000|24 pd; 4 h|42,400|



Project Management Capstone Report – CFTR Mutation Pathogenicity Detection 

Page 9 

|**WBS**|**Work package**|**Labour (₹)**|**Materials /**<br>**other (₹)**|**Basis of estimate**|**TBC (₹)**|
|---|---|---|---|---|---|
|5.2|Code release and report|9,600|0|6 pd|9,600|
||**Total budgeted cost (TBC)**|**1,84,000**|**15,000**|115 pd × 1,600 + 15 h ×<br>1,000|**1,99,000**|
||Contingency reserve (10% of TBC, held<br>separately; Table 6.2)|||0.10 × 1,99,000|19,900|
||**Funding limit (TBC + reserve)**||||**2,18,900**|



_Table 5.1 – Activity cost estimates and total budgeted cost (all amounts in ₹; cash cost ₹0)_ 

##### **5.2 Time-Phased Budget (Cumulative Budgeted Cost)** 

Each work package budget is spread evenly over its scheduled working days (Table 4.2) and summed by calendar month (Feb 20, Mar 22, Apr 22, May 21, Jun 22, Jul 23, Aug 21, Sep 22 and 1–16 Oct 12 working days; rounded to the rupee). 

|**WP**|**Feb**|**Mar**|**Apr**|**May**|**Jun**|**Jul**|**Aug**|**Sep**|**Oct**|**Total (₹)**|
|---|---|---|---|---|---|---|---|---|---|---|
|1.1|16,400|||||||||16,400|
|1.2|8,500|8,500||||||||17,000|
|2.1|7,400|7,400||||||||14,800|
|2.2||5,120|1,280|||||||6,400|
|2.3|||13,800|||||||13,800|
|3.1|||835|8,765||||||9,600|
|3.2|||1,000|8,000||||||9,000|
|3.3|||||21,200|||||21,200|
|3.4|||||1,920|2,880||||4,800|
|4.1||||||19,200||||19,200|
|4.2|||||||14,800|||14,800|
|5.1|||||||12,720|29,680||42,400|
|5.2||||||||738|8,862|9,600|
|**Mont**<br>**hly**|**32,300**|**21,020**|**16,915**|**16,765**|**23,120**|**22,080**|**27,520**|**30,418**|**8,862**|**1,99,000**|
|**CBC**|**32,300**|**53,320**|**70,235**|**87,000**|**1,10,120**|**1,32,200**|**1,59,720**|**1,90,138**|**1,99,000**||



_Table 5.2 – Time-phased budget; the last row is the cumulative budgeted cost (CBC). Example: 3.1 = ₹9,600 ÷ 23 days = ₹417/day; 2 days in April = 835, 21 days in May = 8,765._ 

##### **5.3 Actual Cost and Committed Cost** 

Status Date = project closure, so CBC to date equals TBC and nothing is committed but unpaid. Actual cost is the notional value of effort actually worked (125 person-days at ₹1,600, plus 17 mentor/expert hours at ₹1,000) from the weekly effort log (Appendix D). 

|**WBS**|**Work package**|**CBC to date (₹)**|**Spent (₹)**|**Committed (₹)**|**CAC (₹)**|
|---|---|---|---|---|---|
|1.1|Planning and charter|16,400|16,400|0|16,400|
|1.2|Literature review|17,000|17,000|0|17,000|
|2.1|Data collection|14,800|14,800|0|14,800|
|2.2|Schema standardisation|6,400|6,400|0|6,400|
|2.3|Reference validation|13,800|18,600|0|18,600|
|3.1|LoRA baseline|9,600|11,200|0|11,200|
|3.2|Stacked/paired|9,000|10,600|0|10,600|
|3.3|Highlighted representation|21,200|25,400|0|25,400|
|3.4|Embedding extraction|4,800|4,800|0|4,800|
|4.1|Split, train, tune|19,200|20,800|0|20,800|



Project Management Capstone Report – CFTR Mutation Pathogenicity Detection 

Page 10 

|**WBS**|**Work package**|**CBC to date (₹)**|**Spent (₹)**|**Committed (₹)**|**CAC (₹)**|
|---|---|---|---|---|---|
|4.2|Evaluation|14,800|14,800|0|14,800|
|5.1|Paper writing|42,400|46,600|0|46,600|
|5.2|Code release and report|9,600|9,600|0|9,600|
||**Total**|**1,99,000**|**2,17,000**|**0**|**2,17,000**|



_Table 5.3 – Actual and committed cost as of 16 Oct 2026. Overruns: 2.3 +3 pd (FASTA rework), 3.1 +1 pd, 3.2 +1 pd, 3.3 +2 pd and +1 mentor h, 4.1 +1 pd, 5.1 +2 pd and +1 mentor h = 10 pd × 1,600 + 2 h × 1,000 = ₹18,000._ 

##### **5.4 Earned Value of the Work Performed** 

|**WBS**|**Work package**|**TBC (₹)**|**Percent**<br>**complete**|**How judged**|**CEV (₹)**|
|---|---|---|---|---|---|
|1.1–5.2<br>(each)|All 13 work<br>packages|as in Table<br>5.1|100%|Counted complete only when the deliverable<br>met its Table 3.1 criterion and the mentor<br>accepted it at the weekly review (e.g. 2.3: all<br>1,972 retained alleles match GRCh38.p14; 4.2:<br>metrics reproduced from the confusion matrix)|= TBC|
||**Total**|**1,99,000**|**100%**|Judged by the work-package owner, verified by<br>the mentor; in-progress packages reported on<br>completed steps, not hours spent|**1,99,000**|



_Table 5.4 – Cumulative earned value (CEV = TBC × percent complete)_ 

##### **5.5 Analyse Cost Performance** 

|**Measure**|**Formula**|**Value (₹ or ratio)**|**What it tells you**|
|---|---|---|---|
|Total budgeted cost (TBC)|Sum of work package budgets|1,99,000|Approved budget (excl. reserve)|
|Cumulative budgeted cost<br>(CBC)|Budgeted for work scheduled to date<br>(Table 5.2)|1,99,000|All work was scheduled by Oct|
|Cumulative actual cost (CAC)|Spent + committed (Table 5.3)|2,17,000|What the work cost|
|Cumulative earned value<br>(CEV)|TBC × percent complete = 1,99,000 ×<br>100%|1,99,000|Value of work done|
|Cost performance index (CPI)|CEV ÷ CAC = 1,99,000 ÷ 2,17,000|0.917|₹0.92 of value per ₹1 spent:<br>over budget|
|Cost variance (CV)|CEV − CAC = 1,99,000 − 2,17,000|−₹18,000|9.0% over TBC, inside the<br>₹19,900 reserve|



_Table 5.5 – Cost performance as of 16 Oct 2026. Reserve left: 19,900 − 18,000 = ₹1,900. Schedule check: CEV − CBC = 0._ 

|**Month**|**Feb**|**Mar**|**Apr**|**May**|**Jun**|**Jul**|**Aug**|**Sep**|**16 Oct**|
|---|---|---|---|---|---|---|---|---|---|
|**end**||||||||||
|CBC (₹)|32,300|53,320|70,235|87,000|1,10,120|1,32,200|1,59,720|1,90,138|1,99,000|
|CEV (₹)|32,300|53,320|70,235|87,000|1,10,120|1,32,200|1,59,720|1,90,138|1,99,000|
|CAC (₹)|32,300|53,320|75,035|95,000|1,22,320|1,46,000|1,74,780|2,08,138|2,17,000|



_Table 5.5b – Cumulative curves behind Figure 5.1 (CEV from actual progress; CAC adds overruns when they were incurred)_ 

Project Management Capstone Report – CFTR Mutation Pathogenicity Detection 

Page 11 



<!-- Start of picture text -->
Actual cost ran €18,000 over budget while earned value tracked the plan<br>Funding limit €2,18,900 247.000,<br>200 -| “P= CBC= CEV (planned = earned)<br>= CAC (actual cost) %199,000<br>3 150<br>£ 100<br>é<br>50<br>0 Feb Mar Apr May Jun Jul Aug sep 16 Oct<br><!-- End of picture text -->

_Figure 5.1 – Cumulative budgeted, actual and earned value curves. CEV sits on CBC every month (SPI 1.00) because the planned dates were held. CAC rises above both from April, when the reference-validation rework began, and the gap widens to ₹18,000 by September and stays there. That gap is the price of holding the dates: extra effort, not extra time._ 

##### **5.6 Forecast the Cost at Completion** 

At closure nothing remains, so both methods give the actual cost. The mid-project case (end of August, 80% of value earned) shows the full method. 

|**Measure**|**Formula**|**Closure (16 Oct)**|**End Aug (interim)**|**Interpretation**|
|---|---|---|---|---|
|CPI|CEV ÷ CAC|0.917|1,59,720 ÷ 1,74,780 = 0.914|Efficiency held near 0.91<br>all year|
|FCAC, method 1|TBC ÷ CPI|1,99,000 ÷ 0.917 =<br>₹2,17,000|1,99,000 ÷ 0.914 = ₹2,17,765|Rest of the work at today's<br>efficiency|
|FCAC, method 2|CAC + (TBC − CEV)|2,17,000 + 0 =<br>₹2,17,000|1,74,780 + (1,99,000 −<br>1,59,720) = ₹2,14,060|Rest of the work goes<br>exactly to budget|
|Forecast<br>overrun|TBC − FCAC|−₹18,000|−₹18,765 (method 1) /<br>−₹15,060 (method 2)|Compare with the ₹19,900<br>reserve|
|TCPI|(TBC − CEV) ÷ (TBC −<br>CAC)|not meaningful at<br>100%|39,280 ÷ 24,220 = 1.62|Needs 62% better<br>efficiency to hold TBC: not<br>achievable|
|TCPI vs funding<br>limit|(TBC − CEV) ÷ (2,18,900<br>− CAC)|n/a|39,280 ÷ 44,120 = 0.89|Finishing within ₹2,18,900<br>is achievable|



_Table 5.6 – Forecasted cost at completion. Method 1 is the more realistic assumption here: the remaining work (paper and release) kept overrunning, and the final cost of ₹2,17,000 is within 0.4% of the method-1 forecast of ₹2,17,765._ 

### **6. Managing Risk** 

##### **6.1 Identify and Assess Risks** 

|**ID**|**Risk**|**Category**|**Potential impact**|**Likeli-ho**<br>**od**<br>**(H/M/L)**|**Degree of**<br>**impact**<br>**(H/M/L)**|**On critical**<br>**path?**|
|---|---|---|---|---|---|---|
|R3|Single-nucleotide mutation signal<br>diluted in long sequence windows|Technical|Pathogenic and benign<br>embeddings nearly identical;<br>ROC-AUC ≈ 0.5|H|H|Yes (G, H)|
|R1|Reference-allele or coordinate<br>mismatches (different builds, 0- vs<br>1-based SPDI, wrong FASTA offset)|Technical|Mislabelled sequence–label<br>pairs; near-random<br>predictions|H|H|Yes (D, E)|
|R2|Class imbalance (pre-gnomAD<br>data 93% pathogenic)|Technical|Degenerate classifier calling<br>everything pathogenic|H|H|Yes (F)|



Project Management Capstone Report – CFTR Mutation Pathogenicity Detection 

Page 12 

|**ID**|**Risk**|**Category**|**Potential impact**|**Likeli-ho**<br>**od**<br>**(H/M/L)**|**Degree of**<br>**impact**<br>**(H/M/L)**|**On critical**<br>**path?**|
|---|---|---|---|---|---|---|
|R5|Small dataset (~2,000 variants)<br>overfits a 117M-parameter model|Technical|Inflated or unstable results|H|M|Yes (F, J)|
|R4|Data leakage from overlapping<br>15-bp windows|Technical|Over-optimistic metrics,<br>invalid claims|M|H|Yes (J)|
|R9|Code defects (output indexing,<br>variable overwriting)|Technical|Corrupted embeddings,<br>silent errors|M|M|Yes (I)|
|R6|Shared lab PC with GPU not<br>available when needed|External|Delay in embedding<br>extraction and tuning|M|M|Yes (I, J)|
|R7|Team availability (coursework,<br>exams) and deadline pressure on<br>the paper|Human<br>resources|Slipped activities, rushed<br>writing|M|M|Yes (L)|
|R8|Source database changes or<br>becomes unavailable|External|Cannot refresh or reproduce<br>data|L|M|No (C)|



_Table 6.1 – Risk identification and assessment, ranked by likelihood × impact. Critical-path risks R3, R1 and R2 get the highest priority._ 

##### **6.2 Plan Risk Responses** 

|**Risk ID**|**Response**|**Specific action**|**Action on trigger**|**Responsibilit**<br>**y**|**Contingency**<br>**(₹)**|
|---|---|---|---|---|---|
|R3|Mitigate|Shorten window to 15 nt; embed<br>mutation as [REF>ALT] token; test each<br>representation on a small run first|ROC-AUC < 0.55 after a<br>phase|Ayush|5,000|
|R1|Mitigate|Validate every variant with pyfaidx against<br>GRCh38.p14; convert SPDI to 1-based; use<br>the full genome, not a region FASTA|Mismatch rate > 5% or<br>ROC-AUC ≈ 0.50|Nazeef|4,000|
|R2|Mitigate|Add gnomAD benign variants; class<br>weights (scale_pos_weight); report<br>ROC/PR-AUC and confusion matrix, not<br>accuracy alone|Zero true negatives or > 90%<br>predictions in one class|Ayush|3,000|
|R4|Avoid|Group variants into 1-kb bins;<br>GroupShuffleSplit; confirm with<br>GroupKFold|Any bin appears in both train<br>and test|Ayush|2,000|
|R6|Mitigate|Short 15-nt inputs; batched extraction;<br>cache embeddings; book lab slots in<br>advance|Lab PC unavailable > 1 day|Nazeef|2,900|
|R7|Mitigate|Use the 112-day slack on literature review<br>(B) as a buffer; weekly availability check|A member unavailable > 2<br>days on a critical activity|Nazeef|3,000|
|R5|Avoid|Frozen DNABERT2 with lightweight<br>classifiers instead of fine-tuning|Large gap between train and<br>test scores|Ayush|0|
|R9|Mitigate|Distinct variable names; use outputs[0];<br>check embedding shape and variance|NaN or near-identical<br>embeddings|Nazeef|0|
|R8|Accept|Keep local copies of downloaded data and<br>filtering rules|Source unavailable|Yasser|0|
|||||**Total**<br>**allocated**|**19,900**|



_Table 6.2 – Risk assessment matrix: response plans (5,000 + 4,000 + 3,000 + 2,000 + 2,900 + 3,000 = ₹19,900, equal to the reserve in Table 5.1)_ 

##### **6.3 Monitor Risks** 

The risk matrix was reviewed weekly at the mentor meeting and updated after every experimental phase. 

Project Management Capstone Report – CFTR Mutation Pathogenicity Detection 

Page 13 

|**Risk ID**|**Did it occur?**|**Did the trigger warn you in**<br>**time?**|**How the response performed**|**Actual**<br>**cost (₹)**|
|---|---|---|---|---|
|R1|Yes: 329 of 2,301 variants (14.3%)<br>failed validation; the offset-FASTA<br>error gave ROC-AUC ≈ 0.50|Yes: near-random scores<br>appeared on the first run, about<br>a week after the build|Worked: full-genome pyfaidx<br>validation retained 1,972 clean<br>variants|4,800|
|R2|Yes: LoRA run gave recall 1.000,<br>ROC-AUC 0.582, zero true negatives|Yes: zero true negatives was<br>visible at the first evaluation|Worked: gnomAD benign data (720<br>benign) plus class weighting|1,600|
|R3|Yes: ROC-AUC 0.493 / 0.421 / 0.509<br>across three phases|Partly: the trigger fired after<br>Phase 2, but Phase 3 was run<br>before redesign|Worked: highlighted 15-nt windows<br>raised ROC-AUC to 0.698|5,800|
|R4|No (avoided by the bin-based split)|n/a|Confirmed by GroupKFold 0.661 ±<br>0.019|0|
|R5|Partly: needed extra tuning to<br>control overfitting|Yes: train–test gap seen during<br>tuning|Worked: frozen embeddings plus<br>tuned XGBoost|1,600|
|R6|No material delay|n/a|Lab slots booked in advance|0|
|R7|Yes: the paper needed extra<br>revision after mentor review|Yes: draft reviews slipped about<br>a week in August and were<br>flagged at the weekly review|Worked: extra effort held the 29<br>Sep paper date; the buffer was not<br>needed|4,200|
|R8|No|n/a|Local copies kept|0|
|R9|Yes: wrong output index and an<br>overwritten variable|Yes: embeddings looked<br>corrupted on inspection|Worked: fixed with distinct names<br>and outputs[0]|0 (absorb<br>ed in 3.4)|
|**Total**||||**18,000**|



_Table 6.3 – Risk monitoring record. Reserve used: ₹18,000 of ₹19,900. R9 (code defects) was added to the register during development; R5 had no allocation, so its cost came from the pooled reserve._ 

### **7. The Project Team** 

##### **7.1 Team Effectiveness** 

|**Characteristic of an effective team**|**Rating**<br>**(1–5)**|**Evidence from your project**|
|---|---|---|
|Clear understanding of the project<br>objective|4|Seven written objectives and numeric targets (Table 3.1) shared by all<br>members|
|Clear expectations of roles and<br>responsibilities|4|RAM with one P per work package (Table 3.4); a few overlaps in<br>debugging|
|Results orientation|5|Metrics (ROC-AUC, recall) checked after every phase; the approach<br>changed when results were poor|
|High degree of cooperation and<br>collaboration|4|Representation redesign (H) done jointly by all three members with<br>mentor input|
|High level of trust|4|Failed phases (ROC-AUC 0.493, 0.421) were reported openly, not<br>hidden|



_Table 7.1 – Team effectiveness. Biggest barrier: three failed experimental phases in a row, combined with coursework pressure. The team stopped adding experiments, diagnosed the cause (Table 7.2) and agreed one change at a time._ 

##### **7.2 Conflict and Problem Solving** 

**Source and approach.** Source: priorities and work scope – whether to keep fine-tuning DNABERT2 (as planned) or change the sequence representation. Approach used: **collaborating** . The team laid the experiment evidence side by side and agreed with the mentors to test the representation first. This was the right choice: forcing more fine-tuning on ~1,500 examples would have repeated the LoRA failure. 

|**Step**|**What your team did**|
|---|---|
|1. Problem statement (specific, with a|Early models could not separate classes: ROC-AUC 0.582 (LoRA, 200 bp), 0.493|
|measure)|(stacked, 50 bp), 0.421 (paired, 50 bp), 0.509 (paired, 25 bp); target ≥ 0.65|



Project Management Capstone Report – CFTR Mutation Pathogenicity Detection 

Page 14 

|**Step**|**What your team did**|
|---|---|
|2. Potential causes identified|Mutation signal too weak in long windows; class imbalance; overfitting from small data;<br>coordinate errors in the data|
|3. Data gathered; most likely cause<br>verified|Mean embedding-difference norm 0.528 ± 0.469 showed a single-nucleotide change in<br>100 bp is nearly invisible; reference-allele checks confirmed mismatches in the first<br>FASTA|
|4. Possible solutions generated<br>(brainstorming)|Larger windows; more fine-tuning; shorter windows; explicit mutation token; add<br>benign data; fix FASTA|
|5. Criteria set and alternatives<br>evaluated|Raise mutation-signal density, avoid extra compute on one lab PC, avoid overfitting,<br>stay leakage-safe, finish before 16 Oct|
|6. Best solution chosen|Highlighted [REF>ALT] token in a 15-nt window with frozen embeddings, plus gnomAD<br>benign data and full-genome validation|
|7. Project plan revised|Change requests C1–C5 (Table 4.5); schedule and budget updated|
|8. Solution implemented|Phase 4 pipeline built and tuned (XGBoost: 500 trees, depth 5, learning rate 0.03)|
|9. Checked against the measure in step<br>1 – was it solved?|ROC-AUC 0.698 and PR-AUC 0.806; 5-fold CV 0.661 ± 0.019: solved against the 0.65<br>target|



_Table 7.2 – Problem-solving record (nine steps)_ 

### **8. Lessons Learned and Conclusion** 

|**Course tool or concept**|**How you applied it**|**Usefulness**<br>**(1–5)**|**What you would do differently**|
|---|---|---|---|
|Project charter|Fixed objective, targets and the ₹2,18,900<br>limit at the start (Table 2.6)|4|Add an early ROC-AUC checkpoint<br>that forces a rethink sooner|
|Work breakdown structure|13 work packages summing to ₹1,99,000<br>(Table 3.3)|4|Split embedding experiments into<br>smaller packages for finer control|
|Responsibility assignment<br>matrix|One P per package (Table 3.4)|3|Name a deputy for critical-path<br>packages|
|Network diagram and slack|185-day critical path; B has 112 days of<br>slack (Table 4.2)|4|Add a re-plan buffer after the<br>baseline experiments|
|Time-phased budget and<br>earned value|CBC/CEV/CAC in Section 5; CPI 0.917|3|Log actual hours weekly so CPI is<br>measured, not reconstructed|
|Risk assessment matrix|9 risks, reserve allocated (Table 6.2),<br>₹18,000 used|5|Make the R1 and R3 triggers fire on<br>the first run, not after three phases|



_Table 8.1 – Reflection on the tools applied_ 

**What worked.** Early genome validation removed 14.3% of noisy records; representation design gave a 41.6% relative ROC-AUC gain (0.493 → 0.698) with no change in model size; bin-based splitting and cross-validation kept the results honest. **What to improve.** Quality checks came late: three phases were run before the representation problem was fixed, which accounts for most of the ₹18,000 overrun; the team added effort to hold the planned dates. **Tools that earned their keep:** the risk matrix, WBS and critical-path analysis; earned value was less useful on a notional-cost student project because it needs real hours logged weekly. 

**Outcome against the original objective.** Deliverable: met (ROC-AUC 0.698 ≥ 0.65; recall 84.2% ≥ 80%; zero bin overlap; 100% reference match). Schedule: planned and actual finish both Day 185 (16 Oct 2026): on schedule, variance 0. Budget: TBC ₹1,99,000, actual ₹2,17,000 (+₹18,000, 9.0%), within the ₹2,18,900 funding limit; cash spent ₹0. 

### **9. Individual Contribution and Reflection** 

Project Management Capstone Report – CFTR Mutation Pathogenicity Detection 

Page 15 

|**Member**|**WBS packages**<br>**owned (P)**|**Hours worked**|**Main contribution**|**Reflection**<br>**attached?**|
|---|---|---|---|---|
|Nazeef Ahsan Rafiqui,<br>1BM23CD040 (Team Lead)|1.1, 2.3, 3.1, 3.4,<br>5.2|Planned 296 h;<br>actual 320 h|Led planning and charter;<br>reference-genome validation and FASTA<br>fix; LoRA baseline; embedding extraction;<br>code release|Yes (below)|
|Yasser Ahmed<br>Mohammed,<br>1BM23CD071|2.1, 2.2, 3.2, 4.2|Planned 360 h;<br>actual 376 h|Collected and standardised CFTR2, ClinVar<br>and gnomAD data; stacked/paired<br>experiments; evaluation and threshold<br>analysis|Yes (below)|
|Ayush Khanuja,<br>1BM23CD075|1.2, 3.3, 4.1, 5.1|Planned 264 h;<br>actual 304 h|Literature review; highlighted-mutation<br>representation; classifier training and<br>tuning; IEEE paper|Yes (below)|



_Table 9.1 – Individual contribution. Actual hours total 1,000 h (125 person-days), matching Table 5.3._ 

##### **Reflection – Nazeef Ahsan Rafiqui (1BM23CD040)** 

I led the project as Team Lead and was primary owner of 1.1 Planning and charter, 2.3 Reference validation, 3.1 LoRA baseline, 3.4 Embedding extraction and 5.2 Code release and report. I logged 320 hours against 296 planned. I drew up the charter and baseline with the team on 13 February, ran the weekly reviews, validated every variant against GRCh38.p14, built the LoRA baseline and extracted the DNABERT2 embeddings. 

My biggest mistake was in 2.3. I validated variants against a CFTR-only FASTA with a hard-coded coordinate offset because it was quick to set up. Results looked near-random (ROC-AUC about 0.50) and we lost about a week finding the cause. Rebuilding with the full GRCh38.p14 genome cost three extra person-days and ₹4,800 (change C3), the largest single overrun in Table 5.3. I had treated validation as a quick technical step, not as a quality gate with a pass criterion and a trigger. 

What I learned is that quality checks on the critical path must come first, because there is no slack to hide a late discovery: work package E had zero slack, so the team had to buy the dates back with extra effort. I also learned that earned value only helps if actual hours are logged weekly. Next time I would write the acceptance test for each work package before starting it and hold a short risk review at every weekly meeting. 

**Signed:** Nazeef Ahsan Rafiqui, 1BM23CD040, 26 October 2026 

##### **Reflection – Yasser Ahmed Mohammed (1BM23CD071)** 

I was primary owner of 2.1 Data collection, 2.2 Schema standardisation, 3.2 Stacked and paired embedding experiments and 4.2 Evaluation, and logged 376 hours against 360 planned. I collected the CFTR2, ClinVar and gnomAD variants, converted ClinVar's 0-based SPDI positions to 1-based VCF coordinates, removed duplicates from the 2,301 merged variants, ran the 50 bp and 25 bp experiments, and produced the confusion matrix, threshold analysis and GroupKFold results. 

My mistake was in 3.2. I assumed that longer windows would give the model more useful context, so I stacked reference and mutant embeddings at 50 bp and then ran a 25 bp paired version before checking why the first had failed. The embedding-difference norm of 0.528 ± 0.469 already showed that a one-nucleotide change was almost invisible, and I should have tested that hypothesis before running another experiment. The extra round cost one person-day (₹1,600) and delayed the representation redesign. 

I learned that a non-critical activity's slack is a buffer to protect, not time to spend on guesses, and that each experiment should start with a stated hypothesis and a pass or fail number. I also learned to flag poor results to the team lead the same day, since that is what lets a risk trigger work as intended. 

Project Management Capstone Report – CFTR Mutation Pathogenicity Detection 

Page 16 

**Signed:** Yasser Ahmed Mohammed, 1BM23CD071, 26 October 2026 

##### **Reflection – Ayush Khanuja (1BM23CD075)** 

I was primary owner of 1.2 Literature review, 3.3 Highlighted representation design, 4.1 Split, training and tuning, and 5.1 Paper writing, and logged 304 hours against 264 planned. I reviewed SIFT, PolyPhen-2, CADD, REVEL and the DNA language models, designed the [REF>ALT] highlighting with the 15-nucleotide window, trained and tuned the Logistic Regression and XGBoost classifiers on the bin-based split, and wrote the IEEE paper. 

My mistake came in 4.1 and in the earlier baseline review. I read the LoRA run's F1 of 0.971 as a good sign before noticing it came from 93% class imbalance with zero true negatives. Later I used the same variable name for the DNABERT2 backbone and the scikit-learn classifier, which silently invalidated the embedding calls until the results looked wrong. Together with the representation iterations and paper revisions, this added extra effort in 3.3, 4.1 and 5.1 (₹10,000 in Table 5.3). 

What I learned is that a single headline metric is not an acceptance criterion: Table 3.1 needed several measures (ROC-AUC, recall, specificity) from the start. I also learned to build in review time for deliverables on the critical path, and to use the 112-day slack of the literature review earlier to help the activities that had none. 

**Signed:** Ayush Khanuja, 1BM23CD075, 26 October 2026 

### **Consistency Checks** 

|**Check**|**Where it comes from**|**Figure**|**Agrees?**|
|---|---|---|---|
|Work package budgets add up to the project TBC|Table 3.3 = Table 5.1|₹1,99,000|Yes|
|CBC at the Status Date|Table 5.2 = Table 5.5|₹1,99,000|Yes|
|CAC includes committed amounts|Table 5.3 = Table 5.5|₹2,17,000 (committed ₹0)|Yes|
|CEV uses the same percent complete as the status<br>report|Table 5.4 = Section 1|100%|Yes|
|Critical path duration equals the planned project<br>duration|Table 4.2 = Figure 4.1|185 days|Yes|
|Every activity's total slack is consistent with the<br>critical path|Table 4.2|Critical = 0; G = 5; B = 112|Yes|
|Contingency reserve appears in the budget|Table 5.1 = Table 6.2|₹19,900|Yes|
|Each RAM row has exactly one P|Table 3.4|13 rows, 13 P|Yes|
|Actual hours agree across sections|Table 9.1 = Table 5.3|1,000 h = 125 person-days|Yes|
|Reserve used agrees across sections|Table 6.3 = Table 5.5|₹18,000|Yes|



_Table 10.1 – Consistency checks_ 

Project Management Capstone Report – CFTR Mutation Pathogenicity Detection 

Page 17 

### **Appendices** 

##### **Appendix A: Work breakdown structure** 



<!-- Start of picture text -->
Work breakdown structure: 5 deliverables, 13 work packages, one owner each<br>CFTR pathogenicity classifier - TBC 1,99,000 (reserve €19,900 held separately)<br>41 Project533,400management 41.441.2 LiteraturePlanning and reviewcharter- Ayush« Nazeef- ¥17,000- %16,400<br>2Data 2.1 Data collection (3 databases) - Yasser - %14,800<br>35,000 2.2 Schema standardisation - Yasser » %6,400<br>" 2.3 GRCh38.p14 reference validation - Nazeef- 713,800<br>3.2 Stacked/paired experiments » Yasser - £9,000<br>seyerebeddtnes 3.1 LORA baseline (200 bp) - Nazeef - 9,600<br>44,600 3.3 Highlighted 15-nt representation - Ayush - 721,200<br>" 3.4 DNABERT2 embedding extraction - Nazeef - 74,800<br>4 classification 4.1 Split, training and tuning - Ayush - £19,200<br>‘634.000 4.2 Evaluation (CV, threshold) - Yasser - €14,800<br>5 Documentation S.A IEE paper writing» Ayush 842.400<br>852,000 5.2 Code release and PM report - Nazeef - 79,600<br><!-- End of picture text -->

_Work package budgets sum to the TBC of ₹1,99,000 (Table 3.3); the ₹19,900 reserve is held separately._ 

Project Management Capstone Report – CFTR Mutation Pathogenicity Detection 

Page 18 

##### **Appendix B: Network diagram** 



<!-- Start of picture text -->
Network diagram: 11 critical activities set the 185-day finish<br>‘A Planning<br>and chatter - 10 4<br>a Ss<br>€ Data collection-20.4 B Literature review 20d<br>£510-£ 90-15 10-LF 30-150 5 10-€F 90-1 122-1F 142-1 112<br>D Schema standardisation - 15 4<br>a<br>oavmucrve.ns |<br>E585. €F105-1585-1F 105-150<br>| Embedding extraction +5 d<br>£5 105-€F 110-15 105-LF 110-150<br>ERE Filled bones: critical path slack 0)<br>5 10-€F 130-15 110-F 130-150 OutlinedES/EF forwardboxes:pass,slackS/LF(B 112 backwarddays, G5 days)pass, TS=LS~ ES<br>Paper writing -30 4 BieedsLat Day 142<br>5 142-€F 172-15 142-16 172-150<br>M Code release, report- 13d<br>65172. €F 185-15 172-F 185-150<br><!-- End of picture text -->

_ES/EF and LS/LF are from Table 4.2; the baseline Gantt chart is Figure 4.1._ 

##### **Appendix C: Sample weekly status reviews** 

|**Date (Day)**|**Attendees**|**Status**|**Decisions and actions**|
|---|---|---|---|
|24 Apr 2026 (Day<br>60)|Nazeef, Yasser, Ayush,<br>mentor|2.1 and 2.2 complete; 2.3 validation 80%<br>complete; first run on the CFTR-only<br>FASTA gave ROC-AUC ≈ 0.50 and<br>widespread reference mismatches|Rebuild with the full GRCh38.p14<br>genome (C3, +3 person-days); date<br>Day 62 held; risk R1 trigger fired|
|22 May 2026 (Day<br>80)|Nazeef, Yasser, Ayush,<br>mentor, co-guide|3.2 complete (stacked ROC-AUC 0.493,<br>paired 25 bp 0.509); 3.1 LoRA 85%<br>complete (ROC-AUC 0.582, zero true<br>negatives)|Stop fine-tuning and use frozen<br>embeddings (C1, approved 29 May);<br>gnomAD benign data in use (C2); R2<br>and R3 triggers fired|
|26 Jun 2026 (Day<br>105)|Nazeef, Yasser, Ayush,<br>mentor|3.3 complete: highlighted [G>A] 15-nt<br>windows; Logistic Regression ROC-AUC<br>0.686, default XGBoost 0.676. Month-end<br>CPI 0.90 (CEV ₹1,10,120; CAC ₹1,22,320)|Start embedding extraction (3.4)<br>then tuning (4.1); reserve used so far<br>₹12,200 of ₹19,900; plan unchanged|



_Appendix C – Sample weekly status reviews (Fridays)_ 

##### **Appendix D: Effort and cost log** 

|**WBS**|**Work package**|**Planned**|**Actual**|**Planned**|**Actual mentor**|**Actual cost**|
|---|---|---|---|---|---|---|
|||**person-days**|**person-days**|**mentor hours**|**hours**|**(₹)**|
|1.1|Planning and charter|9|9|2|2|16,400|



Project Management Capstone Report – CFTR Mutation Pathogenicity Detection 

Page 19 

|**WBS**|**Work package**|**Planned**<br>**person-days**|**Actual**<br>**person-days**|**Planned**<br>**mentor hours**|**Actual mentor**<br>**hours**|**Actual cost**<br>**(₹)**|
|---|---|---|---|---|---|---|
|1.2|Literature review|10|10|1|1|17,000|
|2.1|Data collection|8|8|2|2|14,800|
|2.2|Schema standardisation|4|4|0|0|6,400|
|2.3|Reference validation|8|11|1|1|18,600|
|3.1|LoRA baseline|6|7|0|0|11,200|
|3.2|Stacked/paired experiments|5|6|1|1|10,600|
|3.3|Highlighted representation|12|14|2|3|25,400|
|3.4|Embedding extraction|3|3|0|0|4,800|
|4.1|Split, train, tune|12|13|0|0|20,800|
|4.2|Evaluation|8|8|2|2|14,800|
|5.1|Paper writing|24|26|4|5|46,600|
|5.2|Code release and report|6|6|0|0|9,600|
||**Total**|**115**|**125**|**15**|**17**|**2,17,000**|



_Appendix D – Cost = person-days × ₹1,600 + mentor hours × ₹1,000. Actual team hours: Nazeef 320, Yasser 376, Ayush 304 = 1,000 h. No cash was spent: the only equipment was the lab PC with GPU, so there are no invoices._ 

##### **Appendix E: Test results and repository** 

Source: IEEE paper “CFTR Mutation Pathogenicity Detection Using DNABERT2 Embeddings and Downstream Classification”. Code: github.com/MrWhoCoded/cftr_disease_detection. 

|**Source**|**Pathogenic**|**Benign**|**Total**|
|---|---|---|---|
|CFTR2|1,091|37|1,128|
|ClinVar|697|96|793|
|gnomAD|316|720|1,036|
|Merged (de-duplicated)|1,479|822|2,301|
|After GRCh38.p14 validation|1,304|668|1,972|



_Table E.1 – Final dataset composition_ 

|**Phase**|**Approach**|**ROC-AUC**|**PR-AUC**|
|---|---|---|---|
|1|LoRA fine-tuning, 200 bp|0.582|–|
|2|Stacked ref/mut, 50 bp|0.493|0.651|
|3|Paired [SEP], 25 bp|0.509|0.664|
|4|Highlighted mutation, 15 bp|0.698|0.806|



_Table E.2 – Performance across experimental phases_ 

|**Classifier (Phase 4)**|**Accuracy**|**ROC-AUC**|**PR-AUC**|**F1**|
|---|---|---|---|---|
|Logistic Regression|0.670|0.686|0.780|0.730|
|XGBoost (default)|0.668|0.676|0.792|0.776|
|XGBoost (tuned)|0.685|0.698|0.806|0.777|



_Table E.3 – Phase 4 classifiers (80/20 genomic-bin split: 1,572 train, 400 test)_ 

||**Predicted benign**|**Predicted pathogenic**|
|---|---|---|
|Actual benign|55 (TN)|85 (FP)|
|Actual pathogenic|41 (FN)|219 (TP)|



_Table E.4 – Confusion matrix, tuned XGBoost. Pathogenic recall 219/260 = 84.2%; benign specificity 55/140 = 39.3%; pathogenic precision 219/304 = 72.0%._ 

|**Threshold**|**Pathogenic recall**|**Benign specificity**|**Accuracy**|
|---|---|---|---|
|0.5|0.842|0.393|0.685|



Project Management Capstone Report – CFTR Mutation Pathogenicity Detection 

Page 20 

|**Threshold**|**Pathogenic recall**|**Benign specificity**|**Accuracy**|
|---|---|---|---|
|0.3|0.962|0.093|0.658|
|0.1|≈ 0.99|≈ 0.02|≈ 0.650|



_Table E.5 – Effect of classification threshold. 5-fold GroupKFold cross-validation: mean ROC-AUC 0.661 ± 0.019._ 

Project Management Capstone Report – CFTR Mutation Pathogenicity Detection 

Page 21 

