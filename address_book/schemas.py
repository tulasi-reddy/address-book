from pydantic import BaseModel

class Address(BaseModel):
    address_line_one : str
    address_line_two : str
    address_line_three : str
    city_name : str
    state_name : str
    pin_code : str
    land_mark : str
    latitude : float
    longitude : float
    
class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "addressbook"
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
        "file": {
            "format": "[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s"
        }
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "file": {
            "level": LOG_LEVEL,
            "class": "logging.FileHandler",
            "formatter": "file",
            "filename": "debug.log"
        }
    }
    loggers = {
        "addressbook": {"handlers": ["file","default"], "level": LOG_LEVEL},
    }
    
    