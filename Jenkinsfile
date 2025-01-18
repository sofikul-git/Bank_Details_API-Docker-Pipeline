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

        stage('Run Tests') {
            steps {
                script {
                    // Run tests inside the Docker container
                    docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").inside {
                        sh 'pytest tests/'  // Replace with your test command
                    }
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
                    // Stop and remove the existing container
                    sh 'docker stop flask-api-container || true'
                    sh 'docker rm flask-api-container || true'

                    // Run the new Docker container
                    sh "docker run -d --name flask-api-container -p 8080:8080 ${DOCKER_IMAGE}:${DOCKER_TAG}"
                }
            }
        }
    }

    post {
        always {
            // Clean workspace after pipeline execution
            cleanWs()
        }
    }
}
