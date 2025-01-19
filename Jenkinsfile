pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'sofikulmullick/bank-details-api'  // Docker image name
        DOCKER_TAG = 'latest'  // Docker image tag
        HOST_IP = '10.0.0.108'  // The IP address where the service should be available
        HOST_PORT = '8080'  // The port on which to bind the service
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

        stage('Deploy') {
            steps {
                script {
                    // Stop and remove the existing container (Windows compatible)
                    bat 'docker ps -a -q -f "name=flask-api-container" | findstr flask-api-container >nul && docker stop flask-api-container || exit /b 0'
                    bat 'docker ps -a -q -f "name=flask-api-container" | findstr flask-api-container >nul && docker rm flask-api-container || exit /b 0'

                    // Run the Docker container with the new image, bind to specific IP and port
                    bat "docker run -d --name flask-api-container -p ${HOST_IP}:${HOST_PORT}:8080 ${DOCKER_IMAGE}:${DOCKER_TAG}"
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
