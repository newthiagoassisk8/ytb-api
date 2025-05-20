# Usa uma imagem oficial do Python
FROM python:3.11-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos da aplicação
COPY . /app

# Instala dependências do sistema para o yt_dlp funcionar corretamente
RUN apt-get update && apt-get install -y \
    ffmpeg \
 && rm -rf /var/lib/apt/lists/*

# Instala dependências do Python
RUN pip install --no-cache-dir fastapi uvicorn yt-dlp

# Expõe a porta usada pela aplicação
EXPOSE 8000

# Comando para iniciar o servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
