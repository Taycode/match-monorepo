# Use an official Python runtime as a parent image
FROM python:3.11-bullseye

# Set the working directory in the container to /code
WORKDIR /code

# Copy the current directory contents into the container at /code
ADD . /code
ENV PYTHONUNBUFFERED=1

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port exposed configurable via an environment variable with default value
ARG DEFAULT_PORT=7222
ENV PORT=${DEFAULT_PORT}
EXPOSE $PORT

# Command to run the application, using the PORT environment variable
CMD ["python", "manage.py", "runserver", "0.0.0.0:${PORT}"]