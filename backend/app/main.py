from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.submit import router as submit_router

app = FastAPI(title="Cybercrime Evidence API")

# Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Routes
app.include_router(submit_router)
