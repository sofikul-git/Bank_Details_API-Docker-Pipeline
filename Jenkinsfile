pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'sofikulmullick/bank-details-api'  // Docker image name
        DOCKER_TAG = 'latest'  // Docker image tag
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
            // Check if the container exists and output the result for debugging
            bat '''
            echo "Checking for existing container..."
            set CONTAINER_ID=  // Initialize variable to ensure it's empty
            for /f %%i in ('docker ps -a -q -f "name=flask-api-container"') do set CONTAINER_ID=%%i
            echo "Container ID is: %CONTAINER_ID%"
            if not "%CONTAINER_ID%"=="" (
                echo "Stopping and removing flask-api-container..."
                docker stop flask-api-container
                docker rm flask-api-container
            ) else (
                echo "No existing container found to stop/remove."
            )
            '''

            // Run the Docker container with the new image
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

