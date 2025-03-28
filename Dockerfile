# Usar a imagem base mais leve do Python
FROM python:3.11-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Instalar dependências do sistema (se necessário) e copiar apenas os arquivos essenciais
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copiar apenas o arquivo de dependências primeiro para cache de camadas
COPY requirements.txt .

# Instalar as dependências da aplicação
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código para o container
COPY . .

# Expor a porta do Django
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
