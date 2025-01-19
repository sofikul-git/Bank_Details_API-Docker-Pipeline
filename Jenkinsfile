pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'sofikulmullick/bank-details-api'  // Docker image name
        DOCKER_TAG = 'latest'  // Docker image tag
        HOST_PORT = '8080'  // The port on which to bind the service
        APP_URL = 'http://localhost:8080'  // The URL of the running API
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from GitHub
                git credentialsId: 'github-credentials', url: 'https://github.com/sofikul-git/Bank_Details_API-Docker-Pipeline.git', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image from the Dockerfile
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                script {
                    // Push the image to Docker Hub
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-credentials') {
                        docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").push()
                    }
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    // Test if the application is running
                    echo "Running API test..."
                    def response = httpRequest(url: "${APP_URL}", validResponseCodes: '200')
                    echo "Response from API: ${response}"
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Stop and remove the existing container (Windows compatible)
                    bat 'docker ps -a -q -f "name=flask-api-container" | findstr flask-api-container >nul && docker stop flask-api-container || exit /b 0'
                    bat 'docker ps -a -q -f "name=flask-api-container" | findstr flask-api-container >nul && docker rm flask-api-container || exit /b 0'

                    // Run the Docker container with the new image, bind to all available network interfaces
                    bat "docker run -d --name flask-api-container -p ${HOST_PORT}:${HOST_PORT} ${DOCKER_IMAGE}:${DOCKER_TAG}"
                }
            }
        }
        
        stage('Post Actions') {
            steps {
                cleanWs()  // Clean up workspace after build
            }
        }
    }
}
