#!/usr/bin/env bash
# Code maathina aprom redeploy:  bash deploy/update.sh
set -euo pipefail
cd /home/ubuntu/E-library
source venv/bin/activate
git pull
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn-sanza
sudo systemctl reload nginx
echo "Updated."
