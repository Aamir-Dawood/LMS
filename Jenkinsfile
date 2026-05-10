pipeline {
    agent any

    stages {
        stage('Connection Test') {
            steps {
                echo 'Successfully connected to GitHub!'
                sh 'uptime'
                sh 'whoami'
            }
        }
        stage('Environment Check') {
            steps {
                echo 'Checking server tools...'
                sh 'docker --version || echo "Docker not installed yet"'
                sh 'java -version'
            }
        }
    }
    
    post {
        always {
            echo 'Test complete.'
        }
    }
}
