## [2025-05-28] [PR#99](https://github.com/KennyDizi/DRA/pull/99)

### Dependencies
- Updated:
  * `openai` from `1.81.0` to `1.82.0`.
  * `anthropic` from `0.51.0` to `0.52.0`.
  * `langchain-core` from `0.3.60` to `0.3.62`.
  * `langchain-openai` from `0.3.17` to `0.3.18`.
  * `langchain-anthropic` from `0.3.13` to `0.3.14`.
  * `tavily-python` from `0.7.2` to `0.7.3`.
  * `ruff` from `0.11.10` to `0.11.11`.

### Changed
- Refactored `.env` files to use updated LLM model names and ensure consistency with latest dependency versions.

## [2025-05-03] [PR#95](https://github.com/KennyDizi/DRA/pull/95)

### Dependencies
- Updated:
  * `openai` from `1.76.2` to `1.77.0`.
  * `langchain-core` from `0.3.56` to `0.3.58`.
  * `langchain` from `0.3.24` to `0.3.25`.
  * `langchain-openai` from `0.3.15` to `0.3.16`.
- Synchronized dependency versions in `pyproject.toml` and `requirements.txt`.

## [2025-04-23] [PR#90](https://github.com/KennyDizi/DRA/pull/90)

### Dependencies
- Updated:
  * `anthropic` from `0.49.0` to `0.50.0`.
  * `unstructured-client` from `0.33.0` to `0.34.0`.
  * `langchain-core` from `0.3.54` to `0.3.55`.
  * `langchain` from `0.3.23` to `0.3.24`.
  * `langchain-community` from `0.3.21` to `0.3.22`.
  * `firecrawl-py` from `2.1.2` to `2.2.0`.
- Synchronized dependency versions in `pyproject.toml` and `requirements.txt`.

## [2025-03-27] [PR#73](https://github.com/KennyDizi/DRA/pull/73)

### Updated
- Updated `.env.example` with a link to get `UNSTRUCTURED_API_KEY` from the unstructured.io platform.

## [2025-03-23] [PR#69](https://github.com/KennyDizi/DRA/pull/69)

### Changed
- Updated `setup-macos.sh` to install `libmagic` as a separate dependency while retaining existing dependencies.

### Added
- Added `unstructured-client` to core libraries for enhanced document processing capabilities.

## [2025-03-23] [PR#65](https://github.com/KennyDizi/DRA/pull/65)

### Added
- Added `setup-macos.sh` script for macOS-specific dependency installation.
- Added detailed prerequisites and installation steps to `INSTALL.md`, including `pyenv` and `pyenv-virtualenv` setup.

### Changed
- Updated `setup.sh` to use `unstructured[all-docs]` for broader document support.
- Replaced direct `pip install` commands with `setup.sh` and `setup-macos.sh` scripts in `INSTALL.md`.

## [2025-03-23] [PR#63](https://github.com/KennyDizi/DRA/pull/63)

### Added
- Added `lint.sh` script to automate linting for Python files using `ruff`.

### Changed
- Fixed string formatting in `data_ingestion_agent.py` by removing unnecessary `f-string`.

## [2025-03-22] [PR#61](https://github.com/KennyDizi/DRA/pull/61)

### Changed
- Updated `FAST_LLM` configuration from `anthropic:claude-3-7-sonnet-20250219` to `deepseek:deepseek-chat`.
- Updated `SMART_LLM` configuration from `openai:o3-mini-2025-01-31` to `anthropic:claude-3-7-sonnet-20250219`.

## [2025-03-22] [PR#59](https://github.com/KennyDizi/DRA/pull/59)

### Added
- Added `--query-domains` argument to specify query domains for the report, accepting a comma-separated list of domains.
- Updated `README.md` to document the new `--query-domains` argument with usage examples.

### Changed
- Modified `GPTResearcher` initialization to include `query_domains` parameter for domain-specific queries.

## [2025-03-21] [PR#57](https://github.com/KennyDizi/DRA/pull/57)

### Changed
- Consolidated file processing to use `UnstructuredLoader` exclusively, removing `DoclingLoader` and related dependencies.

### Updated
- Updated dependencies to remove `docling` and specify `numpy` version.

## [2025-03-19] [PR#43](https://github.com/KennyDizi/DRA/pull/43)

### Added
- Added `--prompts` argument to dynamically load prompt files, defaulting to `prompts.txt` if not specified.
- Improved error messages for prompt file operations.

### Changed
- Updated file path handling for prompts to use `os.path.join`.
- Refactored argument parsing for better readability.

## [2025-03-17] [PR#31](https://github.com/KennyDizi/DRA/pull/31)

### Added
- Added support for multiple retrievers via `RETRIEVERS` environment variable.
- Updated `.env.example` to include `RETRIEVERS` with options like `tavily` and `arxiv`.
- Added documentation in `USAGE.md` for setting up `RETRIEVERS`.

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