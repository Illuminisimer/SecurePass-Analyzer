from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.analysis import router as analysis_router
from .api.auth import router as auth_router
from .api.assistant import router as assistant_router
from .api.otp import router as otp_router
from .api.vault import router as vault_router
from .database.connection import init_db

app = FastAPI(
    title="SecurePass Analyzer API",
    description="Backend service for enterprise-grade password strength analysis and secure vault storage.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis_router)
app.include_router(auth_router)
app.include_router(assistant_router)
app.include_router(otp_router)
app.include_router(vault_router)


@app.on_event("startup")
async def startup_event() -> None:
    await init_db()


@app.get("/", tags=["health"])
async def root() -> dict[str, str]:
    return {"message": "SecurePass Analyzer backend is running."}
