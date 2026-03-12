FROM python:3.12-slim

WORKDIR /main

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "geo_project.main:app", "--host", "0.0.0.0", "--port", "8000"]