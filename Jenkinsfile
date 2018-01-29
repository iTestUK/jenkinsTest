pipeline {
  agent none
  stages {
    stage('Collect') {
      steps {
        echo 'Collecting'
      }
    }
    stage('Test') {
      steps {
        input(message: 'Is this OK?', id: '01', submitterParameter: 'Hello')
      }
    }
    stage('Publish') {
      steps {
        echo 'Hello, all done'
      }
    }
  }
}