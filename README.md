<div align="center">

# 🛡️ VIGILOX Document Intelligence Research

### Research, Evaluation and Engineering Evolution of an AI-Powered Document Intelligence System

**OCR · LLM Extraction · Evidence Validation · Human Review · Evaluation · Production Engineering**

<br>

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Research_API-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![PaddleOCR](https://img.shields.io/badge/OCR-PaddleOCR-0052CC)](https://github.com/PaddlePaddle/PaddleOCR)
[![Groq](https://img.shields.io/badge/LLM-Groq-F55036)](https://groq.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Deterministic_Gate-72%2F72_Passing-brightgreen)](#testing)

<br>

[Overview](#overview) •
[Research Goals](#research-goals) •
[Phases](#research--development-phases) •
[Architecture](#system-evolution) •
[Evaluation](#evaluation) •
[Testing](#testing) •
[Repository](#repository-structure) •
[Setup](#local-setup) •
[Developer](#-developer)

</div>

---

## Overview

**VIGILOX Document Intelligence Research** documents the complete research and engineering journey behind the VIGILOX security-document processing platform.

The project began as an OCR and structured extraction experiment and progressively evolved into a production-oriented Document Intelligence system capable of processing:

- Security Guard Licences
- ID Cards
- SIA Badges

The research covers the complete lifecycle:

```text
Document Image
      ↓
Image Preprocessing
      ↓
PaddleOCR
      ↓
Structured LLM Extraction
      ↓
Schema Validation
      ↓
OCR Evidence Validation
      ↓
Confidence Analysis
      ↓
Date / Logical Validation
      ↓
Image Quality Assessment
      ↓
Machine Decision
      ↓
Human Review
      ↓
Final Effective Record
      ↓
Audit History
```

This repository is intentionally organized as a **research and engineering archive**, rather than as the main deployment repository.

It preserves:

- early experimental implementations
- the evolved implementation snapshot
- phase-by-phase engineering notes
- evaluation datasets and reports
- testing infrastructure
- benchmark scripts
- production-readiness research
- deployment verification notes

---

# Research Goals

The original objective was to investigate how OCR and LLM-based extraction could be combined into a reliable document-processing workflow for security and compliance use cases.

The initial target was:

> Build a service that ingests security guard licences, identity cards, and SIA badges, extracts structured fields using OCR and an LLM, validates them against an expected schema, and flags anomalies or expiry information.

The research also explored what **production-ready Document Intelligence** should mean in practice.

This included:

- field-level confidence
- source evidence
- human review
- immutable machine extraction
- final authoritative records
- audit history
- durable background processing
- failure recovery
- duplicate detection
- quality assessment
- security boundaries
- observability
- evaluation
- release verification

---

# Core Research Questions

The project evolved around several engineering questions.

### Can OCR reliably recover document text?

PaddleOCR was evaluated for structured security and identity documents under clean and degraded image conditions.

### Can an LLM convert OCR text into structured records?

Groq-hosted language models were used to map OCR output into document-specific Pydantic schemas.

### Can extracted fields be linked back to source evidence?

OCR line identifiers and bounding boxes were retained so extracted values could be visually verified against the original document.

### Is OCR confidence equivalent to semantic correctness?

No.

The research showed that strong OCR confidence does not guarantee that an LLM assigned the value to the correct semantic field.

### When should a document be automatically accepted?

Only when evidence, required fields, validation rules, document support, and quality checks justify automatic acceptance.

### How should uncertainty be handled?

Through human review rather than unsupported confidence or risk claims.

### How should expensive processing be executed reliably?

Through durable PostgreSQL-backed jobs and background workers rather than long browser requests.

---

# Research & Development Phases

The repository documents the project as a sequence of research and engineering phases.

```text
Phase 1
OCR Foundation
      ↓
Phase 2
Structured LLM Extraction
      ↓
Phase 3
Evidence Validation
      ↓
Phase 4
Confidence, Dates & Anomalies
      ↓
Phase 5
Human Review & Audit
      ↓
Phase 6
FastAPI, PostgreSQL & Evaluation
      ↓
Phase 7 / 7C
Review Workflow & Integrity
      ↓
Phase 8
Professional UI / UX
      ↓
Phase 9
Async Processing & Performance
      ↓
Phase 10
Advanced Document Intelligence
      ↓
Phase 11
Production Hardening
      ↓
Phase 12
Final Verification
      ↓
Deployment Research
Cloudflare Public Demo Verification
```

---

## Phase 1 — OCR Foundation

Phase 1 established the document preprocessing and OCR pipeline.

Research included:

- image loading
- rotation handling
- image normalization
- text-region extraction
- OCR confidence
- OCR line structures
- bounding-box preservation

PaddleOCR became the primary OCR engine.

---

## Phase 2 — Structured LLM Extraction

Phase 2 introduced structured extraction from OCR output.

The workflow became:

```text
OCR Text
   ↓
Groq LLM
   ↓
Document-Specific Schema
   ↓
Pydantic Validation
```

The phase explored how language models could convert unstructured OCR text into machine-readable security-document records.

---

## Phase 3 — Evidence Validation

Phase 3 connected extracted values back to OCR evidence.

```text
Structured Value
      ↓
OCR Evidence ID
      ↓
OCR Line
      ↓
Source Bounding Box
```

This allowed extraction results to become inspectable and auditable.

---

## Phase 4 — Confidence, Dates and Validation

Phase 4 introduced:

- field-level confidence
- evidence coverage
- date normalization
- expiry detection
- logical validation
- anomaly findings

The research began separating:

```text
OCR Confidence
```

from:

```text
Semantic Correctness
```

---

## Phase 5 — Human Review and Audit

Phase 5 added the human oversight layer.

Reviewers could:

```text
Approve
Correct
Reject
```

Machine extraction remained immutable.

Human corrections were stored separately and combined only when producing the final effective record.

---

## Phase 6 — API, PostgreSQL and Evaluation

Phase 6 moved the project toward a service architecture using:

- FastAPI
- PostgreSQL
- SQLAlchemy
- REST APIs
- structured persistence
- evaluation tooling

The evaluation corpus grew beyond the original requirement of 50 labelled documents.

---

## Phase 7 / 7C — Review Workflow Integrity

The Phase 7 series strengthened:

- review persistence
- authoritative final states
- review constraints
- database integrity
- duplicate review protection
- effective record semantics

The early implementation through Phase 7C is preserved separately under:

```text
phase_01_to_07c_src/
```

---

# Phase 8 — Professional UI / UX

Phase 8 transformed the backend-focused project into a professional browser-based application.

Major areas included:

- Dashboard
- Upload interface
- Document Library
- Review Queue
- Document Workspace
- original source display
- extracted-field presentation
- OCR evidence overlays
- review actions
- loading / error / empty states
- responsive design
- browser branding

Detailed research notes:

```text
notebooks/phase_08_ui_ux.md
```

---

# Phase 9 — Async Processing and Performance

Phase 9 moved expensive OCR and LLM work out of the HTTP request lifecycle.

Architecture:

```text
Browser
   ↓
FastAPI
   ↓
Durable PostgreSQL Job
   ↓
Background Worker
   ↓
OCR + LLM
   ↓
Persistence
```

The phase introduced:

- durable job queue
- worker claims
- job leases
- retry scheduling
- bounded attempts
- pending upload storage
- batch processing
- browser polling
- API responsiveness measurement
- worker performance analysis

Detailed notes:

```text
notebooks/phase_09_async_processing_and_performance.md
```

---

# Phase 10 — Advanced Document Intelligence

Phase 10 focused on making machine decisions safer and more explainable.

Research included:

- unsupported document handling
- SHA-256 duplicate detection
- concurrent duplicate protection
- image-quality assessment
- quality calibration
- confidence calibration
- finding normalization
- extraction resilience
- model configuration
- conservative automatic acceptance

The project adopted a release-critical safety invariant:

```text
False AUTO_ACCEPT = 0
```

Detailed notes:

```text
notebooks/phase_10_advanced_document_intelligence.md
```

---

# Phase 11 — Production Hardening

Phase 11 explored the engineering requirements around running the system safely.

Areas included:

- reviewer identity
- trusted proxy boundaries
- authorization
- production startup validation
- request IDs
- structured errors
- Content Security Policy
- CORS
- HSTS configuration
- upload rate limiting
- database pool management
- API concurrency
- Alembic migrations
- Docker architecture
- Nginx reverse proxy
- structured logging
- metrics
- worker health
- backup / restore
- graceful shutdown

Detailed notes:

```text
notebooks/phase_11_production_hardening.md
```

---

# Phase 12 — Final Verification

Phase 12 focused on regression testing and release-readiness verification.

The deterministic regression gate produced:

```text
PASSED  : 72
FAILED  : 0
BLOCKED : 0
MISSING : 0
```

Real-dependency tests were kept separate because they depend on:

- PaddleOCR runtime
- PostgreSQL
- Groq API
- network connectivity
- provider quota

The phase also included browser verification of:

- source image rendering
- evidence overlays
- review actions
- final-state persistence
- public browser workflow

Detailed notes:

```text
notebooks/phase_12_final_verification.md
```

---

# 🚀 Deployment Research

The complete VIGILOX workflow was exposed through **Cloudflare Quick Tunnel** for public HTTPS demonstration and end-to-end verification.

Architecture:

```text
Internet
   ↓
Cloudflare Quick Tunnel
   ↓
Local FastAPI
   ↓
PostgreSQL
   ↑
Background Worker
   ↓
PaddleOCR + Groq
```

The deployment exercise verified:

- public HTTPS access
- Dashboard
- Upload
- Documents
- Review Queue
- Document Workspace
- durable processing
- OCR
- structured extraction
- PostgreSQL persistence
- original source image rendering
- OCR evidence highlighting
- human review
- final-state persistence
- audit information

No temporary tunnel URL is stored in this repository.

Detailed deployment research:

```text
notebooks/deployment_cloudflare.md
```

---

# System Evolution

The architecture evolved significantly over the research period.

## Early Research Architecture

```text
Document
   ↓
OCR
   ↓
LLM
   ↓
Schema
   ↓
Result
```

---

## Final Evolved Architecture

```text
                     Document Upload
                           │
                           ▼
                  SHA-256 Fingerprint
                           │
                           ▼
                   Duplicate Detection
                           │
                           ▼
                     Durable Job
                           │
                           ▼
                       Worker
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
         PaddleOCR      Groq LLM     Image Quality
             │             │             │
             └─────────────┼─────────────┘
                           │
                           ▼
                  Evidence Validation
                           │
                           ▼
                 Date / Logic Validation
                           │
                           ▼
                  Normalized Findings
                           │
                           ▼
                   Machine Decision
                           │
             ┌─────────────┼──────────────┐
             │             │              │
             ▼             ▼              ▼
       AUTO_ACCEPT   HUMAN REVIEW    UNSUPPORTED
                           │
                           ▼
                 Approve / Correct /
                       Reject
                           │
                           ▼
                   Effective Record
                           │
                           ▼
                     Audit History
```

---

# Technology Stack

## OCR & Image Processing

- PaddleOCR
- PaddlePaddle
- OpenCV
- Pillow
- NumPy

## AI Extraction

- Groq API
- `openai/gpt-oss-20b`
- structured prompting
- schema-constrained extraction

## Backend

- Python 3.13
- FastAPI
- Pydantic
- SQLAlchemy
- Psycopg

## Database

- PostgreSQL 18
- Alembic

## Frontend

- HTML5
- CSS3
- Vanilla JavaScript

## Verification & Infrastructure Research

- Docker
- Docker Compose
- Nginx
- Cloudflare Tunnel

---

# Repository Structure

```text
VIGILOX-Document-Intelligence-Research/
│
├── code/
│   ├── backend/
│   ├── database/
│   └── frontend/
│
├── phase_01_to_07c_src/
│
├── evaluation/
│   ├── archive/
│   ├── ground_truth/
│   ├── images/
│   ├── reports/
│   └── results/
│
├── notebooks/
│   ├── phase_01_ocr.md
│   ├── phase_02_llm_extraction.md
│   ├── phase_03_evidence_validation.md
│   ├── phase_04_confidence_validation.md
│   ├── phase_05_human_review.md
│   ├── phase_06_api_database_evaluation.md
│   ├── phase_07_production_workflow.md
│   ├── phase_07c_review_integrity.md
│   ├── phase_08_ui_ux.md
│   ├── phase_09_async_processing_and_performance.md
│   ├── phase_10_advanced_document_intelligence.md
│   ├── phase_11_production_hardening.md
│   ├── phase_12_final_verification.md
│   └── deployment_cloudflare.md
│
├── scripts/
│   ├── development/
│   ├── evaluation/
│   ├── phase_07c/
│   └── verification/
│
├── tests/
│
├── migrations/
│
├── .env.example
├── .gitignore
├── alembic.ini
├── requirements.txt
├── LICENSE
└── README.md
```

---

# Code Organization

This repository intentionally contains two implementation snapshots.

## `phase_01_to_07c_src/`

Contains the earlier research implementation developed through Phase 7C.

This preserves the historical structure used while investigating:

- OCR
- extraction
- confidence
- evidence
- human review
- database integration

It is kept for research comparison and development-history preservation.

---

## `code/`

Contains the evolved implementation snapshot produced after the later engineering phases.

```text
code/
├── backend/
├── database/
└── frontend/
```

This snapshot represents the architecture after the project evolved into:

- professional UI
- asynchronous processing
- advanced intelligence
- production hardening
- release verification

The purpose is comparison and research reproducibility rather than maintaining two independent production applications.

---

# Evaluation

The `evaluation/` directory contains the research data and outputs used to measure extraction behavior.

```text
evaluation/
├── images/
├── ground_truth/
├── results/
├── reports/
└── archive/
```

### `images/`

Synthetic or authorized labelled document images used for evaluation.

### `ground_truth/`

Expected structured field values used as the benchmark reference.

### `results/`

Generated extraction outputs from evaluation runs.

### `reports/`

Evaluation summaries and benchmark metrics.

### `archive/`

Historical evaluation artifacts retained for comparison.

---

# Evaluation Methodology

The evaluation framework examines metrics including:

- document-type accuracy
- exact field accuracy
- normalized field accuracy
- known-field normalized accuracy
- critical-field accuracy
- fully correct documents
- machine-decision distribution
- false automatic acceptance

A major safety metric is:

```text
False AUTO_ACCEPT
```

because an incorrect automatically accepted document bypasses human review.

---

# Historical Benchmark

The historical evaluation corpus contained:

```text
63 labelled documents
```

Historical results included:

```text
Document Type Accuracy           100%

Exact Field Accuracy             95.92%

Normalized Field Accuracy        98.64%

Known-Field Normalized Accuracy  98.49%

Critical-Field Accuracy          99.05% (208 / 210)

Fully Correct Documents          93.65%

False AUTO_ACCEPT                0
```

These values represent the historical benchmark baseline documented during development.

---

# Critical-Field Metric Correction

An earlier evaluation definition omitted a production-critical `issuer` field for relevant document types.

The earlier metric was:

```text
99.40%
167 / 168
```

After aligning evaluation with the production critical-field definition:

```text
99.05%
208 / 210
```

This was a **metric-definition correction**, not a model regression.

---

# Confidence Research

One important research finding was:

```text
High OCR Confidence
        ≠
High Semantic Correctness Probability
```

OCR may recognize a value correctly while structured extraction assigns it to the wrong field.

VIGILOX therefore interprets field confidence as:

> OCR and evidence support strength

rather than:

> probability that the semantic field is correct

The system intentionally avoids deriving an unsupported document-level confidence percentage.

---

# Image Quality Research

Deterministic quality signals evaluated during the research included:

```text
IMAGE_BLURRY
IMAGE_UNREADABLE
IMAGE_TOO_DARK
IMAGE_OVEREXPOSED
ROTATION_CONCERN
IMAGE_TOO_SMALL
```

Quality measurements were tested against clean documents and controlled image degradations.

An experimental low-contrast finding was not retained because the tested metric was not sufficiently reliable on the available corpus.

This reflects a core research principle:

> A measurable value should not automatically become a product signal.

---

# Duplicate Detection Research

Duplicate detection uses:

```text
Original Uploaded Bytes
        ↓
SHA-256
```

rather than a preprocessed image.

This provides stable source identity.

The system distinguishes cases such as:

```text
DUPLICATE_DOCUMENT
DUPLICATE_IN_PROGRESS
```

and uses PostgreSQL-level protection against concurrent active duplicate jobs.

---

# Human Review Research

The project treats human review as part of the intelligence architecture.

The reviewer can inspect:

- original source document
- extracted fields
- OCR evidence
- evidence bounding boxes
- confidence
- image quality
- validation findings
- review history

Available decisions include:

```text
Approve
Correct
Reject
```

Machine extraction remains immutable.

Corrections become overlays used when constructing the effective record.

---

# Final Record Semantics

| State | Final | Usable | Effective Source |
|---|---:|---:|---|
| `AUTO_ACCEPTED` | Yes | Yes | Machine |
| `PENDING_REVIEW` | No | No | Withheld |
| `APPROVED` | Yes | Yes | Machine |
| `CORRECTED` | Yes | Yes | Human overlay |
| `REJECTED` | Yes | No | None |
| `UNSUPPORTED` | Yes | No | None |

This distinction is important because:

```text
Processing Completed
```

does not necessarily mean:

```text
Document Usable
```

---

# Scripts

The `scripts/` directory separates executable research utilities by purpose.

```text
scripts/
├── development/
├── evaluation/
├── phase_07c/
└── verification/
```

## Development

Contains experimental and benchmarking utilities such as:

- preprocessing studies
- extraction latency studies
- calibration experiments

## Evaluation

Contains scripts used to:

- generate synthetic documents
- run extraction evaluations
- calculate metrics
- create evaluation reports

## Phase 7C

Preserves migration and integrity utilities associated with the earlier research architecture.

## Verification

Contains regression and release-verification utilities.

---

# Testing

The repository includes tests covering areas such as:

- OCR
- extraction
- evidence validation
- API behavior
- PostgreSQL persistence
- human review
- storage
- async jobs
- concurrency
- duplicate detection
- quality intelligence
- security
- migrations
- deployment configuration
- browser-related contracts

The deterministic regression gate can be run with:

```powershell
python scripts/verification/run_phase7c7g_regressions.py --exclude-real
```

Latest verified deterministic result:

```text
PASSED  : 72
FAILED  : 0
BLOCKED : 0
MISSING : 0
```

The `--exclude-real` option intentionally separates deterministic verification from tests that require external dependencies.

---

# Real Dependency Tests

Tests requiring real runtime dependencies can be executed separately when the required environment and provider quota are available.

```powershell
python scripts/verification/run_phase7c7g_regressions.py --only-real
```

These may depend on:

- PaddleOCR
- PostgreSQL
- Groq API
- provider quota
- network access

Large provider-backed evaluations should not be repeated unnecessarily.

---

# Local Setup

## Prerequisites

Install:

- Python 3.13
- PostgreSQL
- Git

---

## 1. Clone the Repository

```bash
git clone <REPOSITORY_URL>
cd VIGILOX-Document-Intelligence-Research
```

Replace `<REPOSITORY_URL>` with the GitHub URL of this research repository.

---

## 2. Create a Virtual Environment

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 4. Configure Environment

Copy:

```text
.env.example
```

to:

```text
.env
```

On Windows:

```powershell
Copy-Item .env.example .env
```

Configure:

```env
GROQ_API_KEY=your_groq_api_key_here

DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/vigilox_document_intelligence

VIGILOX_GROQ_MODEL=openai/gpt-oss-20b
```

Never commit the real `.env` file.

---

# Database Migrations

Apply migrations:

```powershell
python -m alembic upgrade head
```

Check migration state:

```powershell
python -m alembic current
```

Check schema drift:

```powershell
python -m alembic check
```

Database credentials are read through `DATABASE_URL`.

They are not stored inside `alembic.ini`.

---

# Running the Evolved Code Snapshot

Because the final implementation is stored under:

```text
code/
```

its import path may need to include that directory when running the snapshot directly from the research repository.

The repository is primarily intended for:

- research
- code inspection
- evaluation
- phase comparison
- testing
- documentation

rather than as the canonical deployment repository.

The main production repository should remain the authoritative source for current operational deployment.

---

# Research Notes

The `notebooks/` directory contains the written engineering history of the project.

These notes document:

- objectives
- problems
- architectural decisions
- implementation approaches
- experiments
- measurements
- failures
- fixes
- test results
- lessons learned
- final outcomes

The later research sequence is:

```text
phase_08_ui_ux.md

phase_09_async_processing_and_performance.md

phase_10_advanced_document_intelligence.md

phase_11_production_hardening.md

phase_12_final_verification.md

deployment_cloudflare.md
```

These are intended to explain **why** architectural decisions were made, not only what the final code looks like.

---

# Design Principles

## Evidence Before Trust

An extracted value should be supported by inspectable source evidence whenever possible.

## Human Oversight

Uncertain outcomes should be routed to human review instead of being hidden behind artificial confidence.

## Immutable Machine Output

Human corrections should not erase the machine's historical extraction.

## Durable Processing

Browser sessions should not control the lifetime of long-running OCR and LLM jobs.

## Deterministic Logic Where Possible

Use deterministic methods for problems such as:

- hashing
- schema validation
- dates
- database constraints
- image measurements

rather than asking an LLM to solve everything.

## Conservative Automation

Automation should reduce workload without creating unsafe automatic acceptance.

## No Invented Intelligence

Do not claim unsupported:

- fraud probabilities
- tamper probabilities
- generic AI risk scores
- document-level confidence percentages

## Reproducible Evaluation

Metrics should remain tied to:

- labelled data
- documented definitions
- versioned evaluation artifacts
- reproducible scripts

---

# Research Safety

Do not commit:

```text
.env
API keys
database passwords
real private identity documents
runtime storage
private certificates
```

Use synthetic or properly authorized documents for research and evaluation.

The repository intentionally separates:

```text
evaluation/
```

for reproducible research artifacts from local runtime or sensitive document storage.

---

# 💻 Developer

## ALISHA SAJJAD

**AI Engineer · Python Developer · Generative AI & Agentic Systems Enthusiast**

Developed and researched the VIGILOX Document Intelligence system across OCR, structured AI extraction, evidence validation, confidence analysis, human review, durable processing, evaluation, security, and production-oriented engineering.

GitHub:

[github.com/alishasajjad](https://github.com/alishasajjad)

---

# License

VIGILOX Document Intelligence Research is licensed under the [MIT License](LICENSE).

Copyright © 2026 Alisha Sajjad.

---

<div align="center">

## 🛡️ VIGILOX

**Document Intelligence Research**

OCR · AI Extraction · Evidence · Validation · Human Oversight

<br>

**Developed by ALISHA SAJJAD**

<br>

[⬆ Back to Top](#️-vigilox-document-intelligence-research)

</div>