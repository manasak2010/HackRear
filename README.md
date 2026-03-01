# Clinical Phenotype Extraction Pipeline

This repository contains a modular NLP pipeline that processes unstructured clinical notes and converts them into structured phenotype data. The system extracts **explicitly excluded findings**, maps them to **Human Phenotype Ontology (HPO)** terms, evaluates performance against a gold dataset, and displays everything in a **Streamlit dashboard**.

---

## Features

- **Exclusion Extraction (Module B)**  
  Detects negated clinical findings (e.g., “no seizures”) using spaCy + negspacy.

- **HPO Mapping (Module A)**  
  Maps extracted mentions to HPO IDs using the official `hp.obo` ontology.

- **Evaluation (Module C)**  
  Compares module outputs with manually prepared gold annotations and computes **Micro F1** and **Macro F1** scores.

- **Streamlit Dashboard**  
  View clinical notes, extracted findings, and evaluation metrics with a clean UI.

---

## Project Structure
project/
│── streamlit_app.py
│── modules/
│ ├── module_a.py
│ ├── module_b.py
│ └── module_c.py
│
│── data/
│ ├── notes/
│ ├── gold/
│ └── outputs/
│
│── resources/
│ ├── hp.obo
│ └── sample_cases/
│
│── requirements.txt
└── README.md



---

## Workflow

1. **Input** → Raw clinical note  
2. **Module B** → Extract negated findings → `B_out_case.json`  
3. **Module A** → Map findings to HPO terms → `A_out_case.json`  
4. **Module C** → Compare with gold dataset → F1 scores  
5. **Dashboard** → Visualize results interactively

---

## Evaluation Metrics

- **Micro F1 Score:** Overall performance across all mentions  
- **Macro F1 Score:** Class-level performance across phenotypes

---

## Installation

```bash
pip install -r requirements.txt



## Run the Streamlit App
streamlit run streamlit_app.py
