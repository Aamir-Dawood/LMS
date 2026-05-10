pipeline {
    agent any

    options {
        // Keeps your 30GB disk clean by only saving 5 builds
        buildDiscarder(logRotator(numToKeepStr: '5'))
        timeout(time: 20, unit: 'MINUTES')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build Docker Image') {
            steps {
                // This builds your app into a reusable image
                sh 'docker build -t lms-app:latest .'
            }
        }
        stage('Deploy to Production') {
            steps {
                script {
                    // Stop old version, delete it, and run the new one on Port 80
                    sh 'docker stop lms-container || true'
                    sh 'docker rm lms-container || true'
                    sh 'docker run -d --name lms-container -p 80:3000 lms-app:latest'
                }
            }
        }
    }
    
    post {
        success {
            echo 'App is live! Check your AWS Public IP.'
        }
    }
}
