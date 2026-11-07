# RAVEN — Geographic Intelligence Workbench

RAVEN is a local-first, evidence-led visual geolocation research project. It is being developed alongside this repository's existing llama.cpp fork; it does not replace or modify llama.cpp.

## Scope and design goals

- Analyze user-provided imagery and geographic observations for public-place research.
- Keep observations, hypotheses, and verified facts separate.
- Rank candidate regions using explainable evidence and explicit contradictions.
- Support reproducible investigations with source provenance and audit logs.
- Run locally on Windows 11; optional internet research is opt-in.
- Use llama.cpp only as an optional local language interface. Geographic intelligence must work without a language model.

RAVEN is not a person-tracking system. It must not be used to locate private residences, infer a person's whereabouts, or monitor an individual's movements. It is intended for public landmarks, public infrastructure, user-owned imagery, and authorized research.

## Architecture

- `core/`: C++20 evidence and hypothesis engine.
- `vision/`: image preprocessing and feature extraction interfaces.
- `training/`: custom model training, dataset manifests, and evaluation.
- `backend/`: local API and case storage.
- `frontend/`: local browser UI.
- `integrations/llama.cpp/`: optional adapter to the parent repository's local inference runtime.

## Current milestone

The bootstrap milestone establishes the C++ evidence engine contract, a local Python API, a browser UI, and a dataset/evaluation contract. It is not yet a trained geolocation model and must not be represented as federal-certified or operationally validated.

## Development

See [BUILD.md](BUILD.md) for Windows 11 setup and [docs/ROADMAP.md](docs/ROADMAP.md) for milestones.
