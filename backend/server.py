from mangum import Mangum  # Converts FastAPI (ASGI) to AWS Lambda-compatible app

from main import app  # Import your FastAPI app from main.py

handler = Mangum(app)
