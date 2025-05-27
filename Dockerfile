FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only what's needed early to leverage Docker cache
COPY requirements.txt .

# Install system deps and Python packages
RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Now copy the rest of your code (after installing deps)
COPY . .

# Set Streamlit config
ENV XDG_CONFIG_HOME=/app/.streamlit
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Expose the default port
EXPOSE 7860

# Start Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0", "--server.enableCORS=false"]
