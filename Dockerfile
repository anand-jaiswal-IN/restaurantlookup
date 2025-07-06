FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_CACHE_DIR=/tmp/uv-cache
ENV NODE_VERSION=20.11.1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libpq-dev \
    ca-certificates \
    xz-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js directly from official binaries
RUN curl -fsSLO https://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION-linux-x64.tar.xz \
    && tar -xJf node-v$NODE_VERSION-linux-x64.tar.xz -C /usr/local --strip-components=1 \
    && rm node-v$NODE_VERSION-linux-x64.tar.xz \
    && ln -s /usr/local/bin/node /usr/local/bin/nodejs

# Install uv
RUN pip install uv

# Set work directory
WORKDIR /app

# Copy package files
COPY pyproject.toml uv.lock ./
COPY package*.json ./

# Install Python dependencies using uv
RUN uv sync --frozen

# Install npm dependencies
RUN npm ci --only=production

# Copy project files
COPY . .

# Create staticfiles directory
RUN mkdir -p staticfiles

# Expose port
EXPOSE 8000

# Create entrypoint script
RUN echo '#!/bin/bash\n\
    set -e\n\
    \n\
    echo "Installing packages..."\n\
    uv sync --frozen\n\
    npm ci --only=production\n\
    \n\
    echo "Waiting for database connection..."\n\
    until uv run python -c "import psycopg2; psycopg2.connect(host='\''$DB_HOST'\'', port='\''$DB_PORT'\'', dbname='\''$DB_NAME'\'', user='\''$DB_USER'\'', password='\''$DB_PASSWORD'\'')"; do\n\
    echo "Database is unavailable - sleeping"\n\
    sleep 1\n\
    done\n\
    echo "Database is up!"\n\
    \n\
    echo "Running migrations..."\n\
    uv run python manage.py migrate\n\
    \n\
    echo "Collecting static files..."\n\
    uv run python manage.py collectstatic --noinput\n\
    \n\
    echo "Starting server with gunicorn..."\n\
    exec uv run gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 120 restaurantlookup.wsgi:application' > /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]