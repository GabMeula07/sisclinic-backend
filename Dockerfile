# Etapa final do container
FROM python:3.10-slim AS runtime
WORKDIR /app
RUN pip install --upgrade pip

RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*


COPY --from=builder /app/dist/*.tar.gz .
RUN pip install --no-cache-dir *.tar.gz


COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]