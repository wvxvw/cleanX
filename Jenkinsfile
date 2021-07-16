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
                        values 'pypi', 'anaconda'
                    }
                }

                stages {
                    stage('Build on pypi') {
                        when {
                            expression {
                                return "${PYTHON_DISTRIBUTION}" == 'pypi'
                            }
                        }
                        steps {
                            podTemplate(containers: [
                                containerTemplate(
                                    name: 'python',
                                    image: "python:${PYTHON_VERSION}",
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
                                        sh './.venv/bin/python ./setup.py bdist_egg'
                                        sh './.venv/bin/python ./setup.py bdist_wheel'
                                        sh 'ls ./dist/'
                                        stash includes: './dist/*.*',
                                            name: "dist-pypi-${PYTHON_VERSION}"
                                    }
                                }
                            }
                        }
                    }

                    stage('Build on conda') {
                        when {
                            expression {
                                return "${PYTHON_DISTRIBUTION}" == 'anaconda'
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
    runAsUser: 0
    runAsGroup: 0
  containers:
  - name: python
    image: continuumio/conda-ci-linux-64-python${PYTHON_VERSION}
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
                                        sh 'apt-get update -y'
                                        sh "apt-get install -y ${libraries}"
                                        sh 'which python'
                                        sh 'python -m venv .venv'
                                        sh '.venv/bin/python setup.py genconda'
                                        sh 'conda install conda-build'
                                        sh 'conda build -c conda-forge --output-folder ./dist ./conda-pkg/'
                                        stash includes: './dist/*.*',
                                            name: "dist-conda-${PYTHON_VERSION}"
                                    }
                                }
                            }
                        }
                    }

                    stage('Test on pypi') {
                        when {
                            expression {
                                return "${PYTHON_DISTRIBUTION}" == 'pypi'
                            }
                        }
                        steps {
                            podTemplate(containers: [
                                containerTemplate(
                                    name: 'python',
                                    image: "python:${PYTHON_VERSION}",
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
                                        unstash "dist-pypi-${PYTHON_VERSION}"
                                        sh './.venv/bin/python ./setup.py lint'
                                        sh './.venv/bin/python ./setup.py test --pytest-args "--junit-xml junit-report.xml"'
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
