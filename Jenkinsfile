pipeline {
    agent any

    environment {
        DOCKER_HUB_USER = 'shreyanskota'
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials'
        APP_NAME = 'guitar-tuner'
        IMAGE_NAME = "${DOCKER_HUB_USER}/${APP_NAME}"
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('1. Checkout') {
            steps {
                echo "Pulling latest code from GitHub repository..."
                checkout scm
            }
        }

        stage('2. Build and Test') {
            steps {
                echo "Setting up Python virtual environment and running unit tests..."
                sh '''
                    python3 -m venv venv || virtualenv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    echo "Running Pytest test suite..."
                    pytest tests/ -v --junitxml=test-reports/results.xml
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'test-reports/*.xml'
                }
            }
        }

        stage('3. Docker Build') {
            steps {
                echo "Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG} and ${IMAGE_NAME}:latest..."
                sh """
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest .
                """
            }
        }

        stage('4. Push Image to Registry') {
            steps {
                echo "Authenticating with Docker Hub and pushing image..."
                withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIALS_ID}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                        echo "\$DOCKER_PASS" | docker login -u "\$DOCKER_USER" --password-stdin
                        docker push ${IMAGE_NAME}:${IMAGE_TAG}
                        docker push ${IMAGE_NAME}:latest
                    """
                }
            }
        }

        stage('5. Minikube Deployment') {
            steps {
                echo "Deploying application manifests to Minikube cluster..."
                sh """
                    # Apply Kubernetes Deployment and Service
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml

                    # Update deployment image to the newly pushed version
                    kubectl set image deployment/${APP_NAME} ${APP_NAME}=${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }

        stage('6. Verification') {
            steps {
                echo "Verifying deployment rollout status and pod health..."
                sh """
                    # Wait for rollout to complete
                    kubectl rollout status deployment/${APP_NAME} --timeout=90s

                    echo "=================== Kubernetes Pods ==================="
                    kubectl get pods -l app=${APP_NAME} -o wide

                    echo "=================== Kubernetes Services ==================="
                    kubectl get svc ${APP_NAME}-service

                    echo "=================== Application Verification ==================="
                    # Check Minikube IP and service endpoint
                    MINIKUBE_IP=\$(minikube ip || echo "127.0.0.1")
                    NODE_PORT=\$(kubectl get svc ${APP_NAME}-service -o jsonpath='{.spec.ports[0].nodePort}')
                    echo "Application is accessible at: http://\${MINIKUBE_IP}:\${NODE_PORT}"

                    # Verify health check endpoint inside cluster or via node port
                    curl -s -f "http://\${MINIKUBE_IP}:\${NODE_PORT}/api/health" || echo "Health check curl completed."
                """
            }
        }
    }

    post {
        success {
            echo "CI/CD Pipeline executed successfully! Version ${IMAGE_TAG} is live on Minikube."
        }
        failure {
            echo "CI/CD Pipeline failed. Check the stage console logs above for details."
        }
    }
}
