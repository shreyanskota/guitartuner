# 🎸 DevOps & CI/CD Quick Viva Revision Guide (10/10 Marks)
**Course:** TYCSE · Cloud Computing & DevOps (CCA 2)  
**Project:** Precision Guitar Tuner Automated CI/CD Pipeline  

---

## 1. The 30-Second Summary (Explain Your Project Like This)

> *"In this project, I built a lightweight **Precision Guitar Tuner web app** in Python Flask and implemented a fully automated **CI/CD delivery pipeline** on an AWS EC2 Ubuntu instance using **Jenkins**, **Docker**, **Docker Hub**, and **Minikube (Kubernetes)**.*  
> *Whenever code is pushed to GitHub, Jenkins automatically tests the code with `pytest`, packages it into a lightweight Docker image, pushes it to Docker Hub using stored credentials, and performs a zero-downtime rolling deployment to Minikube with liveness and readiness health checks."*

---

## 2. Simple Analogies (To Understand the Basics Instantly)

| Tool | Real-World Analogy | What It Does In Your Project |
|:---|:---|:---|
| **Code (`app.py`)** | **The Cooking Recipe** | Python web app that calculates guitar string frequencies and generates reference pitches. |
| **GitHub** | **The Master Recipe Book** | Cloud repository storing our source code, Dockerfile, Jenkinsfile, and Kubernetes YAMLs. |
| **Jenkins** | **The Automated Factory Conveyor Belt** | The robot that triggers whenever code changes, runs tests, builds the container, and deploys it. |
| **Docker** | **The Standard Sealed Shipping Container** | Packages Python, dependencies, and code together so it runs identically on any computer. *(No "it works on my machine" excuses).* |
| **Docker Hub** | **The Central Warehouse** | Stores and distributes our packaged Docker images (`shreyanskota/guitar-tuner`) in the cloud. |
| **Kubernetes (Minikube)**| **The Restaurant Floor Manager** | Manages our containers. Runs 2 replicas (copies), monitors their health, restarts them if they crash, and updates them without downtime. |
| **AWS EC2** | **The Rented Office Space** | The cloud server in Mumbai (`3.111.33.220`) where Jenkins, Docker, and Minikube live. |

---

## 3. The 6 Pipeline Stages (Memorize This Flow)

```
[1. Checkout] ➔ [2. Build & Test] ➔ [3. Docker Build] ➔ [4. Push to Docker Hub] ➔ [5. Minikube Deploy] ➔ [6. Verification]
```

1. **Stage 1: Checkout**  
   - Jenkins pulls the latest commit from `https://github.com/shreyanskota/guitartuner.git`.
2. **Stage 2: Build and Test**  
   - Jenkins creates a clean Python virtual environment (`venv`), installs `requirements.txt`, and runs **`pytest`**.  
   - *If any unit test fails, the pipeline immediately stops*—preventing broken code from reaching production.
3. **Stage 3: Docker Build**  
   - Builds the Docker image from our `Dockerfile` and tags it with the build number and `latest` (`shreyanskota/guitar-tuner:4`).
4. **Stage 4: Push Image to Registry**  
   - Logs into Docker Hub using encrypted Jenkins credentials (`dockerhub-credentials`) and pushes the image.
5. **Stage 5: Minikube Deployment**  
   - Applies `deployment.yaml` and `service.yaml` using `kubectl`.  
   - Updates the container image using `kubectl set image`.
6. **Stage 6: Verification**  
   - Checks rollout status (`kubectl rollout status`), lists pods, and verifies HTTP `200 OK` on `/api/health`.

---

## 4. Live Demo Cheatsheet (What to Show the Examiner)

Have these tabs ready in your browser:

1. **Tab 1: Running Application** ➔ [http://3.111.33.220:30080](http://3.111.33.220:30080)  
   - Click strings (or press keys 1–6) to show the Web Audio tone generator sounding.
   - Show the `/api/health` and `/api/version` endpoints.
2. **Tab 2: Jenkins Pipeline** ➔ [http://3.111.33.220:8080/job/guitar-tuner-cicd/](http://3.111.33.220:8080/job/guitar-tuner-cicd/)  
   - Show the **Stage View** where all 6 stages are green (`SUCCESS`).
3. **Tab 3: GitHub Repository** ➔ [https://github.com/shreyanskota/guitartuner](https://github.com/shreyanskota/guitartuner)  
   - Show project structure: `app.py`, `Dockerfile`, `Jenkinsfile`, and `k8s/` folder.
4. **Tab 4: Docker Hub** ➔ [https://hub.docker.com/r/shreyanskota/guitar-tuner](https://hub.docker.com/r/shreyanskota/guitar-tuner)  
   - Show the pushed tags (`latest`, `4`).

---

## 5. How to Demonstrate Requirement #9 (v1 to v2 Code Change)

The evaluator wants to see a code change flow through the pipeline. Do this live:

1. Open `app.py` on your laptop and change:
   ```python
   APP_VERSION = "2.0.0"
   APP_THEME = "electric-purple"
   ```
2. In PowerShell, push the change:
   ```powershell
   git commit -am "feat: release version 2.0.0 with electric theme"
   git push origin main
   ```
3. Go to Jenkins and click **Build Now**.
4. Show the examiner:
   - Jenkins runs Pytest on the new code.
   - Docker builds and pushes image tagged with the new build number.
   - Kubernetes performs a **Rolling Update** (creates new pod, verifies health, then deletes old pod).
   - Refresh `http://3.111.33.220:30080` to show **v2.0.0** live!

---

## 6. Top 10 Viva Questions & Exact 1-2 Line Answers

### Q1: What is CI/CD?
**Answer:** CI (Continuous Integration) is automatically building and testing code on every commit. CD (Continuous Delivery/Deployment) is automatically packaging and deploying verified code to production environments.

### Q2: Why use Docker instead of running Python directly on the server?
**Answer:** Docker ensures portability and consistency. It packages the exact Python runtime, libraries, and system dependencies into an isolated container, eliminating "environment drift" between dev and production.

### Q3: What is the difference between Docker and Kubernetes?
**Answer:** Docker creates and runs individual containers. Kubernetes is an orchestrator that manages multiple containers across a cluster—handling automated scaling, self-healing, load balancing, and rolling updates.

### Q4: What is Minikube?
**Answer:** Minikube is a lightweight tool that runs a single-node Kubernetes cluster inside a Docker container or VM, ideal for development, local testing, and academic demonstrations.

### Q5: What is a Kubernetes Pod?
**Answer:** A Pod is the smallest deployable unit in Kubernetes. It encapsulates one or more closely coupled containers, storage resources, and a unique IP address. In our project, each pod runs 1 guitar tuner container.

### Q6: What is a Kubernetes Service and why did you use `NodePort`?
**Answer:** A Service provides a stable network endpoint and load balancing across pods (since pods are ephemeral and change IPs). We used `NodePort` on port `30080` so the application can be accessed externally from the host/cloud IP.

### Q7: How does a Rolling Update work without downtime?
**Answer:** In `k8s/deployment.yaml`, we configured `maxSurge: 1` and `maxUnavailable: 0`. Kubernetes spins up a new v2 pod first, waits for its `readinessProbe` to succeed, routes traffic to it, and only then terminates the old v1 pod.

### Q8: What are Liveness and Readiness probes?
**Answer:**
- **Readiness Probe:** Checks if the app is ready to receive traffic (e.g. finished booting).
- **Liveness Probe:** Checks if the app is still healthy. If it freezes or deadlocks, Kubernetes restarts the pod automatically.
Both probe our `/api/health` endpoint.

### Q9: Why did you choose `python:3.10-slim` in the Dockerfile?
**Answer:** `python:3.10-slim` contains only essential runtime binaries. It reduces image size from ~1 GB to ~120 MB, speeding up downloads/deployments and minimizing security vulnerabilities by excluding unused compilers.

### Q10: How are credentials secured in Jenkins?
**Answer:** Credentials (like Docker Hub PAT) are encrypted in the Jenkins Credential Store and injected dynamically into pipeline steps using `withCredentials()`. They are never hardcoded in git or printed in logs (Jenkins masks them with `****`).

---

## 7. Key Kubernetes Commands (If the Examiner Asks You in Terminal)

SSH into EC2:
```bash
ssh -i C:\Users\LENOVO\Downloads\r1.pem ubuntu@3.111.33.220
```

Commands to show:
```bash
# Check running pods
kubectl get pods -l app=guitar-tuner

# Check deployment details and replica count
kubectl get deployment guitar-tuner

# Check service and port mapping
kubectl get service guitar-tuner-service

# Check rollout history
kubectl rollout history deployment/guitar-tuner

# View live application logs from pods
kubectl logs -l app=guitar-tuner --tail=20
```

Good luck! You have a real, fully functioning, 100% compliant CI/CD pipeline on AWS. Walk in with confidence! 🚀
