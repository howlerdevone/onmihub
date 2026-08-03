"""Entry point for running omnihub as a module: `python -m omnihub`"""

# Load .env first, before any app imports that might depend on environment variables
from .config.dotenv import load_dotenv_if_present
load_dotenv_if_present()

# Now import and run the app
from .cli import app

if __name__ == "__main__":
    app()
