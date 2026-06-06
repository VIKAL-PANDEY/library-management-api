import logging
import sys

def setup_logger(name: str = "library_api") -> logging.Logger:
    """
    Configures and returns a standard logging instance for the application.
    Ensures that handlers are only added once to avoid duplicate log entries.
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Structured log output format
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(levelname)s - [%(name)s] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # Write to stdout
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # Prevent propagation to the root logger to control formatting
        logger.propagate = False
        
    return logger

# Singleton logger instance for application-wide import
logger = setup_logger()
