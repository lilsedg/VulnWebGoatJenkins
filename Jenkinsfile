pipeline {
    agent { dockerfile true }
    stages {
        stage('build') {
            steps {
                sh 'mvn --version'
            }
            post {
                always {
                    junit '**/target/surefire-reports/**/*.xml'
                }
            }
        }
        stage('test') {
            steps {
                sh 'node-version'
            }
        }
        stage('Publich Container') {
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
