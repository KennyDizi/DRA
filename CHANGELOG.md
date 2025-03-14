## [2025-03-14] [PR#20](https://github.com/KennyDizi/DRA/pull/20)

### Added
- Added `DataIngestionAgent` class for data ingestion functionality with support for customizable `knowledge_base_collection`.
- Implemented `Logger` class for advanced logging with console and file logging, including rotation, retention, and compression.
- Created `run_data_ingestion.sh` shell script to execute `DataIngestionAgent` with specified collection name.
- Defined `KnowledgeBaseCollection` enum in `utils.py` with `GENERIC` collection type.

## [2025-03-13] [PR#8](https://github.com/KennyDizi/DRA/pull/8)

### Added
- Added `STRATEGIC_LLM` configuration to `.env.example`.
- Added `RETRIEVER` configuration with provider options.

### Updated
- Updated `TAVILY_API_KEY` and `SERPER_API_KEY` with documentation links.
- Enhanced environment variable documentation for clarity.

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