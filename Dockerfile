FROM python:3.11.4-alpine

WORKDIR /usr/src/app

# Prevent Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1

# Ensure Python output is sent directly to the terminal without buffering
ENV PYTHONUNBUFFERED 1

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the entire project
COPY . .

# Ensure entrypoint script is executable
RUN chmod +x data_scrub/entrypoint.sh

# Set the entrypoint to the script
ENTRYPOINT ["./data_scrub/entrypoint.sh"]