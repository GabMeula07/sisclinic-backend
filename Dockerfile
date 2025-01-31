FROM python:3.10-slim AS runtime
WORKDIR /app

# Instala dependências do sistema (se necessário)
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copia o pacote já existente no dist
COPY dist/*.tar.gz .
RUN pip install --no-cache-dir *.tar.gz

# Copia o restante do código
COPY . .

# Comando para rodar o FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]