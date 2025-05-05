FROM python:3.13-slim
# Set the working directory
WORKDIR /app
# Install the required Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy the rest of the application files
COPY . .
# Expose the port the app runs on
EXPOSE 4000
# Set environment variables
#ENV FLASK_APP=run.py
# Command to run the application
#CMD ["flask", "run", "--host=0.0.0.0", "--port=4000"]
ENV PYTHONPATH=/app
CMD ["python", "run.py"]