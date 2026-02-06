# PET-Protocol: Data and Supplementary Materials

**Repository for the submitted manuscript to *Nature Protocols***

---

## Paper Title

**A Computational Protocol for Uncovering Photoinduced Electron Transfer Mechanisms in Fluorescent Molecules**

---

## Description

This repository contains all data, computational inputs/outputs, scripts, and supplementary videos supporting the protocol described in the manuscript. The protocol provides a step-by-step computational workflow to characterize **Photoinduced Electron Transfer (PET)** in fluorescent molecules using density functional theory (DFT) and time-dependent DFT (TD-DFT), including:

- Ground- and excited-state geometry optimizations  
- Identification of locally excited (LE) vs. charge-transfer (CT) states  
- Calculation of PET-related quantities (e.g., reorganization energies, driving forces)  
- Benchmarking of functional and basis-set choices  

The data are organized by case study and file type to allow full reproduction of the reported results and figures.

---

## Repository Structure

```
PET-Protocol/
├── README.md                 # This file
├── DATA/                     # All computational data and scripts
│   ├── Case_Study-A_BN1-SI/           # BN-1 supplementary (M06-2X, ethanol)
│   ├── Case_Study_B_BODIPY_Benchmarking/  # BODIPY benchmarking (multiple methods)
│   ├── Case_Study_BN-1_Manuscript/    # BN-1 manuscript workflow (ωB97XD, ethanol)
│   ├── Case_Study_C_Rhodamine/       # Si-rhodamine (M06-2X, def2-SVP)
│   ├── Explicit_Solvation/           # Explicit solvation (BDP, water + ethanol)
│   ├── Scripts_and_GaussianStepMaker/ # Python scripts and Step Maker tool
│   ├── .gitattributes
│   └── .gitignore
└── Video_Recordings/         # Supplementary protocol videos
```

---

## DATA Folder — Detailed Description

### 1. **Case_Study-A_BN1-SI**  
**BN-1 molecule, supplementary information (M06-2X / ethanol)**

- **Purpose:** Full protocol run for the BN-1 fluorophore as in the Supporting Information.
- **Method:** M06-2X, ethanol (implicit), numbered steps 00–07.
- **Contents:**
  - `00`–`07`: Gaussian input (`.com`) and output (`.log`) files for each protocol step (ground-state opt, absorption, LE/CT optimizations, single-points).
  - **ET/** subfolder: Charge-transfer (ET) state calculations (e.g. B3LYP for CT step) for steps 04, 06, 07.
- **File types:** `.com` (input), `.log` (output), `.fchk` (formatted checkpoint, where present).

---

### 2. **Case_Study_BN-1_Manuscript**  
**BN-1 manuscript workflow (ωB97XD / ethanol)**

- **Purpose:** Main manuscript workflow for BN-1 used for figures (e.g. Figure 4).
- **Structure:** `Project-1-BN1-WB97XD-Ethanol/`
  - **conformational_search:** Conformational search outputs (e.g. `.xyz`, `.e`, `.bibtex`).
  - **gaussian_input:** All Gaussian input files (`.com`) for the protocol.
  - **gaussian_output:**  
    - Ground-state and excited-state optimizations (`gs_opt`, `LE_opt`, etc.).  
    - Absorption and state-specific calculations (`absorption.log`, `Abs_S1_cLR.log`, `LE_S0_cLR.log`, `LE_S1_cLR.log`).  
    - **CT_state/:** Charge-transfer state geometries and single-points (`CT_S0_cLR`, `CT_S1_cLR`).  
    - **data_for_FIGURE 4.xlsx:** Processed data used to generate Figure 4.
- **File types:** `.com`, `.log`, `.fchk`, `.xlsx`, `.xyz`.

---

### 3. **Case_Study_B_BODIPY_Benchmarking**  
**BODIPY-NH₂ benchmarking (multiple functionals and basis sets)**

- **Purpose:** Benchmarking different DFT/TD-DFT choices (functional, basis set, mixed functional) for the BODIPY case study.
- **Subfolders (examples):**
  - **only-M062x_def2svp**, **only-wb9xd_def2svp**, **only-wb9xd_def2tzvp(def2svp)**, **only-M062x-def2tzvp(def2svp):** Single-functional runs (M06-2X or ωB97XD) with def2-SVP or def2-TZVP.
  - **Mix_fxnal-M062X(B3LYP)-def2svp**, **Mix_fxnal-WB97XD(B3LYP)-def2svp**, etc.: Mixed functional schemes (e.g. B3LYP for CT).
  - **FigureS4-data-wb97xd(b3lyp)-def2SVP:** Data used for Supplementary Figure 4.
  - **def2tzvp-step-1-opt (for FMO analysis only):** Step 1 optimization with def2-TZVP for FMO analysis.
- **Contents:** For each scheme, numbered steps (00, 02–07, etc.) with `.com`/`.log`/`.fchk`; **ET/** subfolders contain CT-state calculations.
- **File types:** `.com`, `.log`, `.fchk`.

---

### 4. **Case_Study_C_Rhodamine**  
**Si-rhodamine (Si-RDM) case study**

- **Purpose:** Protocol application to a Si-rhodamine fluorophore.
- **Structure:** **Si-RDM/**  
  - Steps 01–07: M06-2X, def2-SVP, ethanol (implicit).  
  - **CT/** subfolder: Charge-transfer state outputs for the relevant steps.
- **File types:** `.log`, `.fchk`.

---

### 5. **Explicit_Solvation**  
**Explicit solvation (BDP + water in ethanol)**

- **Purpose:** Example with explicit water molecules (BDP-NH₂) in ethanol.
- **Structure:** **BDP/**
  - **LE/:** Locally excited state with 0, 1, or 2 explicit water molecules (`*_m062x_def2SVP_ethanol`).
  - **CT/:** Charge-transfer state with same solvation models.
- **File types:** `.log`, `.fchk`.

---

### 6. **Scripts_and_GaussianStepMaker**  
**Automation and input generation**

- **Quantum Chemical Calculations Step Maker/**  
  - **StepMaker.exe:** Standalone tool to generate Gaussian input files for the protocol steps.  
  - **httpsgithub.comabedisyedaliabbasQuantum-Chemistry-Software-Input-Generator.zip:** Source/archive for the input generator.
- **scripts/:** Python scripts used in the protocol:
  - **calc_dct.py** — Driving force (ΔG°) and related PET quantities; can use Multiwfn for orbital analysis.
  - **calc_lambda.py** — Reorganization energy (λ) for PET.
  - **dft_scf_energy_parser.py** — Parse SCF energies from Gaussian logs.
  - **excitation_energy_parser.py** — Parse excitation energies from TD-DFT output.
  - **extract_all_results.py** — Extract step, termination, frequency, energy, oscillator strength, etc., from `.log` files into tabular form.
  - **log_to_com.py** — Generate new Gaussian input (`.com`) from a previous `.log` (e.g. for next step).
  - **NegFreqCheck_ver2.py** — Check for negative frequencies (geometry validation).
  - **plot_pes.py** — Plot potential energy surfaces (e.g. for PET states).
  - **tddft_parser.py** — Parse TD-DFT sections from Gaussian output.

---

## File Type Reference

| Extension | Description |
|-----------|-------------|
| `.com` | Gaussian input file (route, geometry, basis set). |
| `.log` | Gaussian text output (geometry, energies, frequencies, TD-DFT). |
| `.fchk` | Formatted checkpoint (density, orbitals, etc.); tracked with Git LFS. |
| `.xyz` | Cartesian coordinates (e.g. conformational search). |
| `.xlsx` | Processed data (e.g. for figures). |

---

## Video_Recordings

Supplementary videos that accompany the protocol:

- **Input_Generator_Video.mov** — How to use the input generator / Step Maker.
- **Supplementary Video 1.mov** – **Supplementary Video 19.mov** — Step-by-step protocol videos.
- **Supplementary Video A How_to_Submit_Cals_On_HPC.mov** — Submitting calculations on an HPC cluster.
- **Supplementary Video B HPC_vs_Local_Machine.mov** — HPC vs. local machine workflow.

---

## Usage Notes

- **Reproducibility:** Use the same software versions and options as in the manuscript (e.g. Gaussian 16/09, Multiwfn where cited).
- **Paths:** Scripts may contain user-specific paths (e.g. `Multiwfn.exe` in `calc_dct.py`); update these for your system.
- **Large files:** `.fchk` files are stored with Git LFS; ensure Git LFS is installed and that you run `git lfs install` before cloning if you need them.

---

## Citation

If you use this data or protocol in your work, please cite the manuscript when it is published:

> *A Computational Protocol for Uncovering Photoinduced Electron Transfer Mechanisms in Fluorescent Molecules* (submitted to *Nature Protocols*).

---

## License and Contact

See the manuscript and repository for license and contact information.
