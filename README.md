# CI/CD Pipeline Implementation and Deployment of Guitar Tuner Application

**Course:** TYCSE · Cloud Computing and DevOps  
**Assignment:** CCA 2 – Automated CI/CD Pipeline & Minikube Deployment  
**Total Marks:** 10 Marks  

---

## 1. Project Overview

This repository contains the complete source code, automated test suite, Docker container configuration, Kubernetes manifests, and Jenkins declarative pipeline for a **Precision Guitar Tuner Web Application**.

### Key Highlights:
- **Application:** Python 3.10 + Flask + Gunicorn WSGI server.
- **Frontend Engine:** Interactive 6-string tuner utilizing the browser's Web Audio API for synthesis of exact standard guitar frequencies ($E_2, A_2, D_3, G_3, B_3, E_4$).
- **Automated Testing:** `pytest` test suite verifying HTTP endpoints and audio frequency calculations.
- **CI/CD Orchestration:** Jenkins declarative pipeline running on an AWS EC2 instance.
- **Container Registry:** Docker Hub.
- **Container Orchestration:** Local Kubernetes cluster managed with Minikube.

---

## 2. Repository Structure

```
├── app.py                     # Flask application & REST endpoints
├── requirements.txt           # Python dependencies (Flask, Gunicorn, Pytest)
├── Dockerfile                 # Production container definition (python:3.10-slim)
├── .dockerignore              # Excluded files for clean Docker context
├── .gitignore                 # Excluded files for Git version control
├── Jenkinsfile                # 6-Stage Declarative CI/CD Pipeline
├── templates/
│   └── index.html             # Responsive guitar tuner user interface
├── static/
│   ├── css/
│   │   └── style.css          # Dark-theme styles, meter gauge, visualizer
│   └── js/
│       └── tuner.js           # Web Audio API audio synthesis & controls
├── tests/
│   ├── __init__.py
│   └── test_app.py            # Automated unit tests for Jenkins Build/Test stage
├── k8s/
│   ├── deployment.yaml        # K8s Deployment (2 replicas, rolling updates, probes)
│   └── service.yaml           # K8s NodePort Service (Port 30080)
└── README.md                  # Complete documentation and viva guide
```

---

## 3. Pipeline Stages (Jenkinsfile)

| Stage # | Stage Name | Action Performed |
|:---|:---|:---|
| **1** | **Checkout** | Clones/pulls the latest source code from the GitHub repository. |
| **2** | **Build and Test** | Creates a Python virtual environment, installs dependencies, and runs `pytest` automated tests. |
| **3** | **Docker Build** | Builds the Docker image tagged with `${BUILD_NUMBER}` and `latest`. |
| **4** | **Push Image** | Authenticates securely with Docker Hub using Jenkins credentials and pushes both tags. |
| **5** | **Minikube Deployment** | Applies `deployment.yaml` and `service.yaml`, and rolls out the new image. |
| **6** | **Verification** | Asserts rollout completion (`kubectl rollout status`), lists pods/services, and verifies health check `/api/health`. |

---

## 4. Setup Guide: AWS EC2, Jenkins, Docker & Minikube

### Step 4.1: Launch AWS EC2 Instance
- **AMI:** Ubuntu Server 22.04 LTS (HVM), SSD Volume Type
- **Instance Type:** `t3.medium` (2 vCPU, 4 GiB Memory) or `t3.large` (2 vCPU, 8 GiB Memory) *(Required for running Jenkins, Docker, and Minikube concurrently)*
- **Storage:** 25 GB to 30 GB gp3
- **Security Group Inbound Rules:**
  - `SSH` (Port 22) from your IP
  - `Custom TCP` (Port 8080) from Anywhere (Jenkins UI)
  - `Custom TCP` (Port 30080) from Anywhere (Guitar Tuner NodePort Service)
  - `HTTP` (Port 80) / `Custom TCP` (Port 3000)

### Step 4.2: Install Docker, Jenkins & Minikube on EC2
Connect to your EC2 instance via SSH and run the following commands:

```bash
# 1. Update system packages
sudo apt update && sudo apt upgrade -y

# 2. Install Java (required for Jenkins)
sudo apt install -y openjdk-17-jre python3-pip python3-venv

# 3. Install Docker Engine
sudo apt install -y ca-certificates curl gnupg lsb-release
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 4. Install Jenkins
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt update
sudo apt install -y jenkins

# 5. Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# 6. Install Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
rm minikube-linux-amd64

# 7. Configure Permissions for Docker and Jenkins
sudo usermod -aG docker ubuntu
sudo usermod -aG docker jenkins
sudo systemctl restart docker
sudo systemctl restart jenkins
```

### Step 4.3: Start Minikube & Configure for Jenkins
Run as the `ubuntu` user:
```bash
# Start Minikube using Docker driver
minikube start --driver=docker --cpus=2 --memory=2500mb

# Grant the 'jenkins' user access to Minikube's kubeconfig
sudo mkdir -p /var/lib/jenkins/.kube
sudo cp ~/.kube/config /var/lib/jenkins/.kube/config
sudo cp -r ~/.minikube /var/lib/jenkins/
sudo chown -R jenkins:jenkins /var/lib/jenkins/.kube /var/lib/jenkins/.minikube
```

### Step 4.4: Setup Jenkins Web UI & Credentials
1. Open your browser and navigate to: `http://<EC2_PUBLIC_IP>:8080`.
2. Retrieve the initial admin password on EC2:
   ```bash
   sudo cat /var/lib/jenkins/secrets/initialAdminPassword
   ```
3. Install **Suggested Plugins**.
4. Install additional plugins under **Manage Jenkins > Plugins**:
   - `Docker Pipeline`
   - `Pipeline: Stage View`
5. Configure Credentials under **Manage Jenkins > Credentials > System > Global credentials**:
   - **Credential 1 (Docker Hub login):**
     - Kind: `Username with password`
     - ID: `dockerhub-credentials`
     - Username: Your Docker Hub username
     - Password: Your Docker Hub Personal Access Token (or password)
   - **Credential 2 (Docker Hub username string):**
     - Kind: `Secret text`
     - ID: `DOCKER_HUB_USERNAME`
     - Secret: Your Docker Hub username

---

## 5. Setting up Git & Connecting to GitHub

From your local project folder:

```bash
# 1. Initialize local repository (already done)
git branch -M main

# 2. Add remote GitHub repository
git remote add origin https://github.com/shreyanskota/guitartuner.git

# 3. Push to GitHub
git push -u origin main
```

---

## 6. Creating and Running the Jenkins Pipeline

1. In Jenkins dashboard, click **New Item**.
2. Enter item name (e.g., `guitar-tuner-cicd`), select **Pipeline**, and click **OK**.
3. Under **Pipeline Configuration**:
   - Definition: `Pipeline script from SCM`
   - SCM: `Git`
   - Repository URL: `https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPO_NAME>.git`
   - Branch Specifier: `*/main`
   - Script Path: `Jenkinsfile`
4. Click **Save**.
5. Click **Build Now** to trigger the first run!

---

## 7. Two-Phase Demonstration: Source Code Change (v1 to v2)

To satisfy **Rubric Requirement #9** (Demonstrate a source-code change and run the pipeline again):

### Step 7.1: Verify Version 1.0.0
- Jenkins pipeline completes Stage 1 through Stage 6 successfully.
- Access the running app:
  ```bash
  # Inside EC2 terminal:
  curl http://$(minikube ip):30080/api/version
  ```
  Output: `{"appName":"Guitar Tuner","version":"1.0.0",...}`

### Step 7.2: Make a Code Change for Version 2.0.0
In `app.py`:
```python
# Change APP_VERSION from 1.0.0 to 2.0.0
APP_VERSION = "2.0.0"
APP_THEME = "electric-purple"
```
Or in `templates/index.html`:
```html
<p class="subtitle">Standard Tuning · E2 A2 D3 G3 B3 E4 · Version 2.0.0 Updated</p>
```

### Step 7.3: Commit and Push
```bash
git add app.py templates/index.html
git commit -m "feat: update to release v2.0.0 with electric theme"
git push origin main
```

### Step 7.4: Trigger Pipeline & Verify Zero-Downtime Rollout
1. Click **Build Now** in Jenkins (or configure GitHub webhook for automatic trigger).
2. Observe Jenkins stages:
   - Pytest runs on v2.
   - New Docker image `yourusername/guitar-tuner:2` is built and pushed to Docker Hub.
   - Kubernetes executes a rolling update (`kubectl set image`).
3. Verify live pods transitioning without downtime:
   ```bash
   kubectl get pods -l app=guitar-tuner -w
   curl http://$(minikube ip):30080/api/version
   ```
   Output: `{"appName":"Guitar Tuner","version":"2.0.0",...}`

---

## 8. Verification Commands Cheatsheet

```bash
# Check Pods
kubectl get pods -l app=guitar-tuner -o wide

# Check Deployment and Rollout History
kubectl get deployment guitar-tuner
kubectl rollout history deployment/guitar-tuner

# Check Service & Port
kubectl get service guitar-tuner-service

# Get Minikube Service URL
minikube service guitar-tuner-service --url

# Port-forward to EC2 external interface if needed:
kubectl port-forward --address 0.0.0.0 service/guitar-tuner-service 30080:3000
```

---

## 9. Viva Questions & Key Explanations (1.5 Marks)

1. **Why use a multi-stage or slim Docker base image?**  
   *Answer:* `python:3.10-slim` minimizes image size (~120MB vs ~1GB full Python), reducing build/pull times and removing unnecessary build tools to reduce security attack surfaces.

2. **How does the Kubernetes RollingUpdate strategy prevent downtime?**  
   *Answer:* Configured with `maxSurge: 1` and `maxUnavailable: 0`. Kubernetes starts a new v2 pod, waits until its `readinessProbe` succeeds on `/api/health`, and only then terminates a v1 pod.

3. **Why are liveness and readiness probes necessary?**  
   *Answer:* Readiness probe ensures traffic is only routed to pods that have completed startup. Liveness probe detects frozen processes and restarts unhealthy pods automatically.

4. **How are secrets managed securely in the pipeline?**  
   *Answer:* Docker Hub credentials are never hardcoded. They are stored encrypted in the Jenkins Credential Store and injected into the pipeline dynamically using `withCredentials()`.
