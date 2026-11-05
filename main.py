# main.py
"""
HealthMate AI - Bilingual AI Health Assistant
FastAPI Full-Stack Python Web Application with Jinja2 SSR
Run with: uvicorn main:app --reload --port 8000
"""

import os
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

# Import modular application routers
from routes.views import router as views_router, templates
from routes.chat import router as chat_router
from routes.vitals import router as vitals_router
from routes.report import router as report_router
from routes.api import router as api_router

app = FastAPI(
    title="HealthMate AI - Bilingual Health Assistant",
    description=(
        "A Python-powered bilingual health assistant supporting Tamil and English. "
        "Built with FastAPI, Jinja2, Strands Agents SDK, and Google Gemini 2.0 Flash."
    ),
    version="3.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static file serving
static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Inject standard datetime helpers into Jinja2 environment
def format_datetime_now(fmt="%Y-%m-%d"):
    return datetime.now().strftime(fmt)

templates.env.globals["now_date"] = datetime.now().strftime("%Y-%m-%d")
templates.env.globals["now_time"] = datetime.now().strftime("%H:%M")
templates.env.globals["format_datetime_now"] = format_datetime_now

# Register modular routers
app.include_router(views_router)
app.include_router(chat_router)
app.include_router(vitals_router)
app.include_router(report_router)
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
