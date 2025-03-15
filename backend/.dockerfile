# Use official Python image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Install uv first
RUN pip install uv

# Copy the application files
COPY . .

# Install dependencies using uv
RUN uv pip install -r requirements.txt

# Expose FastAPI default port
EXPOSE 8000

# Run FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
