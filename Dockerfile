FROM python:3.9
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
WORKDIR /app
ENTRYPOINT ["python", "main.py"]
