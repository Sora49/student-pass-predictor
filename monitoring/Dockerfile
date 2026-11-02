# Build context is the project root (see docker-compose.yml)
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
COPY monitoring/requirements-api.txt .
RUN pip install -r requirements-api.txt
COPY src/ src/
COPY data/ data/
COPY monitoring/api.py .
RUN python -m src.train
EXPOSE 5000
CMD ["python", "api.py"]
