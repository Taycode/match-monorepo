# Use an official Python runtime as a parent image
FROM python:3.11-bullseye

# Set the working directory in the container to /code
WORKDIR /code

# Copy the current directory contents into the container at /code
ADD . /code
ENV PYTHONUNBUFFERED=1

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

CMD ["python", "manage.py", "runserver"]
