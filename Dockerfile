FROM python:3.9
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y postgresql-client
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "mainmemory:app", "--host", "0.0.0.0", "--port", "8001"]
