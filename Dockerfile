# Small, fast image for the Streamlit app
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# 1) Install dependencies first -> this layer is cached on rebuilds
COPY requirements.txt .
RUN pip install -r requirements.txt

# 2) Copy the code + data and train the model inside the image (takes ~1 s)
COPY src/ src/
COPY data/ data/
COPY app.py .
RUN python -m src.train

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
