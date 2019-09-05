FROM python:3-alpine

COPY src /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "bot.py" ]
