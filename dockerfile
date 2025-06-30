FROM python:3.10-slim-buster

ENV PYTHONWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

WORKDIR /src/app

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    libmysqlclient-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# 🔧 کپی هر دو entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# پیش‌فرض: حالت production
ENTRYPOINT ["/entrypoint.sh"]