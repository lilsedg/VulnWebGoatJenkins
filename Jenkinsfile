pipeline {
    agent { 
        docker { image 'maven:3-alpine' }
    }
    stages {
        stage('Agent Test') {
            steps {
                sh 'svn --version'
            }
        }
        
        stage('Path Decleration') {
            steps {
                sh '''
                 echo "PATH = ${PATH}"
                 echo "M2_HOME = ${M2_HOME}"
                '''
            }
        }
        
        stage('Build Container') {
            steps {
                maven(
                    maven: 'Maven 3.6.1'
                ) {
                sh '''
                  cd webgoat-server
                  mvn -B docker:build
                '''
                }
            }
        }
        
        stage('Test Container') { 
            steps {
                sh 'mvn test' 
            }
            post {
                always {
                    junit 'target/surefire-reports/*.xml' 
                }
            }
        }         
        
        stage('Publish Container') {
            when {
                branch 'master'
            }
            steps {
                sh '''
                  docker tag lilsedg/VulnWebGoatJenkins=8.0  /
                  hub.docker.com:5000/msedgwick08/appsec-kpmg=8.0:8.0
                    docker push 
                  hub.docker.com:5000/msedgwick08/appsec-kpmg=8.0:8.0 
                    '''
            }
        }            
    }
}
