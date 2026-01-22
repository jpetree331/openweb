# Deploying OpenWebUI to Railway

Step-by-step guide to deploy OpenWebUI to Railway.

## Prerequisites

- A GitHub account
- This project pushed to a GitHub repository
- A Railway account (free tier available)

## Step 1: Push to GitHub

If you haven't already, push this project to GitHub:

```powershell
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit: OpenWebUI project"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

## Step 2: Sign Up for Railway

1. Go to [railway.app](https://railway.app)
2. Click **"Start a New Project"** or **"Login"**
3. Sign up with GitHub (recommended - makes deployment easier)

## Step 3: Deploy from GitHub

1. In Railway dashboard, click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Authorize Railway to access your GitHub repositories (if prompted)
4. Select your repository containing this OpenWebUI project
5. Railway will automatically:
   - Detect the `Dockerfile`
   - Start building your application
   - Deploy it

## Step 4: Configure Environment Variables (Optional)

1. In your Railway project dashboard, go to the **Variables** tab
2. Add any environment variables you need:

   - `DATA_DIR` (optional): `/app/data` (default)
   - `WEBUI_SECRET_KEY` (optional): Generate a random secret key for sessions
   - `OPENAI_API_KEY` (optional): If you want to connect to OpenAI
   - `OLLAMA_BASE_URL` (optional): If you want to connect to an Ollama instance

   To generate a secret key:
   ```powershell
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

## Step 5: Get Your Public URL

1. Once deployment completes, Railway will provide a public URL
2. Click on your service → **Settings** → **Generate Domain**
3. Your OpenWebUI will be available at: `https://your-app-name.railway.app`

## Step 6: Access OpenWebUI

1. Open the Railway-provided URL in your browser
2. You should see the OpenWebUI login/registration page
3. Create your first admin account

## Railway-Specific Features

### Persistent Storage

Railway automatically provides persistent storage. The `DATA_DIR` is set to `/app/data` in the Dockerfile, which persists across deployments.

### Custom Domain

1. Go to your service → **Settings** → **Networking**
2. Click **"Generate Domain"** or add a custom domain
3. Railway provides free SSL certificates automatically

### Monitoring

- View logs in real-time in the Railway dashboard
- Check deployment status and build logs
- Monitor resource usage

### Scaling

- Railway automatically handles scaling
- Free tier includes $5 credit monthly
- Pay only for what you use after that

## Troubleshooting

### Build Fails

1. Check the build logs in Railway dashboard
2. Ensure Python 3.11 is being used (check Dockerfile)
3. Verify all files are committed to GitHub

### Port Issues

The Dockerfile is configured to use Railway's `$PORT` environment variable automatically. If you see port errors:
- Check that the Dockerfile CMD uses `${PORT:-8080}`
- Railway sets `$PORT` automatically - no action needed

### Application Not Starting

1. Check the service logs in Railway dashboard
2. Look for error messages
3. Verify environment variables are set correctly

### Data Not Persisting

- Railway volumes persist automatically
- Ensure `DATA_DIR` is set to `/app/data` (default in Dockerfile)
- Check that the data directory is being created in the container

## Updating Your Deployment

To update OpenWebUI:

1. Push changes to GitHub:
   ```powershell
   git add .
   git commit -m "Update OpenWebUI"
   git push
   ```

2. Railway will automatically detect the push and redeploy

Or manually trigger a redeploy:
- Go to Railway dashboard → Your service → **Deployments** → **Redeploy**

## Cost

- **Free Tier**: $5 credit per month
- **After Free Credit**: Pay-as-you-go pricing
- OpenWebUI is lightweight - should stay within free tier for personal use

## Support

- [Railway Documentation](https://docs.railway.app/)
- [Railway Discord](https://discord.gg/railway)
- [OpenWebUI Documentation](https://docs.openwebui.com/)

## Quick Commands (Railway CLI - Optional)

If you prefer using the CLI:

```powershell
# Install Railway CLI
powershell -c "irm https://railway.app/install.ps1 | iex"

# Login
railway login

# Link to your project
railway link

# Deploy
railway up

# View logs
railway logs

# Open in browser
railway open
```
