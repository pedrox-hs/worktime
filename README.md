# WorkTime

Use exported CSV from [Activity Timer](https://trello.com/power-ups/5ec6c1c179ade984555a12eb/activity-timer) to show time spend and value to receive by month.

## Requirements

- Python >= 3.10

## Setup

Copy `.env.example` to `.env` and replace values with your our information:

```bash
cp .env{,.example}
```

Initialize virtual environment:

```bash
python -m venv .venv
```

Activate virtual environment:

```bash
source .venv/bin/activate
```

Install Poetry:

```bash
pip install poetry
```

Install dependencies:

```bash
poetry install
```

## Usage

Execute `./worktime.py --help` to display help:

```bash
usage: worktime.py [-h] [--hour-price HOUR_PRICE] [--member MEMBER] paths [paths ...]

positional arguments:
  paths                 path to the CSV file

options:
  -h, --help            show this help message and exit
  --hour-price HOUR_PRICE
                        hour price in BRL (R$)
  --member MEMBER       member name
```