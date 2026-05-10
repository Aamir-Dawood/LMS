pipeline {
    agent any

    options {
        // Keeps your AWS disk clean by only saving the last 5 builds
        buildDiscarder(logRotator(numToKeepStr: '5'))
        // Stops the build if it hangs for more than 15 minutes
        timeout(time: 15, unit: 'MINUTES')
    }

    stages {
        stage('Checkout SCM') {
            steps {
                // Pulls your latest code from GitHub
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building the Full-Stack Docker Image...'
                // Uses the Dockerfile in your root directory
                sh 'docker build -t lms-app:latest .'
            }
        }

        stage('Clean Old Deployment') {
            steps {
                echo 'Cleaning up any existing containers...'
                script {
                    // || true prevents the build from failing if the container doesn't exist yet
                    sh 'docker stop lms-container || true'
                    sh 'docker rm lms-container || true'
                }
            }
        }

        stage('Deploy to Production') {
            steps {
                echo 'Starting the LMS Application on Port 80...'
                // Maps AWS Port 80 to your App Port 3000
                sh 'docker run -d --name lms-container -p 80:3000 lms-app:latest'
            }
        }
    }

    post {
        success {
            echo '--------------------------------------------------'
            echo 'SUCCESS: Your Leave Management System is now LIVE!'
            echo 'Access it via your AWS Public IP address.'
            echo '--------------------------------------------------'
        }
        failure {
            echo 'Build failed. Check the Console Output for errors.'
        }
    }
}
