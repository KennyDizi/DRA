# Deep Reseach Usage Guide

## Run with web mode

This mode only gets the data source from the Internet with the search engine and crawler.

```bash
./run.sh
```

or

```bash
./run.sh --report-source web
```

## Run with local mode

This mode will get data from your files only as the data source.

You have to set `DOC_PATH` to `./my-docs` in your `.env` file.
Then put your documents to this folder.

Run command:

```bash
./run.sh --report-source local
```

## Run with hybrid mode

This mode is a combination of `web` and `local` modes. It can get data from the Internet as well as your local files.

You have to set `DOC_PATH` to `./my-docs` in your `.env` file.
Then put your documents to this folder.

Run command:

```bash
./run.sh --report-source hybrid
```
