import os
import secrets
from pydantic import BaseSettings, BaseModel

# Get Working Environmen
env_type = os.getenv("ENV_TYPE")
verified_Bearer_token = os.getenv("BEARER_TOKEN")

class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "FPL Team Create Engine"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        "Engine": {"handlers": ["default"], "level": LOG_LEVEL},
    }


class Settings(BaseSettings):
    app_name: str = "FPL Team Create Engine"
    app_port: int = 3000
    app_bearer_token: str = verified_Bearer_token
    
    if env_type == "Development":
        app_reload: bool = True
        app_debug: bool = True
        app_secret_key: str = "notAsecret"

    else:
        app_reload = False
        app_debug = False
        app_secret_key = secrets.token_hex()
