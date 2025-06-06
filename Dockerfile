# Use an official Python base image
FROM python:3.13

# Set working directory
WORKDIR /main

# Copy all files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Chainlit will run on
EXPOSE 7860

# Start Chainlit (FastAPI runs here)
CMD ["chainlit", "run", "main.py", "--host", "0.0.0.0", "--port", "7860"]
