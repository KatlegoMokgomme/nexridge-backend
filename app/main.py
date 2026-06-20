from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import traceback

# ------------------------
# DATABASE (IMPORTANT)
# ------------------------
from app.core.database import Base, engine
from app.models.ticket import Ticket
from app.models.user import User

# ------------------------
# ROUTERS
# ------------------------
from app.api.v1 import auth, tickets, dashboard, notifications

# ------------------------
# SCHEDULER
# ------------------------
from app.core.scheduler import start_scheduler

# ------------------------
# CREATE APP
# ------------------------
app = FastAPI(
    title="Ticket System API",
    version="1.0.0"
)

# ------------------------
# CORS CONFIGURATION (FIX FOR REACT)
# ------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------
# CREATE DATABASE TABLES (DEV ONLY)
# ------------------------
Base.metadata.create_all(bind=engine)

# ------------------------
# INCLUDE ROUTERS
# ------------------------
app.include_router(auth.router)
app.include_router(tickets.router)
app.include_router(dashboard.router)
app.include_router(notifications.router)

# ------------------------
# GLOBAL ERROR HANDLER
# ------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print("🔥 ERROR OCCURRED:", exc)
    traceback.print_exc()

    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )

# ------------------------
# STARTUP EVENT
# ------------------------
@app.on_event("startup")
def startup_event():
    start_scheduler()
    print("🚀 Application started successfully")