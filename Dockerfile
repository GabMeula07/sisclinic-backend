# Use uma imagem leve do Python
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo .whl para o container
COPY dist/app-0.1.0-py3-none-any.whl /app/

# Instala as dependências do sistema (caso precise)
RUN apt-get update && apt-get install -y \
    gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Instala o pacote usando o wheel
RUN pip install --no-cache-dir app-0.1.0-py3-none-any.whl

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]