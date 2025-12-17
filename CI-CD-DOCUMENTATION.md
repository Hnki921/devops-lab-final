# CI/CD Pipeline Documentation

## Overview
This project includes two CI/CD pipeline implementations:
1. **GitHub Actions** (`.github/workflows/ci-cd.yml`) - Recommended for GitHub repositories
2. **Jenkins** (`Jenkinsfile`) - For on-premise Jenkins servers

## Pipeline Architecture

### Task B1: Pipeline Stages

#### Stage 1: Build (Frontend + Backend)
- **Trigger**: On push or pull request
- **Actions**:
  - Checkout source code
  - Set up Node.js 18 environment
  - Install npm dependencies
  - Build frontend assets
  - Build backend application
  - Upload build artifacts

#### Stage 2: Automated Tests
- **Trigger**: After successful build
- **Actions**:
  - Start MongoDB service
  - Run unit tests
  - Run linting/code quality checks
  - Verify JavaScript syntax
  - Generate test reports

#### Stage 3: Docker Image Build and Push
- **Trigger**: On push to main/develop branches
- **Actions**:
  - Build backend Docker image
  - Build frontend Docker image
  - Build database Docker image
  - Push images to GitHub Container Registry (GHCR)
  - Tag images with build number and "latest"
  - Enable layer caching for faster builds

#### Stage 4: Deployment to Staging
- **Trigger**: On push to main branch only
- **Actions**:
  - Pull latest Docker images
  - Deploy using docker-compose
  - Run health checks
  - Verify all services are running
  - Send deployment notification

### Task B2: Trigger Configuration

#### GitHub Actions (`.github/workflows/ci-cd.yml`)
Runs automatically on:
```yaml
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
```

**What triggers the pipeline:**
- ✅ Push to `main` or `develop` branches
- ✅ Pull requests to `main` or `develop` branches
- ✅ Manual trigger (via GitHub UI)

#### Jenkins (`Jenkinsfile`)
Runs automatically on:
```groovy
triggers {
    githubPush()           // On GitHub webhook push
    pollSCM('H/5 * * * *') // Every 5 minutes
}
```

**What triggers the pipeline:**
- ✅ GitHub push events (via webhook)
- ✅ Poll SCM every 5 minutes
- ✅ Manual trigger (via Jenkins UI)

## Setup Instructions

### For GitHub Actions

1. **Push code to GitHub repository**
   ```bash
   git init
   git add .
   git commit -m "Add CI/CD pipeline"
   git push origin main
   ```

2. **The workflow file is automatically detected** at `.github/workflows/ci-cd.yml`

3. **View pipeline runs:**
   - Go to your GitHub repository
   - Click "Actions" tab
   - View all workflow runs and their status

4. **Pipeline secrets (optional):**
   - GitHub Actions automatically provides `GITHUB_TOKEN`
   - No additional secrets needed for basic setup

### For Jenkins

1. **Create a new Pipeline job in Jenkins**
   - Job name: `Todo-App-CI-CD`
   - Pipeline script from SCM: Git
   - Repository URL: Your GitHub repository URL
   - Branch: `*/main`
   - Script path: `Jenkinsfile`

2. **Configure GitHub webhook:**
   - GitHub repository → Settings → Webhooks
   - Payload URL: `http://jenkins-server:8080/github-webhook/`
   - Content type: `application/json`
   - Events: Push events

3. **Enable webhook trigger in Jenkins:**
   - Manage Jenkins → Configure System
   - GitHub → API URL: `https://api.github.com`
   - GitHub → Credentials: Add GitHub token

4. **View pipeline runs:**
   - Jenkins Dashboard → Click on job name
   - View build history and logs

## Pipeline Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ Trigger: Push to main/develop or Pull Request              │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
        ┌────────────────┐
        │ Stage 1: BUILD │ ← Build frontend & backend
        └────────┬───────┘
                 │
                 ▼
        ┌────────────────┐
        │ Stage 2: TEST  │ ← Run automated tests & linting
        └────────┬───────┘
                 │
                 ▼
    ┌────────────────────────────┐
    │ Stage 3: DOCKER BUILD      │ ← Build 3 Docker images
    │ & PUSH (main branch only)  │
    └────────┬───────────────────┘
             │
             ▼
    ┌────────────────────────────┐
    │ Stage 4: DEPLOY TO STAGING │ ← Deploy to staging env
    │ (main branch only)         │
    └────────┬───────────────────┘
             │
             ▼
        ┌─────────────┐
        │ ✅ SUCCESS  │
        └─────────────┘
```

## Environment Variables

### GitHub Actions
```yaml
REGISTRY: ghcr.io
IMAGE_NAME: ${{ github.repository }}
NODE_ENV: production
```

### Jenkins
```groovy
DOCKER_REGISTRY: docker.io
IMAGE_NAME: todo-app
NODE_ENV: production
DEPLOYMENT: staging
```

## Important Notes

1. **Docker Images**: Images are tagged with:
   - `latest` tag for current version
   - Branch name (e.g., `main`, `develop`)
   - Build number/commit SHA
   - Semantic versioning (if available)

2. **Deployment Strategy**:
   - Pull requests: Build and test only
   - Commits to `develop`: Build, test, and push images
   - Commits to `main`: Full pipeline including deployment to staging

3. **Testing**:
   - MongoDB service is automatically started during tests
   - Tests continue even if they fail (using `continue-on-error`)
   - Artifacts are archived for debugging

4. **Security**:
   - GitHub Token automatically provided in GitHub Actions
   - Docker images pushed to private registry (GHCR)
   - Only main branch deploys to production-like environments

## Monitoring & Logs

### GitHub Actions Logs
- View in GitHub repository → Actions tab
- Click on workflow run → Click on job
- View real-time logs as pipeline executes

### Jenkins Logs
- Jenkins Dashboard → Click job → Click build number
- View Console Output for full logs
- Logs are retained based on retention policy

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Pipeline not triggering | Check webhook configuration and branch rules |
| Docker push fails | Verify container registry credentials |
| Tests fail | Check MongoDB service health in logs |
| Deployment fails | Verify docker-compose.yml configuration |
| Build timeout | Increase timeout or optimize build steps |

## Future Enhancements

- [ ] Add SonarQube code quality analysis
- [ ] Add automated security scanning
- [ ] Add performance testing stage
- [ ] Deploy to Kubernetes instead of docker-compose
- [ ] Add approval gate for production deployment
- [ ] Add automated rollback on deployment failure
