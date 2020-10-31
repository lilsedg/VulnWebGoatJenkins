pipeline {
    agent { 
        docker { image 'node:14-alpine' }
    }
    stages {
        stage('Agent Test') {
            steps {
                sh 'node --version'
            }
        }
        
        stage('Maven Install') {
            steps {
                sh '''
                 echo "PATH = ${PATH}"
                 echo "M2_HOME = ${M2_HOME}"
                '''
            }
        }
        
        stage('Build container') {
            steps {
                sh '''
                  cd webgoat-server
                  mvn -B docker:build
                '''
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
