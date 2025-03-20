FROM python:3.10
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y postgresql-client git
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8001
CMD ["uvicorn", "mainmemory:app", "--host", "0.0.0.0", "--port", "8001"]
