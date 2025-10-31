FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir discord.py python-dotenv transformers torch requests

# Copy source code
COPY bot.py .

# Copy environment file (if needed, or mount at runtime)
COPY .env .env

# Run the bot
CMD ["python", "bot.py"]