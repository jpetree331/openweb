# Deploying OpenWebUI to Cloud Platforms

Since local hosting isn't possible due to firewall restrictions, here are several cloud deployment options for OpenWebUI.

## ⚠️ Important Note

**Netlify is NOT suitable** for OpenWebUI because it only hosts static sites. OpenWebUI requires a full Python backend server.

## Recommended Platforms

### 1. Railway (Recommended - Easiest)

Railway is great for Python applications and supports Docker deployments.

#### Steps:

1. **Sign up** at [railway.app](https://railway.app) (free tier available)

2. **Install Railway CLI** (optional, but helpful):
   ```powershell
   powershell -c "irm https://railway.app/install.ps1 | iex"
   ```

3. **Deploy via GitHub** (easiest method):
   - Push this project to GitHub
   - Go to Railway dashboard → New Project → Deploy from GitHub
   - Select this repository
   - Railway will automatically detect the Dockerfile and deploy

4. **Deploy via CLI**:
   ```powershell
   railway login
   railway init
   railway up
   ```

5. **Set Environment Variables** (if needed):
   - In Railway dashboard → Variables tab
   - Add any required OpenWebUI environment variables

6. **Get your URL**:
   - Railway will provide a public URL like `https://your-app.railway.app`
   - OpenWebUI will be accessible at this URL

#### Railway Configuration:
- Uses the `Dockerfile` in this repo
- Automatically handles port binding via `$PORT` environment variable
- Provides persistent storage for data directory

---

### 2. Render (Good Alternative)

Render offers free tier hosting for web services.

#### Steps:

1. **Sign up** at [render.com](https://render.com) (free tier available)

2. **Deploy via GitHub**:
   - Push this project to GitHub
   - Go to Render dashboard → New → Web Service
   - Connect your GitHub repository
   - Render will auto-detect the `render.yaml` configuration

3. **Manual Configuration** (if not using render.yaml):
   - **Build Command**: `pip install open-webui`
   - **Start Command**: `open-webui serve --host 0.0.0.0 --port $PORT`
   - **Environment**: Python 3
   - **Plan**: Free (or paid for more resources)

4. **Add Persistent Disk** (for data storage):
   - In Render dashboard → Settings → Persistent Disk
   - Mount at `/opt/render/project/src/data`
   - Set `DATA_DIR` environment variable to this path

5. **Get your URL**:
   - Render provides: `https://your-app.onrender.com`
   - Note: Free tier services spin down after 15 minutes of inactivity

---

### 3. Fly.io (Another Option)

Fly.io offers global deployment with good performance.

#### Steps:

1. **Install Fly CLI**:
   ```powershell
   powershell -c "irm https://fly.io/install.ps1 | iex"
   ```

2. **Create fly.toml** (already created in this repo):
   ```toml
   app = "your-app-name"
   primary_region = "iad"

   [build]
     dockerfile = "Dockerfile"

   [[services]]
     internal_port = 8080
     protocol = "tcp"
   ```

3. **Deploy**:
   ```powershell
   fly auth login
   fly launch
   fly deploy
   ```

---

### 4. Northflank (One-Click Deployment)

Northflank has a dedicated OpenWebUI template for one-click deployment.

#### Steps:

1. **Sign up** at [northflank.com](https://northflank.com)

2. **Use OpenWebUI Template**:
   - Go to Templates → Open WebUI
   - Click "Deploy"
   - Configure environment variables
   - Deploy

3. **Get your URL**:
   - Northflank provides a public URL automatically

---

## Environment Variables

You may want to set these in your cloud platform's dashboard:

- `DATA_DIR`: Path for persistent data storage (usually `/app/data` or similar)
- `WEBUI_SECRET_KEY`: Secret key for session management (generate a random string)
- `OPENAI_API_KEY`: If connecting to OpenAI API
- `OLLAMA_BASE_URL`: If connecting to Ollama instance

## Important Considerations

### Port Configuration
- Most platforms set a `$PORT` environment variable
- OpenWebUI defaults to port 8080
- Update the start command to use `$PORT` if your platform requires it

### Persistent Storage
- OpenWebUI needs persistent storage for user data, conversations, etc.
- Configure a volume/disk in your platform's settings
- Set `DATA_DIR` environment variable to the mounted path

### WebSocket Support
- OpenWebUI requires WebSocket support
- All recommended platforms (Railway, Render, Fly.io) support WebSockets

### Free Tier Limitations
- **Railway**: $5 free credit monthly, then pay-as-you-go
- **Render**: Free tier available, but services spin down after inactivity
- **Fly.io**: Free tier with limited resources
- **Northflank**: Check their pricing

## Quick Start Commands

### Railway
```powershell
railway login
railway init
railway up
```

### Render
Just connect your GitHub repo and Render handles the rest!

### Fly.io
```powershell
fly launch
fly deploy
```

## Troubleshooting

### Port Issues
If you get port binding errors, ensure your start command uses the platform's `$PORT` variable:
```bash
open-webui serve --host 0.0.0.0 --port $PORT
```

### Data Persistence
Make sure you've configured persistent storage and set the `DATA_DIR` environment variable correctly.

### Build Failures
- Ensure Python 3.11 or 3.12 is specified (not 3.13)
- Check that all dependencies in `pyproject.toml` are correct

## Need Help?

- [OpenWebUI Documentation](https://docs.openwebui.com/)
- [Railway Docs](https://docs.railway.app/)
- [Render Docs](https://render.com/docs)
- [Fly.io Docs](https://fly.io/docs/)
