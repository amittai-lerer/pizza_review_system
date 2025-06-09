# main.py
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "backend.api:app",  # path.to.module:app_object
        host="127.0.0.1",
        port=8000,
        reload=True  
    )
