FROM python:3.10-slim

WORKDIR /app

# Copy everything including the hidden .streamlit folder
COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Make sure Streamlit doesn't try to write to root
RUN mkdir -p /app/.streamlit

EXPOSE 7860

CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
