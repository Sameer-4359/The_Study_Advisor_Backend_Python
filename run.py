import uvicorn
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8005))  # use Railway's PORT if available
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
