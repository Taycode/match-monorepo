# Use an official Python runtime as a parent image
FROM python:3.11-bullseye

# Set the working directory in the container to /code
WORKDIR /code

# Copy the current directory contents into the container at /code
ADD . /code
ENV PYTHONUNBUFFERED=1

# Set default port using an environment variable
ENV PORT=8000

# Expose the port dynamically (the port exposed here is more for documentation as the actual exposure happens at runtime)
EXPOSE $PORT

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Use an ENTRYPOINT to use the environment variable
ENTRYPOINT ["sh", "-c", "python manage.py runserver 0.0.0.0:$PORT"]
