#!/bin/bash

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Todo Application Kubernetes Verification ===${NC}\n"

# Check namespace
echo -e "${YELLOW}1. Checking Namespace...${NC}"
kubectl get namespace todo-app
echo ""

# Check pods
echo -e "${YELLOW}2. Checking Pods Status...${NC}"
kubectl get pods -n todo-app -o wide
echo ""

# Check services
echo -e "${YELLOW}3. Checking Services...${NC}"
kubectl get svc -n todo-app -o wide
echo ""

# Check deployments
echo -e "${YELLOW}4. Checking Deployments...${NC}"
kubectl get deployments -n todo-app -o wide
echo ""

# Check PVC
echo -e "${YELLOW}5. Checking Persistent Volume Claims...${NC}"
kubectl get pvc -n todo-app
echo ""

# Get frontend external IP
echo -e "${YELLOW}6. Frontend Service Details:${NC}"
FRONTEND_IP=$(kubectl get svc todo-frontend-service -n todo-app -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
FRONTEND_HOSTNAME=$(kubectl get svc todo-frontend-service -n todo-app -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

if [ -z "$FRONTEND_IP" ] && [ -z "$FRONTEND_HOSTNAME" ]; then
    echo -e "${YELLOW}Frontend External IP/Hostname: Pending (may take a few minutes)${NC}"
else
    echo -e "${GREEN}Frontend URL: http://${FRONTEND_IP:-$FRONTEND_HOSTNAME}${NC}"
fi
echo ""

# Get backend external IP
echo -e "${YELLOW}7. Backend Service Details:${NC}"
BACKEND_IP=$(kubectl get svc todo-backend-service -n todo-app -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
BACKEND_HOSTNAME=$(kubectl get svc todo-backend-service -n todo-app -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

if [ -z "$BACKEND_IP" ] && [ -z "$BACKEND_HOSTNAME" ]; then
    echo -e "${YELLOW}Backend External IP/Hostname: Pending (may take a few minutes)${NC}"
else
    echo -e "${GREEN}Backend URL: http://${BACKEND_IP:-$BACKEND_HOSTNAME}${NC}"
fi
echo ""

# Check pod logs
echo -e "${YELLOW}8. Recent Pod Logs (Backend):${NC}"
kubectl logs -n todo-app -l app=todo-backend --tail=10 --all-containers=true 2>/dev/null || echo "No logs available yet"
echo ""

# Check events
echo -e "${YELLOW}9. Recent Events:${NC}"
kubectl get events -n todo-app --sort-by='.lastTimestamp' | tail -10
echo ""

echo -e "${GREEN}=== Verification Complete ===${NC}"
