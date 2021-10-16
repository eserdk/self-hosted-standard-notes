FROM python:3.10 as builder

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PATH="/venv/bin:${PATH}" \
    VIRTUAL_ENV=/venv

RUN pip install -U pip poetry && python -m venv /venv

COPY poetry.lock pyproject.toml ./
RUN poetry install -v --no-dev

FROM python:3.10-slim as final

ENV PATH="/venv/bin:${PATH}" VIRTUAL_ENV=/venv

RUN set -ex \
    && apt-get update -yqq \
    && apt-get install -yqq cron \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

WORKDIR /app

COPY --from=builder /venv /venv
COPY entrypoint.sh /entrypoint.sh
COPY update.py ./

RUN touch /var/log/cron.log

ENTRYPOINT ["/entrypoint.sh"]
