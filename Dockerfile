FROM python:3.11-slim

WORKDIR /code

RUN adduser --system --group appuser

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser app/ ./app/

WORKDIR /code/app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
