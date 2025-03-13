## [2025-03-13] [PR#6](https://github.com/KennyDizi/DRA/pull/6)

### Changed
- Increased `DEEP_RESEARCH_DEPTH` from `2` to `4`.
- Decreased `DEEP_RESEARCH_CONCURRENCY` from `4` to `2`.

### Added
- Added `EMBEDDING_PROVIDER` with value `"openai"`.

## [2025-03-13] [PR#1](https://github.com/KennyDizi/DRA/pull/1)

### Added
- Added `.env.example` with environment variables for API keys and research parameters.
- Created `deep_research_agent.py` to perform deep research using `GPTResearcher`.
- Added `run.sh` script to load environment variables and execute the research agent.
- Set Python version to `3.13.2` in `.python-version`.