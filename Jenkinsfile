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

org.jenkinsci.plugins.durabletask.BourneShellScript.LAUNCH_DIAGNOSTICS = true

def libraries = [
    'libleptonica-dev',
    'tesseract-ocr-all',
    'libtesseract-dev',
    'python3-opencv'
].join(' ')

pipeline {
    agent none
    options {
        timestamps()
        timeout(time: 1, unit: 'HOURS')
    }
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
                        values 'python', 'continuumio/conda-ci-linux-64-python'
                    }
                }

                stages {
                    stage('Build on pypi') {
                        when {
                            expression {
                                return "${PYTHON_DISTRIBUTION}" == 'python'
                            }
                        }
                        steps {
                            podTemplate(containers: [
                                containerTemplate(
                                    name: 'python',
                                    image: "${PYTHON_DISTRIBUTION}:${PYTHON_VERSION}",
                                    command: 'sleep',
                                    args: '99d'
                                )
                            ]) {
                                node(POD_LABEL) {
                                    git url: 'https://github.com/wvxvw/cleanX.git', branch: 'main'
                                    container('python') {
                                        sh 'apt-get update -y'
                                        sh "apt-get install -y ${libraries}"
                                        sh "python${PYTHON_VERSION} -m venv .venv"
                                        sh './.venv/bin/python -m pip install wheel'
                                        sh './.venv/bin/python ./setup.py install'
                                    }
                                }
                            }
                        }
                    }

                    stage('Build on conda') {
                        when {
                            expression {
                                return "${PYTHON_DISTRIBUTION}" ==
                                    'continuumio/conda-ci-linux-64-python'
                            }
                        }
                        steps {
                            podTemplate(yaml: """
apiVersion: v1
kind: Pod
metadata:
  name: conda-${PYTHON_VERSION}
spec:
  securityContext:
    runAsUser: 1000
    runAsGroup: 1000
  containers:
  - name: python
    image: ${PYTHON_DISTRIBUTION}${PYTHON_VERSION}
    command:
    - /bin/bash
    args:
    - "-c"
    - "sleep 99d"
    workingDir: /home/jenkins/agent
""") {
                                node(POD_LABEL) {
                                    git url: 'https://github.com/wvxvw/cleanX.git', branch: 'main'
                                    container('python') {
                                        sh 'echo THIS IS CONDA'
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
