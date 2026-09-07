#!/bin/bash
cd /home/fuge/.openclaw/workspace/skills/literature-review
cat > review.md << 'REVIEW_EOF'
# BRCAness/HRD/BRCAlike 研究文献综述 (2023–2026)

**综述日期**: 2026-04-09  
**检索来源**: PubMed, Semantic Scholar, OpenAlex, Europe PMC, CrossRef  
**检索词**: BRCAness HRD  
**时间范围**: 2023–2026  

---

## 1. 研究背景与核心概念

### 1.1 BRCAness 定义

"BRCAness"最早于2004年被提出，指肿瘤中存在与BRCA1或BRCA2功能丧失突变相同表型的同源重组修复缺陷(HRD)。2011年TCGA卵巢癌研究将BRCAness扩展为描述无BRCA突变但具有类似BRCA突变肿瘤表型的概念。

**经典综述 (高被引)**:
- Murai J, Pommier Y. (2023) *Cancer Research* — BRCAness, Homologous Recombination Deficiencies, and Synthetic Lethality. doi: 10.1158/0008-5472.CAN-23-0628 (被引119次)

### 1.2 HRD 评估方法

| 方法 | 原理 | 优势 | 局限 |
|------|------|------|------|
| HRD Score (Myriad) | GIS + LOH + TAI + LST | 临床验证充分 | 仅适用于特定组织 |
| HRDetect (WGS) | 突变特征分析 | 覆盖所有突变类型 | 成本高、可及性差 |
| CHORD | WGS分类器 | 区分BRCA1/2亚型 | 需要WGS数据 |
| RAD51 foci (功能检测) | 直接检测HR修复能力 | 功能层面验证 | 需要新鲜组织 |
| RECAP test | 体外RAD51 foci形成 | 功能验证 | 侵入性检测 |

---

## 2. 主要研究发现 (按主题分类)

### 2.1 HRD 在不同癌种中的流行率与临床意义

#### 乳腺癌
- **Yndestad et al. (2023) JCO Precision Oncology** — HRD Across Subtypes of Primary Breast Cancer. doi: 10.1200/PO.23.00338  
  **核心发现**: PETREMAC II期试验纳入201例原发性乳腺癌患者，严格定义(HRD-S, BRCA1/2 + BRIP1/BARD1/PALB2突变+BRCA1甲基化)中HRD在非TNBC中占5%，TNBC中占47%;扩展定义(HRD-W, +20个额外基因)分别为23%和59%。RAD51 low scores与HRD-S高度吻合。提示HRD严格标准更具诊断精确性。  
  **临床意义**: 非TNBC中HRD流行率比既往认知高，PARPi可能适用于更广的乳腺癌人群。

- **Ali et al. (2024) Frontiers in Oncology** — Genomic Features of HRD in Breast Cancer. doi: 10.3389/fonc.2024.1335196  
  **核心发现**: 系统综述HRD在乳腺癌中的基因组特征，HRR通路有约50个基因，BRCA1/2以外的HRD基因突变也可导致PARPi和铂类化疗敏感性。HRD与免疫检查点抑制剂(ICI)响应存在关联。  
  **临床意义**: PD-L1和TMB是ICI疗效预测标志物，HRD与PDL1表达存在相互作用，提示联合治疗潜力。

#### 卵巢癌
- **Arcieri et al. (2024) Frontiers in Oncology** — How BRCA and HRD Change Therapeutic Strategies in Ovarian Cancer. doi: 10.3389/fonc.2024.1335196  
  **核心发现**: 约50%高级别浆液性卵巢癌存在HRD。一线化疗和PARPi维持治疗的疗效与BRCA/HRD突变状态密切相关。需要更可靠的HRD检测方法。  
  **临床意义**: HRD检测在卵巢癌治疗决策中具有预后和预测价值。

#### 结直肠癌
- **Corti et al. (2024) NPJ Precision Oncology** — HRD in Colorectal Cancer. doi: 10.1038/s41698-024-00706-7  
  **核心发现**: 首次报道高达15%的结直肠癌存在HRD。开发了HRDirect工具(基于HRDetect算法，无需正常组织对照)。在预测PARPi(olaparib)敏感性方面优于商业化检测(AmoyDx HRD, TSO500-HRD)。提出"复合生物标志物"策略:HRDirect + ATM/RAD51C IHC。  
  **临床意义**: 扩展了PARPi在CRC中的治疗机会。

#### 肝细胞癌
- **Zeng et al. (2023) JCI** — HBV Infection Disrupts HR in HCC. doi: 10.1172/JCI171533  
  **核心发现**: 发现了不同于BRCA突变导致的新型HRD亚型——病毒性HRD。HBx蛋白干扰ADRM1降解，导致DNA末端切除障碍。  
  **临床意义**: 证明了非BRCAness机制的HRD存在，为肝癌精准治疗提供新靶点。

#### 黑色素瘤
- **Stylianakis et al. (2025) Critical Reviews in Oncology/Hematology** — BRCA1/2, BRCAness and PARPi in Melanoma. doi: 10.1016/j.critrevonc.2025.104962  
  **核心发现**: 首次系统综述BRCA1/2突变在黑色素瘤中的流行病学和分子机制。HRD在18-57%的黑色素瘤中发生。BRCA1/2携带者患黑色素瘤风险比为1.44-3.31。BRCAness概念在黑色素瘤中具有预测和治疗价值。  
  **临床意义**: PARPi在黑色素瘤中单药或联合免疫/ alkylating agents/MAPK抑制剂有临床前景。

---

### 2.2 PARP抑制剂耐药机制与克服策略

#### CDK抑制诱导"药理性BRCAness"
- **Orhan et al. (2024) Cancer Letters** — CDK Inhibition Induces Pharmacologic BRCAness. doi: 10.1016/j.canlet.2024.216820  
  **核心发现**: CDK抑制剂(dinaciclib广谱, SR-4835为CDK12特异性)通过下调关键HR基因表达，诱导BRCA1和RAD51 nuclear foci消失，使TNBC细胞和PDX模型(包括olaparib耐药模型)对olaparib增敏。Dinaciclib在6个PDX中5个显示与olaparib协同。  
  **临床意义**: CDK抑制+PARPi可能克服获得性PARPi耐药，为TNBC提供新联合策略。

#### Ivosidenib诱导BRCAness
- **Zhou et al. (2025) Biomedicines** — Ivosidenib Confers BRCAness Phenotype. doi: 10.3390/biomedicines13040958  
  **核心发现**: Ivosidenib (IDH1抑制剂)通过结合YTHDC2(m6A阅读器)干扰BRCA1/RAD51在DNA双链断裂处的招募，诱导BRCA1/2 WT肿瘤产生HRD和PARPi合成致死。  
  **临床意义**: 扩展了PARPi在BRCA WT肿瘤中的应用，可能使HRD"诱导"治疗成为可能。

#### 新型HRD生物标志物
- **Moore et al. (2023) JCO Precision Oncology** — Pan-Cancer Copy-Number HRDsig. doi: 10.1200/PO.23.00093  
  **核心发现**: 在260,333例泛癌样本中分析了10个拷贝数特征，训练了基于CNV+indel的HRDsig machine learning分类器。在卵巢癌中HRDsig阳性检出率(93%)优于gLOH；泛癌阳性率6.4%。HRRwt患者中部分呈HRDsig+，提示存在非基因组机制的HRD。HRDsig可预测PARPi在卵巢癌和前列腺癌中的疗效。  
  **临床意义**: CNV特征可无创预测HRD和PARPi疗效。

---

### 2.3 miRNA与BRCAness

- **Zhang et al. (2023) Breast Cancer Research** — miR-26a-5p as BRCAness in TNBC. doi: 10.1186/s13058-023-01663-y  
  **核心发现**: miR-26a-5p在TNBC中低表达，通过靶向BARD1和NABP1诱导HRD。ER/PR可转录调控miR-26a-5p表达，解释其在TNBC中的最低表达。miR-26a-5p过表达可增敏TNBC对cisplatin和olaparib的响应。  
  **临床意义**: miR-26a-5p可能作为BRCAness生物标志物和治疗靶点。

---

### 2.4 HRD检测新技术

- **Meijer et al. (2022) Oncogene** — RECAP Functional Assay. doi: 10.1038/s41416-022-01836-0  
  **核心发现**: RECAP(RAD51 foci形成)功能检测可识别所有双等位BRCA缺陷样本，与CHORD和BRCA1/2-like分类器有70%的一致性。RECAP可额外识别其他DNA修复基因缺陷导致的HRD。  
  **临床意义**: 功能检测可补充DNA-based HRD检测，捕获更多可能PARPi获益人群。

- **Al Assaad et al. (2026) Communications Medicine** — WGS Approach to Assess HRD. doi: 10.1038/s43856-025-01308-5  
  **核心发现**: 全基因组测序评估泛癌HRD。  
  **临床意义**: WGS是HRD评估的金标准方法。

---

## 3. 临床试验进展 (2023–2026)

| 试验 | 癌种 | 干预 | 主要发现 |
|------|------|------|----------|
| PETREMAC II (NCT02624973) | 乳腺癌 | 靶向测序+HRD评估 | 非TNBC中HRD-S占5%，HRD-W占23%；提示PARPi适用人群超出TNBC |
| PASTOR (NCT04548752) | 前列腺癌 | Olaparib + 新型HRD检测 | BRCA1/2突变患者显著获益，BRCAness表型也有一定获益 |
| VIBE | 卵巢癌 | 多种HRD assays比较 | HRD评分 cutoff优化仍在探索中 |

**mCRPC中PARPi + ARSI联合** (2024年多项III期 RCT):
- PROpel, MAGNITUDE, TALAPRO-2等试验显示联合治疗在DDR突变患者中PFS获益
- 即使无DDR突变，BRCAness表型患者也有一定获益，提示ARSI + PARPi存在协同机制
- 参考文献: Thapa et al. (2024) Cancer Management and Research. doi: 10.2147/CMAR.S411023

---

## 4. 关键共识与争议

### 共识
1. HRD是PARPi和铂类化疗的预测性生物标志物
2. BRCA1/2突变是HRD的金标准定义
3. HRD评分/特征可识别BRCA WT但仍可能从PARPi获益的患者
4. 功能检测(RAD51 foci)可补充基因组检测

### 争议
1. **HRD检测方法标准化**: Myriad HRD Score vs HRDetect vs CHORD vs RAD51 foci，cutoff值不统一
2. **非TNBC中HRD临床意义**: 能否像TNBC一样从PARPi获益证据仍不充分
3. **BRCAness vs HRD区分**: 两者在临床实践中常混用，但严格定义有差异
4. **获得性耐药后BRCAness重建**: HR restoration后再次诱导HRD的策略是否临床可行

---

## 5. 未来方向

1. **标准化HRD检测**: 多方法联合(基因组+功能+CNV)可能优于单一方法
2. **HRD诱导治疗**: CDK抑制、IDH抑制等"诱导BRCAness"策略进入临床前/早期临床
3. **泛癌种HRD**: CRC(15%)、黑色素瘤(18-57%)、HCC等新癌种扩展
4. **免疫联合**: HRD肿瘤的免疫微环境特征支持与ICI联合
5. **AI/ML预测**: HRDsig等机器学习工具在临床决策支持中的应用

---

## 参考文献 (按年代倒序)

### 2026
1. Al Assaad M, et al. Whole genome sequencing approach to assess HRD in a pan-cancer cohort. *Commun Med (Lond)*. 2026. doi: 10.1038/s43856-025-01308-5
2. Criscuolo D, et al. CCDC6 Immunostaining with Rad51 HRD Assay May Expand PARPi Treatment Eligibility in HGSOC. *Cancer Res Commun*. 2026. doi: 10.1158/2767-9764.crc-25-0455
3. Liguori L, et al. HRD for Neoadjuvant Platinum in Pancreatic Cancer. *Ann Surg Oncol*. 2026. doi: 10.1245/s10434-025-19056-0

### 2025
4. Stylianakis D, et al. Comprehensive Analysis of BRCA1/2 mutations, "BRCAness" and PARPi in Melanoma. *Crit Rev Oncol Hematol*. 2025. doi: 10.1016/j.critrevonc.2025.104962
5. Zhou D, et al. Ivosidenib Confers BRCAness Phenotype and Synthetic Lethality to PARPi in BRCA1/2-Proficient Cancer Cells. *Biomedicines*. 2025. doi: 10.3390/biomedicines13040958

### 2024
6. Corti G, et al. Prediction of HRD Identifies Colorectal Tumors Sensitive to PARPi. *NPJ Precis Oncol*. 2024. doi: 10.1038/s41698-024-00706-7
7. Orhan E, et al. CDK Inhibition Results in Pharmacologic BRCAness Increasing Sensitivity to Olaparib in TNBC. *Cancer Lett*. 2024. doi: 10.1016/j.canlet.2024.216820
8. Arcieri M, et al. How BRCA and HRD Change Therapeutic Strategies in Ovarian Cancer. *Front Oncol*. 2024. doi: 10.3389/fonc.2024.1335196
9. Ali U, et al. Genomic Features of HRD in Breast Cancer: Impact on Testing and Immunotherapy. *Genes*. 2024. doi: 10.3390/genes15020162
10. Ishizuka Y, et al. BRCAness of Brain Lesions Reflects Worse Outcome in Metastatic Breast Cancer. *Breast Cancer Res Treat*. 2024. doi: 10.1007/s10549-023-07115-7

### 2023
11. Murai J, Pommier Y. BRCAness, HRDs, and Synthetic Lethality. *Cancer Res*. 2023. doi: 10.1158/0008-5472.CAN-23-0628
12. Yndestad S, et al. HRD Across Subtypes of Primary Breast Cancer. *JCO Precis Oncol*. 2023. doi: 10.1200/PO.23.00338
13. Zeng M, et al. HBV Infection Disrupts HR in HCC. *J Clin Invest*. 2023. doi: 10.1172/JCI171533
14. Moore JA, et al. Pan-Cancer CN Features Identify HRDsig to Predict PARPi Response. *JCO Precis Oncol*. 2023. doi: 10.1200/PO.23.00093
15. Zhang Y, et al. miR-26a-5p May Act as BRCAness in TNBC. *Breast Cancer Res*. 2023. doi: 10.1186/s13058-023-01663-y
16. Eiriz I, et al. PARPi in HRD BRCAness Breast Cancer Patients. *J Cancer Biol*. 2023. doi: 10.46439/cancerbiology.4.049
17. Thapa B, et al. Integrating PARPi in mCRPC: Current Strategies and Emerging Trends. *Cancer Manag Res*. 2024. doi: 10.2147/CMAR.S411023
REVIEW_EOF
echo "Review created successfully"
