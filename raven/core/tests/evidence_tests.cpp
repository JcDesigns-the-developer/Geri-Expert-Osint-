#include "raven/evidence.hpp"

#include <cassert>

int main() {
    raven::EvidenceEngine engine;
    const std::vector<raven::Observation> observations{
        {"o1", "terrain", "flat terrain with corn fields", 0.9},
        {"o2", "roads", "rural two lane road", 0.8}
    };
    const std::vector<raven::Candidate> candidates{
        {"midwest", "Candidate Midwest", {"flat terrain", "corn fields", "rural two lane"}, {}},
        {"mountain", "Candidate Mountain", {"mountain terrain"}, {"flat terrain"}}
    };
    const auto ranked = engine.rank(observations, candidates);
    assert(ranked.size() == 2);
    assert(ranked.front().candidate_id == "midwest");
    assert(ranked.front().fit_score > ranked.back().fit_score);
    return 0;
}
