# Roki's Corner

**Roki's Corner** is a web application built with Django that enables users to
create, customize, and manage their portfolio pages. Users can easily generate
and download their portfolios as CVs in PDF format, providing a convenient way
to showcase their professional experience and skills.

## Table of Contents

- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Project Setup](#project-setup)
- [Enable Sentry](#enable-sentry)
- [Enable Google Analytics](#enable-google-analytics)
- [Test Data](#test-data)
    - [Create Superuser](#create-superuser)
- [Run Tests](#run-tests)
- [Setup pre-commit hooks](#setup-pre-commit-hooks)
- [Linting and Formatting](#linting-and-formatting)
- [Deployment](#deployment)
    - [Development Environment](#development-environment)
    - [Production Environment](#production-environment)

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Project Setup

1. Clone the repository:
    ```bash
    git clone git@github.com:roknicmilos/rokis-corner.git
    ```

2. Create file with environment variables:
    ```bash
    cp example.env .env
    ```
   There is no need to change anything in the `.env` file for the **development
   environment**. However, you can change the values of the variables if you
   want to run the project in a different environment.
   <br/><br/>

3. To start the project in a **local environment**, run the following command:
    ```bash
    docker compose up -d
    ```
   To start the project in a **dev environment**, run the following
   command:
    ```bash
    docker compose -f docker-compose.dev.yaml up -d
    ```
   To start the project in a **production environment**, run the following
   command:
    ```bash
    docker compose -f docker-compose.prod.yaml up -d
    ```

You can now access the project at http://localhost:8000/. Django Admin is
available at http://localhost:8000/admin/.

Check `docker-compose`files for more information about the Docker configuration:

- [docker-compose.yaml](docker-compose.yaml)
- [docker-compose.dev.yaml](docker-compose.dev.yaml)
- [docker-compose.prod.yaml](docker-compose.prod.yaml)

## Enable Sentry

To enable Sentry error tracking, set the `SENTRY_DSN` and `SENTRY_ENV` variables
in the `.env` file.

Check
[Client Keys (DSN)](https://rokis-corner.sentry.io/settings/projects/rokis-corner/keys/)
in the Sentry project settings to get the DSN.

Use one of the following values for the `SENTRY_ENV` variable: `local`, `dev` or
`prod`.

To check the issues for this project on Sentry, click
[here](https://rokis-corner.sentry.io/issues/?project=4508003751821312&referrer=sidebar&statsPeriod=14d).

## Enable Google Analytics

To enable Google Analytics, set the `GOOGLE_ANALYTICS_TRACKING_ID` variable in
the `.env` file.

To get the tracking ID, visit:
[Roki's Corner DEV data stream](https://analytics.google.com/analytics/web/#/a152537310p460818596/admin/streams/table/9749560985)
or
[Roki's Corner PROD data stream](https://analytics.google.com/analytics/web/#/a152537310p215621886/admin/streams/table/9749678510)
at [Google Analytics](https://analytics.google.com/).

## Test Data

The project includes test data in the form of Django fixtures. The fixtures are
located in the `fixtures` directories in each Django app. If you started Docker
containers with the `docker compose up -d` command, the fixtures will be loaded
automatically.

If you want to **load the fixtures manually**, you can do so with the following
command:

```bash
docker compose run --rm web sh -c "python manage.py loaddata --all"
```

You can now check out Eric's Cartman portfolio page at
http://localhost:8000/eric-cartman/

### Create Superuser

To create a superuser with credentials defined in the `.env` file, run the
following command:

```bash
docker compose run --rm web sh -c "python manage.py create_superuser"
```

You can now access the Django Admin at http://localhost:8000/admin/ and log in
with the superuser credentials defined in the `.env` file.

## Run Tests

Run the tests with the following command:

```bash
docker compose run --rm web sh -c "pytest"
```

Check `tox.ini` file for more information about the test configuration.

## Setup pre-commit hooks

This project uses [pre-commit](https://pre-commit.com/) to manage and run
pre-commit hooks. To install the pre-commit hooks, you should first install
[Poetry](https://python-poetry.org/) and then run the following command to
install the pre-commit package in the project's virtual environment:

```bash
poetry install --only local
```

Now, you can install the pre-commit hooks with the following command:

```bash
poetry run pre-commit install
```

Check `.pre-commit-config.yaml` file for more information about the pre-commit
hooks configuration.

## Linting and Formatting

For code linting and formatting, this project uses
[Ruff](https://docs.astral.sh/ruff/). To install Ruff, you should first install
[Poetry](https://python-poetry.org/) and then run the following commands to
install Ruff in the project's virtual environment:

```bash
poetry install --only local
```

To run the linters, execute the following command:

```bash
poetry run ruff check
```

Append the `--fix` flag to the above command to automatically fix the issues.

To format the code, run the following command:

```bash
poetry run ruff format
```

Check `[tool.ruff]` section in the `pyproject.toml` file for more information
about the Ruff configuration.

## Deployment

Both the development and production environments are set up on the same droplet
(server) on [Digital Ocean](https://www.digitalocean.com/). The project is
deployed using Docker and Docker Compose.

### Development Environment

Project is deployed automatically to the development environment on every push
to the `develop` branch. Check the
[.github/workflows/develop.dev.yml](.github/workflows/deploy.dev.yml) file for
more information about the deployment configuration.

### Production Environment

Project can be deployed manually to the production environment by running the
`Deploy PROD` workflow in the GitHub Actions tab. Check the
[.github/workflows/deploy.prod.yml](.github/workflows/deploy.prod.yml) file for
more information about the deployment configuration.
