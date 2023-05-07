FROM python:3.11
ENV TZ="Europe/Moscow"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./ /app
WORKDIR /app
ENTRYPOINT ["python", "."]
