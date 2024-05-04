FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]