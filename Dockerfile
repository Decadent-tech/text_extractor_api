# syntax=docker/dockerfile:1
FROM python:3.12-slim

# set workdir
WORKDIR /app

# copy requirements
COPY requirements.txt .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy the app
COPY . .

# expose port
EXPOSE 5000

# run
CMD ["python", "app.py"]