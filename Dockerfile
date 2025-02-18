FROM python:3.12-alpine
COPY pyproject.toml poetry.lock .
RUN pip install poetry && poetry install --without dev --no-root --no-directory
COPY redmine_bot/ ./redmine_bot
COPY README.md .
RUN poetry install --only-root
ENTRYPOINT ["poetry", "run", "redmine-bot"]
