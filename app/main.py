from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import traceback

# ------------------------
# DATABASE
# ------------------------
from app.core.database import Base, engine
from app.models.ticket import Ticket
from app.models.user import User

# ------------------------
# ROUTERS (FIXED IMPORT PATH)
# ------------------------
from app.api import auth, tickets, dashboard, notifications

# ------------------------
# SCHEDULER
# ------------------------
from app.core.scheduler import start_scheduler

# ------------------------
# CREATE APP
# ------------------------
app = FastAPI(
    title="Nexridge Ticket System API",
    version="1.0.0"
)

# ------------------------
# CORS (REACT + ELECTRON SUPPORT)
# ------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost",
        "app://."
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------
# CREATE TABLES (DEV ONLY)
# ------------------------
Base.metadata.create_all(bind=engine)

# ------------------------
# REGISTER ROUTERS
# ------------------------
app.include_router(auth.router)
app.include_router(tickets.router)
app.include_router(dashboard.router)
app.include_router(notifications.router)

# ------------------------
# ROOT HEALTH CHECK
# ------------------------
@app.get("/")
def root():
    return {
        "message": "Nexridge API running successfully",
        "status": "ok"
    }

# ------------------------
# GLOBAL ERROR HANDLER
# ------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print("🔥 ERROR OCCURRED:", exc)
    traceback.print_exc()

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc)
        }
    )

# ------------------------
# STARTUP EVENT
# ------------------------
@app.on_event("startup")
def startup_event():
    start_scheduler()
    print("🚀 Application started successfully")