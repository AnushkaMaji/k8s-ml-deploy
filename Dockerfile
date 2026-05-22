# Start from an official Python image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first (for faster rebuilds)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Tell Docker your app runs on port 8000
EXPOSE 8000

# Command to start the API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]