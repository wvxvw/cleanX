// pipeline {
//     agent {
//         kubernetes {
//             label 'kubeagent'
//             containerTemplate {
//                 name 'dind-jdk8-maven3'
//                 image 'eu.gcr.io/jenkins-demo/dind-jdk8-maven3:v4'
//                 ttyEnabled true
//                 command 'cat'
//             }
//         }
//     }
//     stages {
//     }
// }



pipeline {
    agent none
    stages {
        stage('BuildAndTest') {
            matrix {
                agent {
                    label "kubeagent"
                }
                axes {
                    axis {
                        name 'PYTHON_VERSION'
                        values '3.7', '3.8', '3.9'
                    }
                    axis {
                        name 'PYTHON_DISTRIBUTION'
                        values 'python:', 'continuumio/conda-ci-linux-64-python'
                    }
                }

                stages {

                    stage('Build on ${PYTHON_DISTRIBUTION}/${PYTHON_VERSION}') {
                        steps {
                            podTemplate(containers: [
                                containerTemplate(
                                    name: "python",
                                    image: "${PYTHON_DISTRIBUTION}${PYTHON_VERSION}",
                                    command: 'sleep',
                                    args: '99d'
                                )
                            ]) {
                                node(POD_LABEL) {
                                    git url: 'https://github.com/wvxvw/cleanX.git', branch: 'main'
                                    container('python') {
                                        sh "python${PYTHON_VERSION} -m venv .venv"
                                        sh './.venv/bin/python ./setup.py install'
                                    }
                                }
                            }
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
