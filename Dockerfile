# Use an official Python base image
FROM python:3.13

RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy all files
COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
# COPY . .

# Make sure /app is writable
# RUN chmod -R 777 /app

# Install dependencies

# EXPOSE 7860

# Start Chainlit
COPY --chown=user . /app
CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0", "--port", "7860"]