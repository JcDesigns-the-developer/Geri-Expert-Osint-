# Optional llama.cpp adapter

The parent repository provides llama.cpp. RAVEN may later use a locally hosted GGUF language model to summarize structured evidence or propose follow-up questions.

Rules:
- This adapter is optional; core ranking and image feature extraction must work without it.
- A text LLM is not the geolocation model and must never fabricate visual observations.
- The LLM receives structured, provenance-bearing evidence produced by RAVEN.
- The deterministic engine remains authoritative for scores, contradictions, and candidate ordering.
- No network service or external API is required for local inference.

Integration will be implemented after the visual pipeline and evidence schema stabilize.
