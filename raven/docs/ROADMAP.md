# RAVEN roadmap

## M0 — Foundation (current)
- Separate RAVEN subproject in the existing llama.cpp fork.
- C++ evidence/hypothesis core with explainable weighted scoring.
- Loopback-only local API and browser workbench.
- Explicit evidence provenance and uncertainty labels.
- Training dataset manifest and evaluation protocol.

## M1 — Visual feature pipeline
- Image decoding, EXIF extraction, orientation normalization, and privacy-safe metadata handling.
- Classical CV features: line segments, vanishing points, road geometry, vegetation/land-cover descriptors, and scene composition.
- Feature outputs must include method/version and confidence; no unsupported exact-location claims.

## M2 — Custom models (A + B)
- Train small regional/terrain/road-pattern classifiers from scratch.
- Fine-tune permitted pretrained vision backbones for generic object/sign/landmark detection.
- Keep training/validation/test geography disjoint to prevent location leakage.
- Publish per-region precision/recall, top-k accuracy, calibration, and failure analysis.

## M3 — Geographic retrieval
- Build a licensed, provenance-tracked reference corpus from public geographic datasets and permitted imagery.
- Retrieve candidates using multiple independent signals, not a single embedding similarity.
- Keep source dates, license, spatial resolution, and coverage attached to each reference.

## M4 — Local inference and operator workflow
- Optional llama.cpp adapter for summarizing evidence and generating testable hypotheses.
- The model cannot invent evidence or override deterministic results.
- Case export, audit log, reproducible reports, and model/dataset version pinning.

## M5 — Validation and hardening
- Threat model, dependency review, offline mode, access controls, signed builds, reproducible packaging, and independent evaluation.
- Federal-grade claims require formal security, privacy, records-management, accessibility, and procurement review. RAVEN is not certified by this project.
