FROM python:3.10.4-slim

WORKDIR /khasbot

COPY requirements.txt .

RUN python -m pip install --upgrade pip && pip install -r /khasbot/requirements.txt --no-cache-dir

COPY . .

CMD ["python", "bot.py"] 