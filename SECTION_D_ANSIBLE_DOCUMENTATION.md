# SECTION D: CONFIGURATION MANAGEMENT USING ANSIBLE

## Overview
Ansible is used to automate configuration and deployment of the Todo List application across multiple servers. This section demonstrates Infrastructure as Code (IaC) approach with configuration management.

## Files Included
- `hosts.ini` - Inventory file defining target servers
- `playbook.yml` - Main playbook with configuration tasks
- `setup.py` - Helper script for running playbooks

---

## Task D1: Inventory Setup

### File: `hosts.ini`

The inventory file defines the infrastructure:

```ini
[webservers]
web1 ansible_host=192.168.1.10 ansible_user=ubuntu ansible_password=password
web2 ansible_host=192.168.1.11 ansible_user=ubuntu ansible_password=password

[dbservers]
db1 ansible_host=192.168.1.20 ansible_user=ubuntu ansible_password=password
```

### Inventory Structure

**Groups:**
- `[webservers]` - Application servers (2 instances)
  - `web1` - Primary application server
  - `web2` - Secondary application server
  
- `[dbservers]` - Database servers (1 instance)
  - `db1` - MongoDB database server

### Variables Defined

**Global Variables:**
```
app_user=appuser          # Non-root application user
app_port=8000             # Application port
db_port=27017             # MongoDB port
node_version=18.x         # Node.js version
docker_compose_version=2.20.0
```

**Server-Specific Variables:**
```
[webservers:vars]
server_type=application
service_enabled=true

[dbservers:vars]
server_type=database
db_name=todo_db
db_user=todouser
db_password=todopass123
```

---

## Task D2: Playbook Execution

### File: `playbook.yml`

The playbook automates:

#### 1. **Common Setup (All Hosts)**
- System package updates
- Installation of basic utilities (git, vim, curl, etc.)
- Creation of application user with sudo access

**Commands:**
```bash
apt update && apt upgrade -y
apt install -y build-essential python3-pip git curl
```

#### 2. **Docker Installation (All Hosts)**
- Add Docker GPG key and repository
- Install Docker Engine, CLI, and Docker Compose
- Start Docker daemon
- Configure user permissions

**Installed Components:**
```
✓ Docker CE
✓ Docker CLI
✓ Containerd
✓ Docker Compose Plugin
✓ Docker Buildx
```

#### 3. **Node.js Installation (Webservers Only)**
- Add NodeSource repository
- Install Node.js 18.x and npm
- Install global packages: pm2, nodemon

**Global Packages:**
```
✓ PM2 - Process manager for Node.js
✓ Nodemon - Development utility
```

#### 4. **Nginx Installation (Webservers Only)**
- Install Nginx web server
- Configure reverse proxy to Node.js app
- Set up upstream proxy to port 8000
- Enable API routing with proper headers

**Nginx Configuration:**
```nginx
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

#### 5. **MongoDB Installation (Database Servers Only)**
- Add MongoDB repository and GPG key
- Install MongoDB 6.0
- Create database and admin user
- Bind MongoDB to all interfaces (0.0.0.0)

**MongoDB Setup:**
```javascript
use admin
db.createUser({
  user: "todouser",
  pwd: "todopass123",
  roles: [{role: "root", db: "admin"}]
})
use todo_db
db.createCollection("tasks")
```

#### 6. **Application Setup (Webservers)**
- Clone application repository
- Install Node.js dependencies
- Create `.env` configuration file
- Set up PM2 ecosystem configuration
- Create log directories

**.env Configuration:**
```
ENVIRONMENT=production
DEPLOYMENT=docker
DB_DEVELOPMENT=mongodb://todouser:todopass123@192.168.1.20:27017/todo_db
DB_PRODUCTION=mongodb://todouser:todopass123@192.168.1.20:27017/todo_db
PORT=8000
```

#### 7. **Firewall Configuration**
- Enable UFW firewall
- Allow SSH (port 22)
- Allow HTTP (port 80) on webservers
- Allow HTTPS (port 443) on webservers
- Allow MongoDB (27017) only from webservers

---

## Prerequisites

### 1. Install Ansible

**On Windows (WSL or Git Bash):**
```bash
sudo apt update
sudo apt install ansible
```

**On Mac:**
```bash
brew install ansible
```

**On Linux:**
```bash
sudo apt install ansible
```

### 2. Verify Installation
```bash
ansible --version
```

### 3. Set Up SSH Keys (Recommended)
Instead of using passwords, set up SSH keys:

```bash
# Generate SSH key
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa

# Copy to target servers
ssh-copy-id appuser@192.168.1.10
ssh-copy-id appuser@192.168.1.11
ssh-copy-id appuser@192.168.1.20
```

### 4. Update Inventory File
Modify `hosts.ini` with your actual server IPs and credentials:

```ini
[webservers]
web1 ansible_host=YOUR_WEB1_IP ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/id_rsa

[dbservers]
db1 ansible_host=YOUR_DB1_IP ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/id_rsa
```

---

## Running the Playbook

### 1. Syntax Check
```bash
ansible-playbook -i hosts.ini playbook.yml --syntax-check
```

### 2. Dry Run (No Changes)
```bash
ansible-playbook -i hosts.ini playbook.yml --check
```

### 3. Full Playbook Execution
```bash
ansible-playbook -i hosts.ini playbook.yml -v
```

### 4. Run Specific Tags
```bash
# Install only Docker
ansible-playbook -i hosts.ini playbook.yml -t docker

# Install only Node.js
ansible-playbook -i hosts.ini playbook.yml -t nodejs

# Install only MongoDB
ansible-playbook -i hosts.ini playbook.yml -t mongodb
```

### 5. Run for Specific Host Group
```bash
# Only on webservers
ansible-playbook -i hosts.ini playbook.yml -l webservers

# Only on database servers
ansible-playbook -i hosts.ini playbook.yml -l dbservers
```

---

## Expected Output

### Successful Playbook Execution

```
PLAY [Todo List Application - Complete Setup] **********

TASK [Update system packages] **********
ok: [web1]
ok: [web2]
ok: [db1]

TASK [Install basic packages] **********
changed: [web1]
changed: [web2]
changed: [db1]

TASK [Create application user] **********
changed: [web1]
changed: [web2]
changed: [db1]

...

TASK [Install Docker] **********
changed: [web1]
changed: [web2]
changed: [db1]

TASK [Start Docker service] **********
changed: [web1]
changed: [web2]
changed: [db1]

TASK [Install Node.js and npm] **********
changed: [web1]
changed: [web2]

TASK [Install Nginx] **********
changed: [web1]
changed: [web2]

TASK [Install MongoDB] **********
changed: [db1]

PLAY RECAP **********
web1 : ok=45 changed=35 unreachable=0 failed=0
web2 : ok=45 changed=35 unreachable=0 failed=0
db1  : ok=35 changed=25 unreachable=0 failed=0

============================================
TODO LIST APPLICATION - DEPLOYMENT COMPLETE
============================================
```

---

## Verification After Playbook

### 1. Verify Docker
```bash
# SSH to server
ssh appuser@192.168.1.10

# Check Docker
docker --version
docker-compose --version
docker ps
```

### 2. Verify Node.js
```bash
node --version
npm --version
pm2 list
```

### 3. Verify Nginx
```bash
sudo systemctl status nginx
nginx -t
curl http://localhost
```

### 4. Verify MongoDB (on db server)
```bash
sudo systemctl status mongod
mongosh -u todouser -p todopass123 --authenticationDatabase admin
```

### 5. Test Application Connectivity
```bash
# Test from webserver
curl http://192.168.1.20:27017

# Test Nginx reverse proxy
curl http://192.168.1.10
```

---

## Troubleshooting

### Issue: "Permission denied" when running playbook
**Solution:** Add `-u root` flag or ensure SSH user has sudo access

```bash
ansible-playbook -i hosts.ini playbook.yml -u root
```

### Issue: "Unable to locate package" error
**Solution:** Add apt cache update
```bash
ansible-playbook -i hosts.ini playbook.yml -t common
```

### Issue: Connection timeout
**Solution:** Verify network connectivity and firewall rules
```bash
ansible all -i hosts.ini -m ping
```

### Issue: MongoDB connection refused
**Solution:** Check MongoDB binding
```bash
ssh appuser@192.168.1.20
sudo grep bindIp /etc/mongod.conf
```

---

## Playbook Handlers

Handlers execute when tasks notify them:

```yaml
handlers:
  - name: Restart MongoDB
    service:
      name: mongod
      state: restarted
    listen: Restart MongoDB
```

---

## Best Practices Used

✓ Idempotent tasks (safe to run multiple times)
✓ Proper error handling with conditions
✓ Use of variables for customization
✓ Separation of concerns (webservers vs dbservers)
✓ Proper file permissions and ownership
✓ Service enablement for persistence
✓ Comprehensive logging and reporting
✓ Firewall configuration for security

---

## Deployment Summary

| Component | Webservers | Database Servers |
|-----------|-----------|-----------------|
| Docker | ✓ | ✓ |
| Docker Compose | ✓ | ✓ |
| Node.js 18.x | ✓ | - |
| Nginx (Reverse Proxy) | ✓ | - |
| MongoDB 6.0 | - | ✓ |
| UFW Firewall | ✓ | ✓ |
| PM2 (Process Manager) | ✓ | - |
| Python 3 | ✓ | ✓ |

---

## Scaling Considerations

To scale to more servers:

1. **Add to webservers group:**
   ```ini
   web3 ansible_host=192.168.1.12 ...
   web4 ansible_host=192.168.1.13 ...
   ```

2. **Add load balancer:**
   - Configure HAProxy or Azure Load Balancer
   - Point to multiple webservers

3. **Add more database replicas:**
   - Set up MongoDB replication
   - Create secondary database servers

---

## Security Notes

⚠️ **Warning:** The inventory file contains passwords. In production:

1. Use SSH keys instead of passwords
2. Store passwords in Ansible Vault
3. Use environment variables
4. Implement role-based access control

**Example with Vault:**
```bash
ansible-vault encrypt hosts.ini
ansible-playbook -i hosts.ini playbook.yml --ask-vault-pass
```

---

## Next Steps

1. ✅ Update `hosts.ini` with your server IPs
2. ✅ Configure SSH or password-based authentication
3. ✅ Run syntax check: `--syntax-check`
4. ✅ Run dry run: `--check`
5. ✅ Execute playbook: `-v` (verbose mode)
6. ✅ Verify all services are running
7. ✅ Take screenshots of successful execution

---

## Screenshots Required for Submission

1. **Playbook Execution Start**
   ```bash
   ansible-playbook -i hosts.ini playbook.yml -v
   ```
   Screenshot showing initial task execution

2. **Playbook Execution - Docker Installation**
   Screenshot showing Docker installation progress

3. **Playbook Execution - Node.js Installation** 
   Screenshot showing Node.js and npm installation

4. **Playbook Execution - MongoDB Setup**
   Screenshot showing MongoDB installation (dbservers only)

5. **Playbook Execution - Complete**
   Screenshot showing "PLAY RECAP" with all servers successful

6. **Verification - SSH Connection**
   ```bash
   ssh appuser@192.168.1.10
   docker ps
   ```
   Screenshot showing Docker containers running

7. **Verification - Service Status**
   ```bash
   systemctl status nginx
   systemctl status mongod (on db server)
   ```

---

## Additional Resources

- [Ansible Documentation](https://docs.ansible.com/)
- [Ansible Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html)
- [Ansible Modules](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/)
- [Docker Ansible Module](https://docs.ansible.com/ansible/latest/collections/community/docker/)

