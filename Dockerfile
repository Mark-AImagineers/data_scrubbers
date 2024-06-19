FROM python:3.11.4-alpine

WORKDIR /usr/src/app

# Prevent Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1

# Ensure Python output is sent directly to the terminal without buffering
ENV PYTHONUNBUFFERED 1

# Upgrade pip
RUN pip install --upgrade pip

# Install system dependencies for common packages
# This might include dependencies used in Django/Scrapy projects

RUN apk add --no-cache netcat-openbsd

RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && apk add --no-cache jpeg-dev zlib-dev libxml2-dev libxslt-dev

RUN apk add --no-cache gcc musl-dev linux-headers libc-dev

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the entire project
COPY . .

# Ensure entrypoint script is executablesss
RUN chmod +x data_scrub/entrypoint.sh

# Set the entrypoint to the script
ENTRYPOINT ["./data_scrub/entrypoint.sh"]