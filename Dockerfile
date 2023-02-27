FROM python:3.9
ENV TZ="Europe/Moscow"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./fakegeo_polychessbot /app
WORKDIR /app
ENTRYPOINT ["python", "main.py"]
