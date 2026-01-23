FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir --default-timeout=1000 -r requirements.txt

# Copy the rest of your code
COPY . .

# The command is now handled by docker-compose or here
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
