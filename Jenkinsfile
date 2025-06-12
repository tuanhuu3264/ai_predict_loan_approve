pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.13'
        VENV_NAME = 'venv'
        DOCKER_IMAGE = 'loan-prediction-app'
        DOCKER_TAG = "latest"
        DOCKER_REGISTRY = 'tuanhuu3264/hackathon'
    }
    
    stages {
        stage('Setup Environment') {
            steps {
                sh '''
                    python -m venv ${VENV_NAME}
                    . ${VENV_NAME}/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Train Model') {
            steps {
                sh '''
                    . ${VENV_NAME}/bin/activate
                    python src/preprocess.py
                    python src/train.py
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                    
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
                    // Dừng container cũ nếu đang chạy
                    sh 'docker stop loan-prediction-app || true'
                    sh 'docker rm loan-prediction-app || true'
                    
                    // Chạy container mới
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
                    // Xóa các Docker image cũ
                    sh '''
                        docker image prune -f
                        docker system prune -f
                    '''
                    
                    // Xóa các file tạm và cache
                    sh '''
                        rm -rf ${VENV_NAME}
                        rm -rf __pycache__
                        rm -rf .pytest_cache
                        rm -rf .coverage
                    '''
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
            // Thông báo lỗi qua email hoặc các kênh khác
            emailext (
                subject: "Pipeline Failed: ${currentBuild.fullDisplayName}",
                body: "Something is wrong with ${env.BUILD_URL}",
                recipientProviders: [[$class: 'DevelopersRecipientProvider']]
            )
        }
    }
} 