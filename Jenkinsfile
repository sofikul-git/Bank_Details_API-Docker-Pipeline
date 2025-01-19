pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'sofikulmullick/bank-details-api'  // Docker image name
        DOCKER_TAG = 'latest'  // Docker image tag
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
                    bat 'docker stop flask-api-container || exit /b 0'
                    bat 'docker rm flask-api-container || exit /b 0'

                    // Run the Docker container with the new image
                    bat 'docker run -d --name flask-api-container ${DOCKER_IMAGE}:${DOCKER_TAG}'
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
