org.jenkinsci.plugins.durabletask.BourneShellScript.LAUNCH_DIAGNOSTICS = true

def libraries = [
    'libleptonica-dev',
    'tesseract-ocr-all',
    'libtesseract-dev',
].join(' ')

def branch_full = scm.branches[0].name

def branch = branch_full[11..-1]

pipeline {
    agent none
    options {
        timestamps()
        timeout(time: 2, unit: 'HOURS')
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
                                    sh "echo ${branch}, ${env.GIT_BRANCH}, ${GIT_BRANCH}"
                                    git url: 'https://github.com/wvxvw/cleanX.git',
                                        branch: "${branch}"
                                    container('python') {
                                        sh 'apt-get update -y'
                                        sh "apt-get install -y ${libraries}"
                                        sh "python${PYTHON_VERSION} -m venv .venv"
                                        sh './.venv/bin/python -m pip install wheel'
                                        sh './.venv/bin/python ./setup.py install'
                                        sh './.venv/bin/python ./setup.py bdist_egg'
                                        sh './.venv/bin/python ./setup.py bdist_wheel'
                                        dir('dist') {
                                            stash name: "dist-pypi-${PYTHON_VERSION}"
                                        }
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
                                    git url: 'https://github.com/wvxvw/cleanX.git',
                                        branch: "${branch}"
                                    container('python') {
                                        sh 'apt-get update -y'
                                        sh """apt-get install -y ${libraries} \\
                                           libgl1-mesa-dri libgl1-mesa-glx"""
                                        sh 'python -m venv .venv'
                                        sh '.venv/bin/python setup.py genconda'
                                        sh 'conda config --add channels conda-forge'
                                        sh 'conda install conda-build'
                                        sh 'conda build --output-folder ./dist ./conda-pkg/'
                                        dir('./dist/') {
                                            stash name: "dist-conda-${PYTHON_VERSION}"
                                        }
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
                            podTemplate(
                                podRetention: onFailure(),
                                activeDeadlineSeconds: 3600,
                                containers: [
                                containerTemplate(
                                    name: 'python',
                                    image: "python:${PYTHON_VERSION}",
                                    command: 'sleep',
                                    args: '99d'
                                )
                            ]) {
                                node(POD_LABEL) {
                                    container('python') {
                                        git url: 'https://github.com/wvxvw/cleanX.git',
                                            branch: "${branch}"
                                        sh 'apt-get update -y'
                                        sh """apt-get install -y ${libraries} \\
                                           libgl1-mesa-dri libgl1-mesa-glx"""
                                        sh "python${PYTHON_VERSION} -m venv .venv"
                                        sh './.venv/bin/python -m pip install wheel'
                                        dir('./dist') {
                                            unstash "dist-pypi-${PYTHON_VERSION}"
                                        }
                                        sh './.venv/bin/python -m pip install ./dist/*.whl'
                                        sh './.venv/bin/python ./setup.py lint'
                                        sh """./.venv/bin/python \\
                                              ./setup.py test --pytest-args \\
                                               \"--junit-xml \\
                                               pypi-${PYTHON_VERSION}junit-report.xml\"
                                           """
                                        junit testResults: "pypi-${PYTHON_VERSION}junit-report.xml",
                                            skipPublishingChecks: true
                                    }
                                }
                            }
                        }
                    }
                    stage('Test on conda') {
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
    resources:
      requests:
        memory: "2Gi"
        cpu: "2"
      limits:
        memory: "2Gi"
        cpu: "2"
""") {
                                node(POD_LABEL) {
                                    container('python') {
                                        git url: 'https://github.com/wvxvw/cleanX.git',
                                            branch: "${branch}"
                                        dir('./dist') {
                                            unstash "dist-conda-${PYTHON_VERSION}"
                                        }
                                        sh 'apt-get update -y'
                                        sh 'apt-get install -y libgl1-mesa-dri libgl1-mesa-glx'
                                        sh 'conda config --add channels conda-forge'
                                        sh 'conda install $(find ./dist/ -name cleanx*.bz2)'
                                        sh 'conda install pytest pycodestyle'
                                        sh 'python ./setup.py lint'
                                        sh """python \\
                                              ./setup.py test --pytest-args \\
                                               \"--junit-xml \\
                                               conda-${PYTHON_VERSION}junit-report.xml\"
                                           """
                                        junit testResults: "conda-${PYTHON_VERSION}junit-report.xml",
                                            skipPublishingChecks: true
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
