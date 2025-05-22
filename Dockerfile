FROM python:3.10-slim

WORKDIR /app

# Copy project files
COPY . /app
COPY .streamlit /app/.streamlit

# Prevent Streamlit from writing to the root
ENV XDG_CONFIG_HOME=/app/.streamlit
ENV STREAMLIT_HOME=/app/.streamlit
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port
EXPOSE 7860

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
