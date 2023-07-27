
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
# Install the required Python packages
RUN pip install --no-cache-dir -r requirement.txt
# Copy the entire project folder into the container
COPY . .
# Expose the port that FastAPI will run on (change this if your app runs on a different port)
EXPOSE 80
# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
