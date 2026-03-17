# Grace-Mar — multi-stage: base Python + optional Pandoc for PDF/curriculum scripts
# Use for miniapp_server, gate-review-app, and CLI scripts (export, merge, etc.)
ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim AS base
WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Install root + bot dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY bot/requirements.txt bot/requirements.txt
RUN pip install --no-cache-dir -r bot/requirements.txt

# App code (miniapp_server, gate-review-app, bot, scripts)
COPY bot/ bot/
COPY scripts/ scripts/
COPY miniapp/ miniapp/
COPY users/ users/
COPY gate-review-app.py miniapp_server.py .

EXPOSE 5000 5001
CMD ["python", "miniapp_server.py"]
