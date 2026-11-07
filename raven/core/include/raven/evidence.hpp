#pragma once

#include <string>
#include <vector>

namespace raven {

struct Observation {
    std::string id;
    std::string category;
    std::string description;
    double reliability; // 0.0 - 1.0; operator-assessed evidence quality
};

struct Candidate {
    std::string id;
    std::string label;
    std::vector<std::string> supporting_tags;
    std::vector<std::string> contradicting_tags;
};

struct EvidenceMatch {
    std::string observation_id;
    std::string observation;
    std::string matched_tag;
    double contribution;
    bool contradiction;
};

struct CandidateAssessment {
    std::string candidate_id;
    std::string label;
    double fit_score; // heuristic fit, NOT a probability
    std::vector<EvidenceMatch> evidence;
    std::string interpretation;
};

class EvidenceEngine {
public:
    // Deterministic baseline. Scores are relative evidence-fit indices, never probabilities.
    [[nodiscard]] std::vector<CandidateAssessment> rank(
        const std::vector<Observation>& observations,
        const std::vector<Candidate>& candidates) const;
};

} // namespace raven
