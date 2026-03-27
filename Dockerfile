FROM python:3.12-slim

WORKDIR /geo_project/geo_project

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://geo-backend/health')" || exit 1

CMD ["uvicorn", "geo_project.main:app", "--host", "0.0.0.0", "--port", "8000"]