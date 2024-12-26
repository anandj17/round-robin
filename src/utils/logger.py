import os
import sys
import logging
from pathlib import Path
from typing import Optional
from logging.handlers import RotatingFileHandler

class Logger:

    def __init__(self, name):
        self.name = name
        self.log_dir = "logs"
        self.level = "INFO"

    def get_file_handler(self, name: str, log_dir: str = "logs") -> RotatingFileHandler:
        Path(self.log_dir).mkdir(exist_ok=True)

        log_file = os.path.join(self.log_dir, f"{self.name}.log")
        handler = RotatingFileHandler(
            log_file,
            maxBytes=10_000_000,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        
        return handler

    def setup_logger(self) -> logging.Logger:
        logger = logging.getLogger(self.name)
    
        log_level = getattr(logging, (self.level or "INFO").upper())
        logger.setLevel(log_level)
        
        if not logger.handlers:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(log_level)
            console_handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            ))
            logger.addHandler(console_handler)
            
            file_handler = self.get_file_handler(self.name)
            file_handler.setLevel(log_level)
            logger.addHandler(file_handler)
        
        return logger