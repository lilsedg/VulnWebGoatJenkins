pipeline {
    agent { 
        docker { image 'node:14-alpine' }
    }
    stages {
        stage('build') {
            steps {
                sh '''
                 echo "PATH = ${PATH}"
                 ech "M2_HOME = ${M2_HOME}"
                 mvn -B install
                '''
            }
            post {
                always {
                    junit '**/target/surefire-reports/**/*.xml'
                }
            }
        }
        stage('Agent Test') {
            steps {
                sh 'node --version'
                sh 'svn --version'
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
