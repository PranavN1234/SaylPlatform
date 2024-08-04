from app import create_app
from dotenv import load_dotenv

load_dotenv(verbose=True, override=True)

app = create_app()

if __name__ == '__main__':
    app.run(port=8000, debug=True)