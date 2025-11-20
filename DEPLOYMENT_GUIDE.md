# Deployment Configuration for Railway/Heroku

# This file helps configure your deployment
# Copy the relevant section to your platform

## Railway Configuration
# Railway auto-detects Python apps
# Just connect your GitHub repo and deploy!

## Heroku Configuration (if using Heroku)
# Make sure these files exist:
# - Procfile (already exists)
# - runtime.txt (already exists)
# - requirements.txt (already exists)

## Environment Variables (set in your hosting platform)

# Optional: Set Python version
PYTHON_VERSION=3.11

# Optional: Set port (most platforms auto-configure)
PORT=5000

# Optional: Disable debug mode in production
FLASK_ENV=production
FLASK_DEBUG=0

## Post-Deployment Checklist

After deploying, verify:
1. [ ] App URL is accessible via HTTPS
2. [ ] Home page loads correctly
3. [ ] Image upload works
4. [ ] ML model predictions work
5. [ ] Blockchain verification works
6. [ ] /static/manifest.json is accessible
7. [ ] /.well-known/assetlinks.json is accessible

## Update These Files After Deployment

1. Update twa-manifest.json:
   - Replace "your-domain.com" with your actual domain
   - Update all URLs

2. Update .well-known/assetlinks.json:
   - Replace "https://your-domain.com" with your actual domain

3. Test the PWA:
   - Visit your site in Chrome mobile
   - Check for "Install app" prompt
   - Install and test

## Railway Deployment Steps

1. Sign up at https://railway.app/
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Authorize GitHub and select this repository
5. Railway will auto-detect Python and deploy
6. Copy your deployment URL
7. Update twa-manifest.json with your URL
8. Redeploy if needed

## Heroku Deployment Steps

```powershell
# Install Heroku CLI
# Download from: https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create fruit-classifier-app

# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit"

# Deploy
git push heroku main

# View logs
heroku logs --tail

# Open app
heroku open
```

## Render Deployment Steps

1. Sign up at https://render.com/
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - Name: fruit-classifier
   - Environment: Python 3
   - Build Command: pip install -r requirements.txt
   - Start Command: python app.py
5. Deploy

## Testing Your Deployment

```powershell
# Test endpoints
curl https://your-domain.com/
curl https://your-domain.com/static/manifest.json
curl https://your-domain.com/.well-known/assetlinks.json

# Test with browser
# Open: https://your-domain.com
# Check: Chrome DevTools → Application → Manifest
# Should see your app manifest with icons
```

## SSL/HTTPS Verification

All platforms (Railway, Heroku, Render) provide automatic HTTPS.
Verify with:
- Visit https://your-domain.com (should load securely)
- Check browser address bar for lock icon
- Test in Chrome DevTools → Security tab

## Domain Configuration (Optional)

If you have a custom domain:

1. Add custom domain in your platform dashboard
2. Update DNS records as instructed
3. Wait for SSL certificate provisioning (automatic)
4. Update twa-manifest.json with custom domain
5. Update assetlinks.json with custom domain

## Troubleshooting Deployment

### App not starting
- Check logs: `heroku logs --tail` or Railway dashboard
- Verify all dependencies in requirements.txt
- Check Python version compatibility

### Model not loading
- Ensure fruit_freshness_model.h5 is committed to git
- Check file size limits (Heroku: 300MB slug limit)
- Verify TensorFlow is installed

### Static files not serving
- Check Flask static folder configuration
- Verify file paths are correct
- Test manifest.json URL directly

### Build fails
- Check requirements.txt syntax
- Verify Python version in runtime.txt
- Check build logs for errors

## Performance Optimization

Add these to your deployment:

1. Enable gzip compression
2. Use CDN for static files (optional)
3. Configure caching headers
4. Monitor with platform analytics

## Security Checklist

- [ ] Disable Flask debug mode in production
- [ ] Use environment variables for secrets
- [ ] Keep dependencies updated
- [ ] Monitor error logs
- [ ] Set up CORS if needed
- [ ] Configure CSP headers (if needed)

## Monitoring

After deployment, monitor:
- Response times
- Error rates
- Model prediction accuracy
- Blockchain verification success
- User engagement

Most platforms provide built-in monitoring dashboards.
