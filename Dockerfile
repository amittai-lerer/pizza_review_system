FROM python:3.10-slim

WORKDIR /app

# Copy everything including the app code and requirements
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Ensure Streamlit config directory exists AND config file is copied
RUN mkdir -p /app/.streamlit
COPY .streamlit /app/.streamlit

# Expose Streamlit's default port
EXPOSE 7860

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
