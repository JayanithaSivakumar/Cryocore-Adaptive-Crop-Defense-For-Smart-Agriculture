FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/python_core
ENV PYTHONPATH=/app/python_core
EXPOSE 8790
