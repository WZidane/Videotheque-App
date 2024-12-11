FROM videotheque:1.0

RUN apt-get update

WORKDIR /app

RUN pip install --no-cache-dir flask

COPY . .
