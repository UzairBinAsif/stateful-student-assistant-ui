# Use an official Python base image
FROM python:3.13

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Make sure /app is writable
RUN chmod -R 777 /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7860

# Start Chainlit
CMD ["chainlit", "run", "main.py", "--host", "0.0.0.0", "--port", "7860"]