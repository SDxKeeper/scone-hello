pipeline {
  agent { label 'AKS-container' }
  stages {
    stage('Build image') {
      steps {
        script {
          dockerImage = docker.build(registry + ":$BUILD_NUMBER", ".")
        }

      }
    }
    stage('Deploy Image') {
      steps {
        script {
          docker.withRegistry( '', registryCredential ) {
            dockerImage.push()}
          }

        }
      }
      stage('Cleanup') {
        steps {
          sh 'docker rmi $registry:$BUILD_NUMBER'
        }
      }
    }
    environment {
      registry = 'sdxkeeper/scone-hello'
      registryCredential = 'dockerhub'
    }
  }
