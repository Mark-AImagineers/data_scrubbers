FROM python:3.10

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install --upgrade pip \
    && apt-get update \
    && apt-get install -y netcat-openbsd libjpeg-dev zlib1g-dev libxml2-dev libxslt1-dev \
    && apt-get install -y --no-install-recommends build-essential \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get remove -y build-essential \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN chmod +x data_scrub/entrypoint.sh

ENTRYPOINT ["./data_scrub/entrypoint.sh"]