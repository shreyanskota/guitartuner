# 🎸 DevOps & CI/CD Master Viva Guide (10/10 Marks)
**Course:** TYCSE · Cloud Computing & DevOps (CCA 2)  
**Project:** Precision Guitar Tuner Automated CI/CD Pipeline  

---

## 1. The 30-Second Summary (How to Introduce Your Project)

> *"In this project, I built a lightweight **Precision Guitar Tuner web app** in Python Flask and implemented a fully automated **CI/CD delivery pipeline** on an AWS EC2 Ubuntu instance using **Jenkins**, **Docker**, **Docker Hub**, and **Minikube (Kubernetes)**.*  
> *Whenever code is pushed to GitHub, Jenkins automatically tests the code with `pytest`, packages it into a lightweight Docker image, pushes it to Docker Hub using stored credentials, and performs a zero-downtime rolling deployment to Minikube with liveness and readiness health checks."*

---

## 2. Every Component Explained (With Simple Analogies for Beginners)

If you have never studied DevOps before, read these simple real-world analogies:

### 1. Git & GitHub
- **Real-World Analogy:** A **Google Doc with version history** or a **cloud save file for a video game**.
- **What it does:** Git tracks every change you make to your code files. GitHub is the cloud platform that hosts your git repository (`https://github.com/shreyanskota/guitartuner.git`) so Jenkins and your team can access it from anywhere.

### 2. AWS EC2 (Elastic Compute Cloud)
- **Real-World Analogy:** **Renting a computer in Amazon's high-tech warehouse** instead of running your home laptop 24/7.
- **What it does:** We launched an Ubuntu 22.04 server in Mumbai (`ap-south-1`) with 2 vCPUs and 8 GB of RAM (`m7i-flex.large`). This computer stays on all the time and runs Jenkins, Docker, and Minikube.
- **IP Address:** `3.111.33.220`

### 3. AWS Security Group
- **Real-World Analogy:** **The Security Guard at the entrance of the building** checking visitor badges.
- **What it does:** It acts as a firewall for our EC2 instance. We opened:
  - Port `22` for SSH (remote control).
  - Port `8080` for Jenkins UI.
  - Port `30080` for the Guitar Tuner web application.

### 4. Jenkins
- **Real-World Analogy:** **An Automated Factory Assembly Line Robot**.
- **What it does:** Instead of a human manually testing, building, and deploying software, Jenkins does it 100% automatically. It detects when new code is pushed to GitHub, pulls it, tests it, builds a container, pushes to Docker Hub, and tells Kubernetes to deploy it.

### 5. Jenkinsfile (Pipeline-as-Code)
- **Real-World Analogy:** **The Robot’s Step-by-Step Instruction Manual**.
- **What it does:** A script stored right in our repository that tells Jenkins exactly what stages to run:
  1. `Checkout` ➔ 2. `Build and Test` ➔ 3. `Docker Build` ➔ 4. `Push Image` ➔ 5. `Minikube Deploy` ➔ 6. `Verification`.

### 6. Python 3 & Flask
- **Real-World Analogy:** **The Engine and the Waiter**.
- **What it does:** Python is the programming language calculating frequencies. Flask is a lightweight web framework acting like a waiter: when a user opens the page or asks for `/api/health`, Flask serves the web page and JSON responses.

### 7. Gunicorn WSGI Server
- **Real-World Analogy:** **A multi-lane highway vs. a single-lane road**.
- **What it does:** Flask's built-in development server can only handle 1 request at a time. Gunicorn is a production-grade Python WSGI server running multiple worker processes to handle multiple simultaneous users smoothly.

### 8. Web Audio API (In the Browser)
- **Real-World Analogy:** **A Digital Musical Synthesizer built into Google Chrome/Firefox**.
- **What it does:** Instead of downloading heavy MP3 audio files, our JavaScript code uses the browser's audio synthesizer oscillator to vibrate soundwaves at the exact physical frequencies of guitar strings ($E_2=82.41$ Hz, $A_2=110$ Hz, $D_3=146.83$ Hz, $G_3=196$ Hz, $B_3=246.94$ Hz, $E_4=329.63$ Hz).

### 9. Pytest (Automated Testing)
- **Real-World Analogy:** **The Factory Quality Inspector / Food Taster**.
- **What it does:** Before packing our software, `pytest` runs 6 automated test cases in Jenkins Stage 2 checking that `/api/health` returns `200 OK` and frequency formulas are 100% accurate. If any test fails, Jenkins stops immediately to prevent broken code from shipping to users.

### 10. Docker & Containerization
- **Real-World Analogy:** **A Sealed, Pre-packed Lunchbox or Shipping Container**.
- **What it does:** Have you ever said *"It works on my computer, but doesn't work on yours"*? Docker solves this forever! It packages our Python code, libraries (`requirements.txt`), and operating system tools into a lightweight, self-contained box called a **Docker Image**. This image runs identically on Mac, Windows, Linux, AWS, or anywhere else.

### 11. Dockerfile
- **Real-World Analogy:** **The Recipe to make the Lunchbox**.
- **What it does:** A text file with instructions:
  1. Start with a clean Python base (`python:3.10-slim`).
  2. Copy our code files.
  3. Install dependencies (`pip install`).
  4. Create a secure, non-root user (`appuser`).
  5. Start the web server on port `3000` with Gunicorn.

### 12. Docker Hub
- **Real-World Analogy:** **The Global Supermarket / App Store for Containers**.
- **What it does:** A cloud registry where we store our built Docker images (`shreyanskota/guitar-tuner`). Anyone or any server with permission can pull and run our application with a single command.

### 13. Kubernetes (K8s)
- **Real-World Analogy:** **The Restaurant General Manager / Airport Air Traffic Controller**.
- **What it does:** Docker runs single containers; Kubernetes manages hundreds of them! It automates:
  - **Self-Healing:** If a container crashes, Kubernetes revives it in seconds.
  - **Scaling:** It can run 2, 10, or 100 copies (replicas) of the app.
  - **Zero-Downtime Updates:** Swaps out old versions for new ones without disconnecting users.

### 14. Minikube
- **Real-World Analogy:** **A Practice Flight Simulator for Kubernetes**.
- **What it does:** Real Kubernetes usually requires a cluster of 5 to 10 enterprise servers. Minikube is a tool that packages a full Kubernetes cluster inside a single Docker container on our EC2 instance, allowing us to practice and demonstrate real Kubernetes commands without high cloud costs.

### 15. kubectl (Kube-Control)
- **Real-World Analogy:** **The TV Remote Control for Kubernetes**.
- **What it does:** The command-line tool we use to talk to Minikube. For example: `kubectl get pods` tells Kubernetes to show us all running containers.

### 16. Kubernetes Pod
- **Real-World Analogy:** **An Individual Hotel Room**.
- **What it does:** The smallest building block in Kubernetes. A Pod wraps around our running Docker container. In our project, we have **2 Pods** running side-by-side (`guitar-tuner-...`).

### 17. Kubernetes Deployment (`deployment.yaml`)
- **Real-World Analogy:** **The Manager’s Roster / Shift Rules**.
- **What it does:** A configuration file declaring:
  - *"Always keep 2 copies of the Guitar Tuner running (`replicas: 2`)."*
  - *"If a new version is released, use RollingUpdate so users never see an error page."*

### 18. Kubernetes Service & NodePort (`service.yaml`)
- **Real-World Analogy:** **The Hotel Front Desk & Switchboard**.
- **What it does:** Since Pods are temporary and get new internal IP addresses whenever they restart, customers can't connect to pods directly. A **Service** provides a single, permanent phone number. We used `type: NodePort` on port `30080` so anyone in the world can reach our pods by visiting `http://3.111.33.220:30080`.

### 19. Rolling Update (Zero-Downtime Deployment)
- **Real-World Analogy:** **Changing the tires on a moving pit-stop car one wheel at a time**.
- **What it does:** When updating from v1 to v2:
  1. Kubernetes starts a new v2 pod.
  2. It waits for the v2 pod to pass its health check.
  3. It routes user traffic to the v2 pod.
  4. Only then does it delete the old v1 pod.
  5. The user never experiences even 1 millisecond of downtime!

### 20. Liveness & Readiness Probes
- **Real-World Analogy:**
  - **Readiness Probe:** *"Are you dressed and ready to take customer orders?"* (Checks `/api/health` before sending traffic).
  - **Liveness Probe:** *"Are you still breathing?"* (Periodically checks `/api/health`. If the server freezes, Kubernetes automatically kills and restarts it).

### 21. Socat
- **Real-World Analogy:** **An electrical extension cable / bridge**.
- **What it does:** Minikube runs inside its own isolated Docker network on the EC2 server (`192.168.49.2`). `socat` forwards incoming traffic from the EC2 public interface on port `30080` directly into Minikube's internal network.

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

Have these 4 tabs open:

1. **Tab 1: Live Web App** ➔ [http://3.111.33.220:30080](http://3.111.33.220:30080)  
   - Click strings (or press keys 1–6) to show the Web Audio tone generator sounding.
   - Show `/api/health` and `/api/version`.
2. **Tab 2: Jenkins Pipeline** ➔ [http://3.111.33.220:8080/job/guitar-tuner-cicd/](http://3.111.33.220:8080/job/guitar-tuner-cicd/)  
   - Show the **Stage View** where all 6 stages are green (`SUCCESS`).
3. **Tab 3: GitHub Repository** ➔ [https://github.com/shreyanskota/guitartuner](https://github.com/shreyanskota/guitartuner)  
   - Show project structure: `app.py`, `Dockerfile`, `Jenkinsfile`, and `k8s/` folder.
4. **Tab 4: Docker Hub** ➔ [https://hub.docker.com/r/shreyanskota/guitar-tuner](https://hub.docker.com/r/shreyanskota/guitar-tuner)  
   - Show the pushed tags (`latest`, `4`).

---

## 5. How to Demonstrate Requirement #9 (v1 to v2 Code Change)

If the examiner asks: *"Show me a code change being deployed automatically"*:

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
   - Docker builds and pushes a new image tagged with the new build number.
   - Kubernetes updates the pods without dropping traffic (Rolling Update).
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

## 7. Useful Kubernetes Terminal Commands (To Impress Evaluators)

SSH into EC2:
```bash
ssh -i C:\Users\LENOVO\Downloads\r1.pem ubuntu@3.111.33.220
```

Commands:
```bash
# Check running pods
kubectl get pods -l app=guitar-tuner

# Check deployment details and replica count (2/2)
kubectl get deployment guitar-tuner

# Check service and port mapping (Port 30080)
kubectl get service guitar-tuner-service

# Check rollout history
kubectl rollout history deployment/guitar-tuner

# View live application logs from the pods
kubectl logs -l app=guitar-tuner --tail=20
```

You are 100% prepared. Walk in with full confidence! 🚀
