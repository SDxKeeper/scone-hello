pipeline {
  agent any
  stages {
    stage('Build image') {
      environment {
        http_proxy = 'proxy-chain.intel.com:911'
        https_proxy = 'proxy-chain.intel.com:912'
      }
      steps{
        script {
          docker.build(registry + ":$BUILD_NUMBER", "--build-arg http_proxy=http://proxy-chain.intel.com:911 --build-arg https_proxy=http://proxy-chain.intel.com:912 .")
        }
      }
    }
  }
  environment {
    http_proxy = 'proxy-chain.intel.com:911'
    https_proxy = 'proxy-chain.intel.com:912'
    registry = "sdxkeeper/scone-hello"
    registryCredential = 'dockerhub'
  }
}

