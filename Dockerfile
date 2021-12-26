ARG PYTHON_VERSION=3.10-slim-buster

# define an alias for the specfic python version used in this file.
FROM python:${PYTHON_VERSION} as python

# Force stin, stdout, and stderr to be totally unbuffered
ENV PYTHONUNBUFFERED=1 \
	POETRY_VERSION=1.1.12

RUN true \
	# python setup
	&& pip install --no-cache-dir --upgrade pip wheel \
	# python poetry
	&& pip install "poetry==$POETRY_VERSION" && poetry config virtualenvs.create false

# project skeleton
WORKDIR /app

# COPY pyproject.toml and poetry.lock and RUN poetry install BEFORE adding the rest the code,
# this will cause Docker's caching mechanism to prevent re-installing (all)
# dependencies when there is only a change in the code.
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-root

ENTRYPOINT ["bash"]
