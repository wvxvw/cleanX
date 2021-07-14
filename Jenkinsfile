pipeline {
    agent none
    stages {
        stage('BuildAndTest') {
            matrix {
                agent any
                axes {
                    axis {
                        name 'PYTHON_VERSION'
                        values '3.7', '3.8', '3.9'
                    }
                    axis {
                        name 'PYTHON_DISTRIBUTION'
                        values 'PiPy', 'Anaconda'
                    }
                }
                stages {
                    stage('Build') {
                        steps {
                            echo "Do Build for ${PYTHON_VERSION} - ${PYTHON_DISTRIBUTION}"
                        }
                    }
                    stage('Test') {
                        steps {
                            echo "Do Test for ${PYTHON_VERSION} - ${PYTHON_DISTRIBUTION}"
                        }
                    }
                }
            }
        }
    }
}
