FROM python:3.11-slim-bookworm

# Installer les dépendances système pour Chromium
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install fastapi uvicorn playwright

RUN playwright install --with-deps chromium

# On copie le script Python de l'API (voir étape suivante)
COPY api.py /app/api.py

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
