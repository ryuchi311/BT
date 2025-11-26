# Quest Hub - Docker Deployment Guide

## Quick Start

### 1. Build and Run with Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

The app will be available at `http://localhost:5000`

### 2. Build Docker Image Only

```bash
# Build the image
docker build -t quest-hub .

# Run the container
docker run -p 5000:5000 quest-hub
```

## Environment Variables

Create a `.env` file in the project root:

```env
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-change-this

# Database Configuration (if using PostgreSQL)
DATABASE_URL=postgresql://questuser:questpass@db:5432/questdb

# Supabase Configuration (if using Supabase)
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
```

## Cloud Deployment

### Deploy to DigitalOcean/AWS/GCP

1. **Install Docker on your server**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker $USER
   ```

2. **Install Docker Compose**
   ```bash
   sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

3. **Clone your repository**
   ```bash
   git clone your-repo-url
   cd BT
   ```

4. **Set environment variables**
   ```bash
   nano .env
   # Add your production environment variables
   ```

5. **Run the application**
   ```bash
   docker-compose up -d
   ```

6. **Run database migrations**
   ```bash
   docker-compose exec web python scripts/migrations/migrate_sqlite.py
   ```

### Deploy to Heroku

1. **Install Heroku CLI**
   ```bash
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login and create app**
   ```bash
   heroku login
   heroku create your-app-name
   ```

3. **Add PostgreSQL addon**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

4. **Set environment variables**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set FLASK_ENV=production
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

6. **Run migrations**
   ```bash
   heroku run python scripts/migrations/migrate_sqlite.py
   ```

### Deploy to Railway

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and initialize**
   ```bash
   railway login
   railway init
   ```

3. **Add PostgreSQL**
   ```bash
   railway add postgresql
   ```

4. **Deploy**
   ```bash
   railway up
   ```

## Production Checklist

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Set `FLASK_ENV=production`
- [ ] Use PostgreSQL instead of SQLite for production
- [ ] Set up SSL/HTTPS (use nginx reverse proxy or cloud provider SSL)
- [ ] Configure domain name
- [ ] Set up database backups
- [ ] Configure logging
- [ ] Set up monitoring (e.g., Sentry, DataDog)
- [ ] Enable CORS if needed for Telegram Mini App
- [ ] Run database migrations
- [ ] Test all features in production environment

## Useful Commands

```bash
# View running containers
docker ps

# View logs
docker-compose logs -f web

# Restart services
docker-compose restart

# Execute command in container
docker-compose exec web python scripts/utils/add_test_youtube_quest.py

# Access database
docker-compose exec db psql -U questuser -d questdb

# Stop and remove everything
docker-compose down -v

# Rebuild after code changes
docker-compose up -d --build
```

## Nginx Reverse Proxy (Optional)

If you want to use Nginx as a reverse proxy:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Troubleshooting

**Container won't start:**
```bash
docker-compose logs web
```

**Database connection issues:**
```bash
docker-compose exec web python -c "from app import app; from models import db; app.app_context().push(); db.create_all()"
```

**Permission issues:**
```bash
sudo chown -R $USER:$USER .
```

## Scaling

To scale the web service:
```bash
docker-compose up -d --scale web=3
```

Add a load balancer (nginx) in front for production.
