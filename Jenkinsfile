// Experiment 2 Part C (optional) - only if a Jenkins server is available.
// For a Windows agent replace `sh` with `bat` and `python3` with `python`.
pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Setup and Test') {
            steps {
                sh 'python3 -m pip install -r requirements-dev.txt'
                sh 'python3 -m pytest -v'
            }
        }
    }
}
