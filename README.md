# 🌾 🥳 🌋 🏰 🌅 🌕 Deep Research Advanced 🌖 🌔 🌈 🏆 👑

## Setup

You can follow the original use guide [here](https://github.com/assafelovic/gpt-researcher?tab=readme-ov-file#installation)

## Run with web mode

This mode only gets the data source from the Internet with the search engine and crawler.

```bash
# Basic web mode
./run.sh

# With explicit argument and word limit
./run.sh --report-source web --total-words 2000
```

## Run with local mode

This mode will get data from your files only as the data source.

You have to set `DOC_PATH` to `./my-docs` in your `.env` file.
Then put your documents to this folder.

```bash
# Basic local mode
./run.sh --report-source local

# With word limit
./run.sh --report-source local --total-words 1500
```

## Run with hybrid mode

This mode is a combination of `web` and `local` modes. It can get data from the Internet as well as your local files.

You must set `DOC_PATH` to `./my-docs` in your `.env` file.
Then, put your documents in this folder.

If your documents are stored online, you will put all your links to `DOCUMENT_URLS`, separate them by `,`. For example: `DOCUMENT_URLS=https://yourdocument1.docx,https://yourdocument2.pdf`

Important note: If you enable `DOCUMENT_URLS`, the `DOC_PATH` will not be used.

```bash
# Basic hybrid mode
./run.sh --report-source hybrid

# With hybrid mode and word limit
./run.sh --report-source hybrid --total-words 3000
```

## Environment variable setup

### TOTAL_WORDS

Optional. Specifies the total number of words for the report. Can be set either:

1. Via command line argument (takes precedence):
   `--total-words <number>`
2. In .env file:
   `TOTAL_WORDS=2000`

### RETRIEVERS

You can set it as a single value, eg: `RETRIEVERS="tavily"` or multiple value `RETRIEVERS="tavily,arxiv"` separate them by `,`.

### QUERY DOMAINS

You can specify the query domains via argument `--query-domains`, for example: `./run.sh --report-source web --query-domains "foo.com,bar.com"`

## Prompt

You can put your requirements into the file `prompts/prompts.txt` or if you have multiple prompts that located in multiple files, you can specify it via argument `--prompts your_file.txt`, eg: `./run.sh --report-source web --prompts my_new_requirements.txt`

## Output

The generated output will be saved in markdown file in folder `reports` with timestamped format, eg: `2025-03-20_07-57AM.md`
