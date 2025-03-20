# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in pyproject.toml
RUN pip install poetry && poetry install

# Make port 80 available to the world outside this container
EXPOSE 80

# Run demo script when the container launches
CMD ["poetry", "run", "python", "demo/demo_script.py"]