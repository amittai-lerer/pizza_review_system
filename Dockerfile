FROM python:3.10-slim

WORKDIR /app

# Install system dependencies (git, curl) first, as they change less often
RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*

# Copy only the requirements file to leverage Docker cache
COPY requirements.txt /app/requirements.txt

# Upgrade pip and install Python dependencies
# This layer will be cached if requirements.txt doesn't change
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# Now copy the rest of the application code
# The .dockerignore file will ensure unnecessary files are excluded
COPY . /app

# Ensure .streamlit directory is correctly set up if it contains necessary runtime configs (not secrets)
# If .streamlit/config.toml is part of your source and not in .dockerignore, 
# the previous COPY . /app might have handled it. This explicit copy ensures it if needed.
# Critical: .streamlit/secrets.toml should NOT be copied into the image if it contains real secrets.
# It should be mounted as a secret at runtime or managed via environment variables.
COPY .streamlit /app/.streamlit

# Prevent Streamlit from writing to non-writable locations if any
ENV XDG_CONFIG_HOME=/app/.streamlit
ENV STREAMLIT_HOME=/app/.streamlit
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

EXPOSE 7860

CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
