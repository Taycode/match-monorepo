# Use an official Python runtime as a parent image
FROM python:3.11-bullseye

# Set the working directory in the container to /code
WORKDIR /code

# Copy the current directory contents into the container at /code
ADD . /code
ENV PYTHONUNBUFFERED=1

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Configure Poetry to create a virtual environment inside the container
RUN poetry config virtualenvs.in-project true

# Install dependencies using Poetry
RUN poetry install --no-interaction --no-ansi

# Set the Poetry virtual environment's path
ENV VENV_PATH="/code/.venv"

# Activate the virtual environment and ensure it's used for the app
ENV PATH="$VENV_PATH/bin:$PATH"

# Set default port using an environment variable
ENV PORT=8000

# Expose the port dynamically
EXPOSE $PORT

# Default entrypoint script to apply migrations and start the server
ENTRYPOINT ["sh", "-c", "poetry run python manage.py migrate && poetry run python manage.py runserver 0.0.0.0:$PORT"]
