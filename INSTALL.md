# Install guide

## Prerequisites

```bash
brew install pyenv
```

```bash
brew install pyenv-virtualenv
```

## Create a virtual environment

```bash
pyenv virtualenv DRA-Python3.12.7

pyenv activate DRA-Python3.12.7
```

## Install the dependencies

```bash
./setup.sh
```

## Install additional libs for MacOS

```bash
./setup-macos.sh
```

Read more details at [here](https://python.langchain.com/docs/integrations/providers/unstructured)
