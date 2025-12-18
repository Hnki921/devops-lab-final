# Quick Reference Guide - Execution Commands

## 🚀 One-Liner Quick Start

### Start Application Locally
```bash
npm install && npm start
# Access: http://localhost:8000
```

### Run All Tests
```bash
python selenium/test_todo_application.py
```

### Deploy to Kubernetes
```bash
kubectl apply -f kubernetes/
```

### Run Ansible Playbook
```bash
ansible-playbook -i ansible/hosts.ini ansible/playbook.yml -v
```

---

## 📋 Full Execution Sequence

### Phase 1: Local Testing (5 minutes)
```bash
# 1. Start application
npm install
npm start

# 2. In another terminal, run Selenium tests
cd selenium
python test_todo_application.py

# 3. Expected output
# ✓ [TEST 1 PASSED] Homepage loaded successfully
# ✓ [TEST 2 PASSED] Task created successfully
# ✓ [TEST 3 PASSED] All Tasks view verified
# ✓ [TEST 4 PASSED] Task completion works
# ✓ [TEST 5 PASSED] Frontend is responsive
# ✓ [TEST 6 PASSED] API connectivity verified
```

### Phase 2: AKS Deployment (20 minutes)
```bash
# 1. Check cluster creation status
az aks show --resource-group todo-rg --name todo-aks-cluster

# 2. Wait for provisioningState to be "Succeeded"
# (Already in progress! Started earlier)

# 3. Get credentials
az aks get-credentials --resource-group todo-rg --name todo-aks-cluster

# 4. Deploy application
kubectl apply -f kubernetes/

# 5. Wait for pods to be Running (2-3 minutes)
kubectl get pods -n todo-app

# 6. Get external IP addresses
kubectl get svc -n todo-app

# 7. Access application
# Open http://<EXTERNAL-IP> in browser

# 8. Verify deployment
bash kubernetes/verify-deployment.sh
```

### Phase 3: Ansible Configuration (20 minutes)
```bash
# 1. Update inventory with your server IPs
vim ansible/hosts.ini
# Change:
# web1 ansible_host=192.168.1.10
# web2 ansible_host=192.168.1.11
# db1 ansible_host=192.168.1.20

# 2. Syntax check
ansible-playbook -i ansible/hosts.ini ansible/playbook.yml --syntax-check

# 3. Dry run (preview changes)
ansible-playbook -i ansible/hosts.ini ansible/playbook.yml --check

# 4. Execute playbook
ansible-playbook -i ansible/hosts.ini ansible/playbook.yml -v

# 5. Verify services
ssh appuser@192.168.1.10
docker ps
node --version
nginx -t
systemctl status nginx
```

### Phase 4: Selenium Testing (5 minutes)
```bash
# 1. Install dependencies
pip install -r selenium/requirements.txt

# 2. Run tests
python selenium/test_todo_application.py -v

# 3. Generate HTML report
pytest selenium/test_todo_application.py -v --html=test_report.html --self-contained-html

# 4. View report
open test_report.html  # or use your browser
```

---

## 🔍 Monitoring & Verification Commands

### Kubernetes
```bash
# Get all resources
kubectl get all -n todo-app

# Get detailed pod status
kubectl get pods -n todo-app -o wide

# Get service IPs
kubectl get svc -n todo-app -o wide

# Get pod events
kubectl get events -n todo-app

# Check pod logs
kubectl logs -n todo-app <pod-name>

# Describe pod details
kubectl describe pod -n todo-app <pod-name>

# SSH into pod
kubectl exec -it -n todo-app <pod-name> -- /bin/bash

# Test connectivity
kubectl run -it --rm debug --image=curlimages/curl --restart=Never -- sh
# Inside: curl http://todo-backend-service:8000
```

### Ansible
```bash
# Check inventory
ansible all -i ansible/hosts.ini --list-hosts

# Ping all hosts
ansible all -i ansible/hosts.ini -m ping

# Check facts
ansible all -i ansible/hosts.ini -m setup | head -20

# Run ad-hoc command
ansible webservers -i ansible/hosts.ini -m shell -a "docker ps"

# Check playbook syntax
ansible-playbook -i ansible/hosts.ini ansible/playbook.yml --syntax-check

# Run specific role
ansible-playbook -i ansible/hosts.ini ansible/playbook.yml -t docker -v
```

### Docker
```bash
# Build images
docker build -f Dockerfile.backend -t todo-backend .
docker build -f Dockerfile.frontend -t todo-frontend .
docker build -f Dockerfile.database -t todo-database .

# Run containers
docker-compose up

# Check logs
docker logs <container-id>

# Execute command in container
docker exec -it <container-id> /bin/bash
```

---

## 📊 Testing Commands

### Selenium Tests
```bash
# Run all tests
python selenium/test_todo_application.py

# Run specific test
python -m pytest selenium/test_todo_application.py::TodoListApplicationTests::test_01_homepage_loads

# Run with pytest verbosity
pytest selenium/test_todo_application.py -vv

# Run in parallel
pytest selenium/test_todo_application.py -n 4

# Generate detailed report
pytest selenium/test_todo_application.py --html=report.html --self-contained-html -v

# Run with custom timeout
pytest selenium/test_todo_application.py --timeout=30
```

### Manual API Testing
```bash
# Test homepage
curl http://localhost:8000/

# Test API endpoint
curl http://localhost:8000/api/tasks

# Test with headers
curl -H "Content-Type: application/json" http://localhost:8000/api/tasks

# Test POST request
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"task":"Test Task","priority":"high"}'
```

---

## 🛠️ Troubleshooting Commands

### AKS Issues
```bash
# Check cluster status
az aks show --resource-group todo-rg --name todo-aks-cluster --query '{name:name, provisioningState:provisioningState}'

# Get cluster credentials (if lost)
az aks get-credentials --resource-group todo-rg --name todo-aks-cluster --overwrite-existing

# Check node status
kubectl get nodes

# Check resource quota
kubectl describe quota -n todo-app

# Check pod scheduling
kubectl describe pod -n todo-app <pod-name> | grep -A 5 "Events:"

# Delete and redeploy
kubectl delete -f kubernetes/
kubectl apply -f kubernetes/
```

### Ansible Issues
```bash
# Test SSH connection
ssh -v appuser@192.168.1.10

# Test with debug mode
ansible-playbook -i ansible/hosts.ini ansible/playbook.yml -vvv

# Gather facts
ansible webservers -i ansible/hosts.ini -m setup

# Check service status
ansible webservers -i ansible/hosts.ini -m service -a "name=docker state=started"

# Create backup of inventory
cp ansible/hosts.ini ansible/hosts.ini.backup
```

### Selenium Issues
```bash
# Check Chrome version
google-chrome --version

# Update ChromeDriver
python -m pip install --upgrade webdriver-manager

# Run with headless option removed (to see browser)
# Modify: options.add_argument('--headless')  # Comment this out

# Check browser logs
# In test, add: logs = driver.get_log('browser')

# Increase timeout
# Modify: WebDriverWait(driver, 20)  # Was 10
```

---

## 📁 File Location Reference

### Ansible
```
ansible/
├── hosts.ini              ← Update with your server IPs
└── playbook.yml           ← Run this

Command: ansible-playbook -i ansible/hosts.ini ansible/playbook.yml -v
```

### Kubernetes
```
kubernetes/
├── namespace.yaml         ← Creates namespace first
├── database.yaml          ← Then database
├── backend.yaml           ← Then backend
├── frontend.yaml          ← Then frontend
├── configmap.yaml         ← Configuration
└── verify-deployment.sh   ← Verification script

Commands:
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/
bash kubernetes/verify-deployment.sh
```

### Selenium
```
selenium/
├── test_todo_application.py    ← Test code (6 test cases)
├── setup.py                    ← Helper script
└── requirements.txt            ← Dependencies

Command: python selenium/test_todo_application.py
```

---

## ⏱️ Time Estimates

| Task | Time |
|------|------|
| Start application locally | 1 min |
| Run Selenium tests | 2 min |
| Create AKS cluster | 15 min |
| Deploy to AKS | 5 min |
| Verify AKS deployment | 2 min |
| Setup Ansible inventory | 2 min |
| Run Ansible playbook | 10 min |
| Verify Ansible setup | 2 min |
| Generate reports | 2 min |
| **Total** | **~45 minutes** |

---

## 🎯 Success Criteria

### Each section should show:

**Kubernetes (Section C):**
```
✓ All pods Running
✓ Services with External IPs
✓ Application accessible via browser
✓ Database connected and working
```

**Ansible (Section D):**
```
✓ Playbook execution: "PLAY RECAP" with 0 failed
✓ Docker installed and running
✓ Node.js installed (webservers)
✓ Nginx configured (webservers)
✓ MongoDB running (dbservers)
```

**Selenium (Section E):**
```
✓ All 6 tests passing
✓ Test execution summary: 6 Run, 6 Success, 0 Failures
✓ HTML report generated
```

---

## 📸 Screenshot Locations

Create a `screenshots/` folder for organized submission:

```
screenshots/
├── 01_kubernetes/
│   ├── cluster_creation.png
│   ├── pods_running.png
│   ├── services_external_ip.png
│   ├── app_accessible.png
│   └── verify_deployment.png
│
├── 02_ansible/
│   ├── playbook_start.png
│   ├── docker_install.png
│   ├── nodejs_install.png
│   ├── playbook_complete.png
│   └── verification.png
│
└── 03_selenium/
    ├── test_start.png
    ├── test_1_homepage.png
    ├── test_2_add_task.png
    ├── test_3_view_tasks.png
    ├── test_4_completion.png
    ├── test_5_responsiveness.png
    ├── test_6_api.png
    └── test_summary.png
```

---

## 💾 Backup & Recovery

### Backup before deployment
```bash
# Backup Kubernetes manifests
cp -r kubernetes kubernetes.backup

# Backup Ansible inventory
cp ansible/hosts.ini ansible/hosts.ini.backup

# Backup application
git tag -a v1.0 -m "Pre-deployment backup"
git push origin v1.0
```

### Rollback commands
```bash
# Rollback Kubernetes
kubectl rollout undo deployment/todo-backend -n todo-app
kubectl rollout undo deployment/todo-frontend -n todo-app

# Restore from git
git reset --hard HEAD~1
git push -f origin main

# Delete and restart
kubectl delete -f kubernetes/
kubectl apply -f kubernetes/
```

---

## 🔗 Useful Links

- Kubernetes Docs: https://kubernetes.io/docs/
- Ansible Docs: https://docs.ansible.com/
- Selenium Docs: https://www.selenium.dev/documentation/
- Azure AKS: https://docs.microsoft.com/en-us/azure/aks/
- GitHub Actions: https://docs.github.com/en/actions/

---

## ✅ Pre-Submission Checklist

- [ ] All services running and tested locally
- [ ] AKS cluster created and pods deployed
- [ ] Kubernetes verification script output captured
- [ ] Ansible playbook executed successfully on test servers
- [ ] All 6 Selenium tests passing
- [ ] HTML test report generated
- [ ] All screenshots collected
- [ ] Documentation complete and pushed to GitHub
- [ ] README updated with instructions
- [ ] Repository is public and accessible

---

*Last Updated: December 18, 2025*
*For support, refer to DEVOPS_PROJECT_SUMMARY.md and individual section documentation*
