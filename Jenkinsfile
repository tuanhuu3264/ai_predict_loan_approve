pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'loan-prediction-app'
        DOCKER_TAG = "latest"
        DOCKER_REGISTRY = 'tuanhuu3264/hackathon'
    }
    
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // Build Docker image
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                    
                    // Push to registry
                    docker.withRegistry("https://${DOCKER_REGISTRY}") {
                        docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").push()
                    }
                }
            }
        }

        stage('Deploy Docker Container') {
            when {
                branch 'main'
            }
            steps {
                script {
                    // Stop and remove old container if exists
                    sh 'docker stop loan-prediction-app || true'
                    sh 'docker rm loan-prediction-app || true'
                    
                    // Run new container
                    docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").run(
                        '-d',
                        '--name loan-prediction-app',
                        '-p 8000:8000',
                        '--restart unless-stopped'
                    )
                }
            }
        }

        stage('Cleanup') {
            steps {
                script {
                    // Clean up old Docker images
                    sh '''
                        docker image prune -f
                        docker system prune -f
                    '''
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        
    }
} 