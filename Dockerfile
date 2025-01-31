 # Estágio de build
 FROM python:3.9-slim as builder

 WORKDIR /app
 RUN pip install poetry
 COPY pyproject.toml poetry.lock* ./
 RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
 
 # Estágio final
 FROM python:3.9-slim
 
 WORKDIR /app
 COPY --from=builder /app/requirements.txt .
 RUN pip install --no-cache-dir -r requirements.txt
 COPY . .
 EXPOSE 8000
 CMD ["uvicorn", "meu_projeto.main:app", "--host", "0.0.0.0", "--port", "8000"]