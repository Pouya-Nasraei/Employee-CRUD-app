import os
import logging
from gui import start_gui

# Create logs folder if it does not exist
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

if __name__ == "__main__":
    logging.info("Application started")
    start_gui()