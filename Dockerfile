# Use official Python base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    git \
    npm \
    && apt-get clean

# Install uv (like pipenv or poetry)
RUN pip install uv

# Copy only dependency files first for caching
COPY uv.lock pyproject.toml ./

# Install Python dependencies
RUN uv pip install -r requirements.txt

# Copy rest of the project
COPY . .

# Install npm dependencies (for Tailwind/Flowbite)
RUN npm install

# Build Tailwind CSS
RUN npx tailwindcss -i ./static/src/input.css -o ./static/css/output.css --minify

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run Gunicorn
CMD ["gunicorn", "restaurantlookup.wsgi:application", "--bind", "0.0.0.0:8000"]
