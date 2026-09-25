#!/bin/sh
set -e

DOMAIN="vsenglish.me"
EMAIL="${1:-vs.english.learning@gmail.com}"
CERT_DIR="./certbot/conf/live/$DOMAIN"

mkdir -p "$CERT_DIR"
mkdir -p "./certbot/www"

if [ ! -f "$CERT_DIR/fullchain.pem" ]; then
  openssl req -x509 -nodes -newkey rsa:2048 -days 1 \
    -keyout "$CERT_DIR/privkey.pem" \
    -out "$CERT_DIR/fullchain.pem" \
    -subj "/CN=localhost"
fi

docker compose -f docker-compose.prod.yml up -d nginx

docker compose -f docker-compose.prod.yml run --rm --entrypoint certbot certbot certonly \
  --webroot \
  --webroot-path=/var/www/certbot \
  --email "$EMAIL" \
  --agree-tos \
  --no-eff-email \
  --force-renewal \
  -d "$DOMAIN" \
  -d "www.$DOMAIN"

docker compose -f docker-compose.prod.yml exec nginx nginx -s reload
docker compose -f docker-compose.prod.yml up -d certbot
