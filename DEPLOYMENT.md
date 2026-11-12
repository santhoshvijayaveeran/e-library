# Sanza E-Library — AWS EC2 Deployment Guide

Project: **Sanza E-Library** (Django 6.0, PostgreSQL, django-allauth Google login, Razorpay payments, Gmail SMTP, uploaded PDFs/images).
Target: **Ubuntu 24.04 EC2 + Nginx + Gunicorn + PostgreSQL (same server) + Let's Encrypt HTTPS**.

---

## 1. Architecture

```
Browser ──HTTPS──▶ Nginx (80/443)
                    ├─ /static/        ──▶ /home/ubuntu/E-library/staticfiles/
                    ├─ /media/books/   ──▶ BLOCKED (PDF Django view vazhiya mattum)
                    ├─ /media/         ──▶ /home/ubuntu/E-library/media/
                    └─ /              ──▶ Gunicorn (unix socket) ──▶ Django ──▶ PostgreSQL (localhost)
```

---

## 2. Code-la naan kandupidicha problems (deploy-ku munnadi fix pannanum)

| # | Problem | Enna aagum | Fix (bundle-la irukku) |
|---|---------|-----------|------------------------|
| 1 | `settings.py` kadaisila `DEBUG = True` hard-coded | `.env`-la `DEBUG=False` kuduthaalum override aagum — errors/secret info public-a theriyum | Andha line remove pannitten |
| 2 | `ALLOWED_HOSTS = []` | `DEBUG=False`-la site 400 error kudukkum | `.env`-la irundhu read pannum |
| 3 | `requirements.txt`-la `razorpay`, `django-import-export`, `Pillow` illa | `pip install` aprom `ModuleNotFoundError` / ImageField error | Add pannitten |
| 4 | `gunicorn` illa | App run aagaadhu | Add pannitten |
| 5 | `STATIC_ROOT` illa | `collectstatic` fail aagum | `staticfiles/` set pannitten |
| 6 | Media files `DEBUG=True`-la mattum serve aagum | Production-la cover images/author images theriyaadhu | Nginx `/media/` serve pannum |
| 7 | `CSRF_TRUSTED_ORIGINS`, secure cookies illa | HTTPS-la login/forms-la CSRF error | Settings-la add pannitten |
| 8 | **`.env` file zip-kulla irundhadhu** (Razorpay, Google, Gmail, DB secrets) | Yaaravadhu paartha secrets leak | **Ellaa keys-um rotate pannunga** (section 11) |
| 9 | Google client ID/secret `settings.py`-la use aagala | Google login work aagaadhu | Admin-la Social Application add pannanum (Step 10) |

Paid PDFs: `serve_book_pdf` view free books-ku mattum serve pannum. Nginx `/media/books/`-a block pannina, paid PDFs direct URL-la download panna mudiyaadhu. (Templates `pdf_file.url` use pannala — so idhu safe.)

---

## 3. Bundle-la irukkum files

| File | Enga podanum |
|------|--------------|
| `ebook/settings.py` | Project-oda `ebook/settings.py`-a replace pannunga (`settings.diff`-la maathangal paakalaam) |
| `requirements.txt` | Project root-la replace |
| `.env.example` | Server-la `.env`-a copy panni real values podunga |
| `deploy/setup.sh` | Server-la first time run |
| `deploy/gunicorn.service` | systemd service (setup.sh auto-a copy pannum) |
| `deploy/nginx-sanza.conf` | Nginx config (domain maathanum) |
| `deploy/update.sh` | Code update panna |
| `deploy/backup.sh` | DB + media backup |

---

## 4. Step-by-step

### Step 0 — Prerequisites
- AWS account
- Oru **domain** (GoDaddy / Namecheap / Route 53). **Google login-ku domain kattaayam theva** — Google raw IP address-a redirect URI-a accept pannaadhu.
- Razorpay account (live keys venum na KYC complete aagirukkanum)
- Gmail **App Password** (2-Step Verification on pannitu: Google Account → Security → App passwords)

### Step 1 — EC2 instance launch
1. AWS Console → **EC2 → Launch instance**
2. Name: `sanza-library`
3. AMI: **Ubuntu Server 24.04 LTS** (Django 6 ku Python 3.12+ venum; 24.04-la default 3.12 irukku)
4. Instance type: **t3.small** recommended (2 GB RAM). `t3.micro` (1 GB) la odum, aana swap add pannunga (Step 4b) and gunicorn workers 2-a vechukonga.
5. Key pair: **Create new** → `sanza-key.pem` download → safe-a vechukonga
6. Network → Security group (new):
   - SSH (22) → **My IP** mattum
   - HTTP (80) → Anywhere
   - HTTPS (443) → Anywhere
   - ❌ 5432 (Postgres), 8000 — **open pannaadhinga**
7. Storage: **20 GB gp3**
8. Launch

### Step 2 — Elastic IP (fixed IP)
EC2 → **Elastic IPs → Allocate → Associate** with your instance. (Illa na instance restart pannina IP maarum.)

### Step 3 — Domain DNS
Domain provider-la:
```
A    @      <ELASTIC_IP>
A    www    <ELASTIC_IP>
```
`ping yourdomain.com` la IP vandhaa ready (few minutes–hours aagalam).

### Step 4 — SSH login
Local machine-la:
```bash
chmod 400 sanza-key.pem
ssh -i sanza-key.pem ubuntu@<ELASTIC_IP>
```

**4b. (t3.micro mattum) Swap add pannunga:**
```bash
sudo fallocate -l 2G /swapfile && sudo chmod 600 /swapfile
sudo mkswap /swapfile && sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### Step 5 — Project server-ku upload
**Option A (recommended): Git**
```bash
cd ~ && git clone <your-repo-url> E-library
```
**Option B: scp** (local machine-la irundhu; `.env`, `db.sqlite3`, `__pycache__` thavira)
```bash
cd E-library.2
rsync -avz -e "ssh -i sanza-key.pem" \
  --exclude '.env' --exclude 'db.sqlite3' --exclude '__pycache__' --exclude 'venv' --exclude '*.backup' \
  E-library/ ubuntu@<ELASTIC_IP>:~/E-library/
```
> Project path **`/home/ubuntu/E-library`** aa irukkanum (service & nginx files adhai expect pannum). Vera path na andha files-la maathunga.

### Step 6 — Deployment files apply pannunga
Bundle-a project-kulla copy pannunga (local-la irundhu):
```bash
scp -i sanza-key.pem sanza-ec2-deploy/requirements.txt ubuntu@<IP>:~/E-library/
scp -i sanza-key.pem sanza-ec2-deploy/ebook/settings.py ubuntu@<IP>:~/E-library/ebook/
scp -i sanza-key.pem -r sanza-ec2-deploy/deploy ubuntu@<IP>:~/E-library/
```
Better: ivatrai git-la commit pannitu server-la `git pull`.

### Step 7 — `.env` create
```bash
cd ~/E-library
cp .env.example .env     # (.env.example-a um scp pannunga)
nano .env
```
Important values:
- `SECRET_KEY` → **pudhusa generate pannunga**:
  `python3 -c "import secrets; print(secrets.token_urlsafe(50))"`
- `DEBUG=False`
- `ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,<ELASTIC_IP>`
- `CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com`
- `DB_*` → neenga vekkura pudhu DB name/user/password (setup.sh adhe values-la DB create pannum)
- `DB_HOST=localhost`
- HTTPS certificate varum varai test panna: `USE_HTTPS=False` (Step 9 aprom `True` aakkunga)

```bash
chmod 600 .env
```

### Step 8 — Nginx domain set
```bash
nano ~/E-library/deploy/nginx-sanza.conf
# server_name yourdomain.com www.yourdomain.com;
```

### Step 9 — Setup script run
```bash
cd ~/E-library
bash deploy/setup.sh
```
Idhu pannum: packages install → venv → Postgres user/DB → migrate → collectstatic → gunicorn service → nginx → firewall.

Aprom:
```bash
source venv/bin/activate
python manage.py createsuperuser
```
`http://<ELASTIC_IP>` / `http://yourdomain.com` open pannina site theriyanum.

**HTTPS (Let's Encrypt):**
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```
Aprom `.env`-la `USE_HTTPS=True` set panni:
```bash
sudo systemctl restart gunicorn-sanza
```
Auto-renewal check: `sudo certbot renew --dry-run`

> Certbot nginx config-a edit pannumbodhu `proxy_set_header X-Forwarded-Proto $scheme;` line apdiye irukkanum — adhu thaan Django-ku request HTTPS-nu sollum.

### Step 10 — Google Login configure
**Google Cloud Console → APIs & Services → Credentials → OAuth client (Web)**
- Authorized JavaScript origins: `https://yourdomain.com`
- Authorized redirect URIs: `https://yourdomain.com/accounts/google/login/callback/`

**Django admin (`https://yourdomain.com/admin/`):**
1. **Sites → Sites** → `example.com`-a `yourdomain.com` ku maathunga (Domain name & Display name)
2. **Social applications → Add** → Provider: Google, Client ID & Secret podunga, **Chosen sites-la `yourdomain.com` move pannunga** → Save

> `settings.py` Google keys-a read pannala; adhanaala admin-la Social Application add pannanum (local DB-a restore pannina already irukkum).

### Step 11 — Razorpay
- `.env`-la `RAZORPAY_KEY_ID` / `RAZORPAY_KEY_SECRET` → **live keys** (go-live munnadi test keys vechi try pannunga)
- Dashboard-la website domain whitelist/settings check pannunga
- Test: oru ₹1–₹10 book vaangi payment success + order DB-la save aagudha paarunga

### Step 12 — Existing data migrate (optional)
**Database** (local Postgres-la already books/users irundha):
```bash
# local:
pg_dump -Fc -U <user> <dbname> > sanza.dump
scp -i sanza-key.pem sanza.dump ubuntu@<IP>:~/
# server:
cd ~/E-library && source venv/bin/activate
sudo -u postgres pg_restore --clean --if-exists --no-owner --role=<DB_USER> -d <DB_NAME> ~/sanza.dump
python manage.py migrate
```
**Media files** (zip-la `media/` folder illa — covers, author images, PDFs local-la irundha):
```bash
rsync -avz -e "ssh -i sanza-key.pem" media/ ubuntu@<IP>:~/E-library/media/
```
Books-a scratch-la load panna na: `python manage.py import_pdfs` (Gutenberg importer project-la irukku — command-a oru thadava `--help` paathu run pannunga).

---

## 5. Testing checklist
- [ ] Home page + CSS/images load aagudha (static)
- [ ] Book cover / category images theriyudha (media)
- [ ] Signup / login / logout
- [ ] Google login
- [ ] Free book PDF read aagudha (`/book/<id>/read/`)
- [ ] Paid book PDF URL direct-a `https://domain/media/books/xxx.pdf` → **404** varanum
- [ ] Razorpay payment → success page → book "My Library"-la
- [ ] Admin panel CSS sariya irukka (`/admin/`)
- [ ] Large PDF upload (author/admin add book) work aagudha (100 MB limit)
- [ ] Password reset email varudha (Gmail App Password)

---

## 6. Daily operations

```bash
# Code update
bash ~/E-library/deploy/update.sh

# Logs
sudo journalctl -u gunicorn-sanza -f          # Django/gunicorn errors
sudo tail -f /var/log/nginx/error.log

# Restart
sudo systemctl restart gunicorn-sanza
sudo systemctl reload nginx

# Status
sudo systemctl status gunicorn-sanza nginx postgresql

# Backup (cron: daily 2 AM)
crontab -e
0 2 * * * bash /home/ubuntu/E-library/deploy/backup.sh
```
Backups EC2 kulla thaan save aagum → weekly-a `~/backups`-a S3 / local machine-ku copy pannunga, illa EBS snapshot edunga.

---

## 7. Troubleshooting

| Symptom | Reason / Fix |
|---------|--------------|
| **502 Bad Gateway** | Gunicorn down. `journalctl -u gunicorn-sanza -n 50` paarunga. Usually `.env` missing key / DB connection |
| **400 Bad Request** | `ALLOWED_HOSTS`-la domain/IP illa |
| **CSRF verification failed** | `CSRF_TRUSTED_ORIGINS` (https://…) set pannala, or `X-Forwarded-Proto` header missing |
| **Static/CSS illa** | `collectstatic` run pannala / nginx alias path thappu / `sudo chmod 755 /home/ubuntu` |
| **Images 404** | `media/` upload pannala; nginx `/media/` alias check |
| **`ModuleNotFoundError: razorpay / import_export / PIL`** | `pip install -r requirements.txt` (venv active-a?) |
| **Google: redirect_uri_mismatch** | Console-la redirect URI exact-a `https://domain/accounts/google/login/callback/` |
| **Google: SocialApp.DoesNotExist** | Admin-la Social Application add pannala / Site-oda link pannala |
| **Google login HTTP callback use pannudhu** | `USE_HTTPS=True` + `SECURE_PROXY_SSL_HEADER` (settings-la irukku) |
| **Upload 413 error** | `client_max_body_size` nginx-la increase |
| **`password authentication failed`** | `.env` DB_PASSWORD ≠ Postgres user password |
| **Site slow / killed (OOM)** | Swap add pannunga, workers 2-a kuraikkunga, illa t3.small upgrade |

---

## 8. Security checklist
- [ ] **Secrets rotate:** zip-la `.env` irundhadhaala — Django `SECRET_KEY`, Razorpay secret, Google client secret, Gmail App Password, DB password ellaathaiyum pudhusa maathunga
- [ ] `.env` git-la commit aagala (`.gitignore`-la irukku ✔) — `git log --all -- .env` check pannunga
- [ ] `DEBUG=False`
- [ ] SSH (22) → My IP mattum; password login off (default off)
- [ ] 5432 public-a open illa
- [ ] `python manage.py check --deploy` warnings paarunga
- [ ] `sudo apt update && sudo apt upgrade` monthly
- [ ] Backups work aagudha (restore oru thadava test pannunga)

---

## 9. Next improvements (optional)
- **S3 for media** (`django-storages`) — EC2 disk-a depend pannaama, backup/scale easy
- **RDS PostgreSQL** — managed DB, auto backups
- **Amazon SES** — Gmail SMTP-ku better email limits
- **CloudFront** — static/media speed
- Error monitoring: Sentry


wZN3riAglIDAaW8IH0t3qHYNzjk20lE2uMxuo78TFmrA0uLw4hD2SBnwVe3HPz3rGII