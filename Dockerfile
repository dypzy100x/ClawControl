FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY clawcontrol/ ./clawcontrol/
COPY config/ ./config/

RUN mkdir -p /root/.clawcontrol/config /root/.clawcontrol/logs

EXPOSE 8787

ENV HOST=0.0.0.0

CMD ["uvicorn", "clawcontrol.main:app", "--host", "0.0.0.0", "--port", "8787"]
