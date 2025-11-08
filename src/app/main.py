from fastapi import FastAPI
from app.api.v1.payments_router import router as payments_router



app = FastAPI()



@app.get("/health")
async def health_check():
    return {"status": "ok"}


app.include_router(payments_router)