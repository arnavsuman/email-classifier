from fastapi import FastAPI
from api import router

app = FastAPI(title="Email Classification API")

# Register the /classify router
app.include_router(router)

# Add this root route to fix the 404 on /
@app.get("/")
def root():
    return {
        "message": "🚀 Email Classification API is running!",
        "usage": "Send a POST request to /classify with {'input_email_body': '...'}"
    }
