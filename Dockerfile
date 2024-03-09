FROM python:3.11.8-slim-bullseye

RUN apt-get update && \
    apt-get upgrade --yes

RUN useradd --create-home pyuser
USER pyuser
WORKDIR /home/pyuser/fast_app

ENV VIRTUALENV=/home/pyuser/fast_app/venv
RUN python3 -m venv $VIRTUALENV
ENV PATH="$VIRTUALENV/bin:$PATH"

COPY --chown=pyuser pyproject.toml requirements.txt ./

RUN python -m pip install --upgrade pip setuptools && \
    python -m pip install --no-cache-dir -c requirements.txt ".[dev]"

COPY --chown=pyuser fast_app/ fast_app/
COPY --chown=pyuser tests/ tests/

RUN python -m pip install . -c requirements.txt && \
    python -m pytest tests && \
    python -m pylint fast_app/ --disable=C0114,C0116,R1705 --max-line-length=120 && \
    python -m flake8 fast_app/ && \
    python -m isort fast_app/ --check && \
    python -m black fast_app/ --check --quiet && \
    python -m bandit -r fast_app/ --quiet