#!/usr/bin/env bash
# Fresh Ubuntu 24.04 EC2-la oru thadava run pannunga:  bash deploy/setup.sh
# Munnadi: project /home/ubuntu/E-library-la irukkanum, .env ready-a irukkanum.
set -euo pipefail

APP_DIR=/home/ubuntu/E-library
cd "$APP_DIR"

echo "==> System packages"
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-venv python3-pip python3-dev libpq-dev build-essential \
                    postgresql postgresql-contrib nginx git ufw

echo "==> Python venv + requirements"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "==> Postgres DB create (.env values use panni)"
set -a; source .env; set +a
sudo -u postgres psql -tc "SELECT 1 FROM pg_roles WHERE rolname='${DB_USER}'" | grep -q 1 || \
  sudo -u postgres psql -c "CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}';"
sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname='${DB_NAME}'" | grep -q 1 || \
  sudo -u postgres psql -c "CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};"

echo "==> Django: migrate + collectstatic"
mkdir -p media
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py check --deploy || true

echo "==> Gunicorn service"
sudo cp deploy/gunicorn.service /etc/systemd/system/gunicorn-sanza.service
sudo systemctl daemon-reload
sudo systemctl enable --now gunicorn-sanza

echo "==> Nginx"
sudo cp deploy/nginx-sanza.conf /etc/nginx/sites-available/sanza
sudo ln -sf /etc/nginx/sites-available/sanza /etc/nginx/sites-enabled/sanza
sudo rm -f /etc/nginx/sites-enabled/default
# nginx (www-data) media/static folders-a read panna home dir traverse permission
sudo chmod 755 /home/ubuntu
sudo nginx -t && sudo systemctl restart nginx

echo "==> Firewall"
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw --force enable

echo
echo "DONE. Next: python manage.py createsuperuser  ->  then HTTPS: sudo certbot --nginx"
