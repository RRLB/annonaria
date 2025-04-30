FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 4000
ENV FLASK_APP=run.py
CMD ["flask", "run", "--host=0.0.0.0", "--port=4000"]