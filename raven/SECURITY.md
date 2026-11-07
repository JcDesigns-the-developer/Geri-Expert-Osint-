# RAVEN security and responsible-use baseline

RAVEN is a local research workbench, not a government-certified product. The phrase "federal-level" is treated as an engineering aspiration for rigor, traceability, reproducibility, and security—not as a claim of authorization, accreditation, or certification.

## Data boundaries
- Bind the development server to 127.0.0.1 by default.
- Do not expose the API to a LAN or public interface without authentication, TLS, access review, and a documented threat model.
- Keep uploaded imagery, case databases, training data, and model weights out of Git.
- Do not send image bytes or case data to cloud AI services.
- Optional public-data research must be visibly opt-in and record the provider, query, retrieval time, and applicable license.

## Use boundaries
- Analyze public landmarks, public infrastructure, and imagery the operator owns or is authorized to examine.
- Do not identify or locate a private person's residence, track an individual's movements, or create dossiers about private people.
- Avoid facial recognition, identity matching, and person re-identification features.
- A location hypothesis must not be presented as fact without independent corroboration.

## Evidence integrity
- Every observation should record who/what supplied it, when it was added, and whether it is direct observation or inference.
- Preserve original observations; corrections should be appended with provenance.
- Keep model version, dataset version, source license, and analysis parameters with each report.
- Scores are heuristic fit measures unless and until statistically calibrated on a geographically disjoint benchmark.

## Operational limitations
This repository does not provide FISMA authorization, FedRAMP authorization, NIST control assessment, CJIS compliance, or any other government certification. Those require a separate organizational security program, formal assessment, legal review, and independent validation.
