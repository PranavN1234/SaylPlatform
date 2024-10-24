from app import create_app
from dotenv import load_dotenv
import logging

# Configure logging to console (captured by Gunicorn)
logging.basicConfig(
    level=logging.INFO,  # Set to DEBUG to capture all types of logs
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler()  # Log to the console, captured by Gunicorn
    ]
)

load_dotenv(verbose=True, override=True)

app = create_app()

if __name__ == '__main__':
    app.run(port=8000, debug=True)
