services:
  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434" # Host port:Container port
    volumes:
      - ollama-data:/root/.ollama
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:11434/api/tags"]
      interval: 5s
      timeout: 5s
      retries: 12
    networks: # Add ollama service to the network
      - pizza_network

  pizza-app:
    build: .
    depends_on:
      ollama:
        condition: service_healthy
    ports:
      - "7860:7860" # Host port:Container port
    environment:
      - PYTHONUNBUFFERED=1
    networks: # Add pizza-app service to the network
      - pizza_network

volumes:
  ollama-data:

networks: # Define the network
  pizza_network:
    driver: bridge