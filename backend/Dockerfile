# Use official Python image
# FROM python:3.12
FROM python:3.12-slim


# Set the working directory
WORKDIR /app

# Install uv first
RUN pip install uv

# Copy the application files
COPY . .

# Install dependencies using uv
# RUN uv pip install -r requirements.txt
# If you're using Docker, it's usually best not to use a virtual environment inside the container because Docker itself provides isolation. So the second option (--system) is generally preferred.
RUN uv pip install --system -r requirements.txt


# Expose FastAPI default port
EXPOSE 8000

# Run FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
