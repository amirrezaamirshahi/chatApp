# app/main.py

from fastapi import FastAPI, Depends
from app.routes import auth
from app.routes.auth import get_current_user

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/protected")
async def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello, {current_user}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
