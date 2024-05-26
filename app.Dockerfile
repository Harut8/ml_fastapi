FROM python:3.11
WORKDIR /app
COPY pyproject.toml poetry.lock entrypoint.sh ./
RUN ["chmod", "+x", "entrypoint.sh"]
RUN pip install --upgrade pip
RUN pip --no-cache-dir install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
ADD .. /app/
ENTRYPOINT ["sh", "/app/entrypoint.sh"]
CMD ["uvicorn", "--lifespan=on", "main:app", "--host", "0.0.0.0", "--workers", "3", "--port", "80"]