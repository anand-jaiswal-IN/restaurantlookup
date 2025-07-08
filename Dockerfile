FROM python:3.12.3-slim-bookworm

# Install uv
RUN pip install uv

# Copy dependency files
WORKDIR /app
COPY . .

# Install dependencies into the virtual environment
RUN uv sync --no-cache

# Expose port
EXPOSE 8000

# Run the application
CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "restaurantlookup.wsgi"]