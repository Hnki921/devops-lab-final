# Azure AKS Deployment Guide

## Section C: Kubernetes on Azure (AKS)

### Task C1: Kubernetes Manifests & Azure AKS Setup

#### Prerequisites
- Azure CLI installed (`az --version`)
- kubectl installed (`kubectl version --client`)
- Docker images pushed to Docker Hub
- Azure subscription with sufficient quota

---

## Step 1: Create Azure Kubernetes Service (AKS) Cluster

### 1a. Set Variables
```bash
RESOURCE_GROUP="todo-rg"
CLUSTER_NAME="todo-aks-cluster"
LOCATION="eastus"
NODE_COUNT=3
VM_SIZE="Standard_B2s"
```

### 1b. Create Resource Group
```bash
az group create \
  --name $RESOURCE_GROUP \
  --location $LOCATION
```

### 1c. Create AKS Cluster
```bash
az aks create \
  --resource-group $RESOURCE_GROUP \
  --name $CLUSTER_NAME \
  --node-count $NODE_COUNT \
  --vm-set-type VirtualMachineScaleSets \
  --load-balancer-sku standard \
  --enable-managed-identity \
  --network-plugin azure \
  --network-policy azure \
  --docker-bridge-address 172.17.0.1/16 \
  --service-cidr 10.0.0.0/16 \
  --dns-service-ip 10.0.0.10 \
  --vm-sku $VM_SIZE
```

**Estimated Time**: 10-15 minutes

### 1d. Get Cluster Credentials
```bash
az aks get-credentials \
  --resource-group $RESOURCE_GROUP \
  --name $CLUSTER_NAME
```

### 1e. Verify Cluster Connection
```bash
kubectl cluster-info
kubectl get nodes
```

---

## Step 2: Deploy Application to AKS

### 2a. Apply Kubernetes Manifests
```bash
# Deploy all manifests at once
kubectl apply -f kubernetes/

# Or deploy individually
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/configmap.yaml
kubectl apply -f kubernetes/database.yaml
kubectl apply -f kubernetes/backend.yaml
kubectl apply -f kubernetes/frontend.yaml
```

### 2b. Verify Deployment
```bash
# Run the verification script
chmod +x kubernetes/verify-deployment.sh
bash kubernetes/verify-deployment.sh
```

### 2c. Wait for LoadBalancer IPs
```bash
# Watch for external IPs to be assigned (takes 2-5 minutes)
kubectl get svc -n todo-app --watch
```

---

## Step 3: Expose Application with Public IP

### 3a. Get Service IPs
```bash
# Frontend Service
kubectl get svc todo-frontend-service -n todo-app

# Backend Service
kubectl get svc todo-backend-service -n todo-app
```

### 3b. Access the Application
```
Frontend URL: http://<FRONTEND_EXTERNAL_IP>
Backend API: http://<BACKEND_EXTERNAL_IP>
```

---

## Task C2: Deployment Verification Commands

### Check All Pods
```bash
# All pods in todo-app namespace
kubectl get pods -n todo-app -o wide

# Expected Output:
# NAME                             READY   STATUS    RESTARTS   AGE
# todo-backend-xxxxx               1/1     Running   0          5m
# todo-backend-xxxxx               1/1     Running   0          5m
# todo-frontend-xxxxx              1/1     Running   0          5m
# todo-frontend-xxxxx              1/1     Running   0          5m
# todo-database-xxxxx              1/1     Running   0          6m
```

### Check Services
```bash
# All services
kubectl get svc -n todo-app

# Expected Output:
# NAME                       TYPE           CLUSTER-IP    EXTERNAL-IP       PORT(S)
# todo-backend-service       LoadBalancer   10.0.1.100    20.XX.XX.XX       80:30000/TCP
# todo-frontend-service      LoadBalancer   10.0.1.101    20.YY.YY.YY       80:30001/TCP
# todo-database-service      ClusterIP      None          <none>            27017/TCP
```

### Check Pod Logs
```bash
# Backend logs
kubectl logs -n todo-app -l app=todo-backend --tail=50

# Frontend logs
kubectl logs -n todo-app -l app=todo-frontend --tail=50

# Database logs
kubectl logs -n todo-app -l app=todo-database --tail=50
```

### Check Deployment Status
```bash
# Detailed deployment info
kubectl describe deployment todo-backend -n todo-app
kubectl describe deployment todo-frontend -n todo-app
kubectl describe deployment todo-database -n todo-app
```

### Test Connectivity
```bash
# From your local machine, test frontend
curl http://<FRONTEND_EXTERNAL_IP>

# Test backend API
curl http://<BACKEND_EXTERNAL_IP>/
```

### Check Pod-to-Pod Communication
```bash
# Exec into a pod to test internal connectivity
kubectl exec -it <pod-name> -n todo-app -- /bin/sh

# Inside pod, test database connection
curl http://todo-database-service:27017/
```

---

## Troubleshooting

### Pod not running?
```bash
# Check pod status
kubectl describe pod <pod-name> -n todo-app

# Check events
kubectl get events -n todo-app --sort-by='.lastTimestamp'
```

### Image pull errors?
```bash
# Check image credentials
kubectl get secrets -n todo-app

# Verify Docker credentials in GitHub
```

### External IP stuck on "Pending"?
```bash
# Check service status
kubectl describe svc <service-name> -n todo-app

# Increase AKS node quota in Azure
az aks show --resource-group $RESOURCE_GROUP --name $CLUSTER_NAME
```

### Database connection issues?
```bash
# Test from backend pod
kubectl exec -it <backend-pod> -n todo-app -- curl todo-database-service:27017
```

---

## Cleanup (Optional)

### Delete Entire Cluster
```bash
az aks delete \
  --resource-group $RESOURCE_GROUP \
  --name $CLUSTER_NAME \
  --yes
```

### Delete Resource Group
```bash
az group delete \
  --resource-group $RESOURCE_GROUP \
  --yes
```

---

## Screenshots Required for Submission

1. **kubectl get pods -n todo-app**
   - Show all 5 pods in Running status

2. **kubectl get svc -n todo-app**
   - Show all services with External IPs

3. **Running Application**
   - Screenshot of frontend in browser at EXTERNAL-IP
   - Screenshot showing database connection working
   - Screenshot showing backend API working

4. **Logs**
   - Backend pod logs showing successful startup
   - Database logs showing initialization

---

## Submission Checklist

- [ ] All pods in Running state
- [ ] All services have External IPs assigned
- [ ] Frontend accessible via browser
- [ ] Backend API responding
- [ ] Database connected and working
- [ ] Screenshots of kubectl commands
- [ ] Screenshots of running application
- [ ] Deployment logs showing successful startup

---

**Total Marks Available**: 12 marks
- Cluster creation & setup: 4 marks
- Manifests & deployment: 4 marks
- Verification & accessibility: 4 marks
