#include "raven/evidence.hpp"

#include <algorithm>
#include <cctype>
#include <cmath>
#include <unordered_set>

namespace raven {
namespace {
std::string normalize(std::string value) {
    std::transform(value.begin(), value.end(), value.begin(),
        [](unsigned char c) { return static_cast<char>(std::tolower(c)); });
    return value;
}
bool contains_phrase(const std::string& haystack, const std::string& needle) {
    if (needle.empty()) return false;
    return normalize(haystack).find(normalize(needle)) != std::string::npos;
}
}

std::vector<CandidateAssessment> EvidenceEngine::rank(
    const std::vector<Observation>& observations,
    const std::vector<Candidate>& candidates) const {

    std::vector<CandidateAssessment> results;
    results.reserve(candidates.size());

    for (const auto& candidate : candidates) {
        double positive = 0.0;
        double negative = 0.0;
        double possible = 0.0;
        std::vector<EvidenceMatch> matches;

        for (const auto& observation : observations) {
            const double reliability = std::clamp(observation.reliability, 0.0, 1.0);
            if (reliability <= 0.0 || observation.description.empty()) continue;
            possible += reliability;

            bool supported = false;
            for (const auto& tag : candidate.supporting_tags) {
                if (contains_phrase(observation.description, tag)) {
                    positive += reliability;
                    matches.push_back({observation.id, observation.description, tag,
                                       reliability, false});
                    supported = true;
                    break;
                }
            }
            for (const auto& tag : candidate.contradicting_tags) {
                if (contains_phrase(observation.description, tag)) {
                    negative += reliability;
                    matches.push_back({observation.id, observation.description, tag,
                                       reliability, true});
                    break;
                }
            }
            (void)supported;
        }

        // Contradictions carry a stronger penalty than a simple absence of a match.
        const double raw = possible > 0.0
            ? 100.0 * std::max(0.0, positive - 1.5 * negative) / possible
            : 0.0;

        std::string interpretation = "Insufficient evidence; do not infer a location.";
        if (possible > 0.0 && positive > 0.0 && negative == 0.0)
            interpretation = "Some supporting evidence; independently verify with distinct sources.";
        else if (negative > 0.0)
            interpretation = "Contradictory evidence found; candidate requires review or elimination.";

        results.push_back({candidate.id, candidate.label,
                           std::round(raw * 10.0) / 10.0,
                           std::move(matches), std::move(interpretation)});
    }

    std::stable_sort(results.begin(), results.end(),
        [](const CandidateAssessment& a, const CandidateAssessment& b) {
            return a.fit_score > b.fit_score;
        });
    return results;
}
} // namespace raven
