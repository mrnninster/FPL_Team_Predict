# Imports
import uvicorn
import logging
import routers.routes as routes

from fastapi import FastAPI,responses
from config import LogConfig,Settings
from dotenv import load_dotenv
from logging.config import dictConfig
from fastapi.middleware.cors import CORSMiddleware

# Create Logger
dictConfig(LogConfig().dict())
logger = logging.getLogger("Engine")

# allowed Origins
origins = [
    "https://localhost:3000",
    "http://localhost:3000",
    "https://fplteamview.com"
]

# Load Env File
load_dotenv(".env")

# Load Env Variables
settings = Settings()

# Create App Instance
app = FastAPI()

# allowed Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Include Created Routes
app.include_router(routes.router)


# Root destination
@app.get("/")
async def root():
    return responses.RedirectResponse('/redoc')


if __name__ == "__main__":
    uvicorn.run("main:app", port=settings.app_port, reload=True, access_log=False)