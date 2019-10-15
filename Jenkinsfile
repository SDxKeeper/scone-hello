pipeline {
  agent any
  stages {
    stage('Build image') {
      agent any
      environment {
        http_proxy = 'proxy-chain.intel.com:911'
        https_proxy = 'proxy-chain.intel.com:912'
      }
      steps {
        sh ' docker.build registry + ":$BUILD_NUMBER"'
      }
    }
  }
  environment {
    http_proxy = 'proxy-chain.intel.com:911'
    https_proxy = 'proxy-chain.intel.com:912'
  }
}