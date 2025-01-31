# Estágio de build
FROM python:3.10-slim as builder

WORKDIR /app

# Instala o Poetry
RUN pip install --upgrade pip && \
    pip install poetry

# Copia os arquivos de dependências
COPY pyproject.toml poetry.lock* ./

# Instala as dependências do projeto (apenas produção)
RUN poetry config virtualenvs.create false && \
    poetry install --without dev

# Copia o restante do código-fonte
COPY . .

# Estágio final
FROM python:3.9-slim

WORKDIR /app

# Copia as dependências instaladas do estágio de build
COPY --from=builder /app /app

# Expõe a porta da aplicação
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["poetry", "run", "uvicorn", "meu_projeto.main:app", "--host", "0.0.0.0", "--port", "8000"]