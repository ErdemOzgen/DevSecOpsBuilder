pipeline {
    agent any

    stages {
        stage('Start') {
            steps {
                sh 'echo "Welcome to DevSecOpsBuilder"'
            }
        }
        stage('Parallel_Steps_2') {
            steps {
                parallel {
                    'List_files': {
                        steps {
                            sh 'ls -l'
                        }
                    },
                    'Get_current_directory': {
                        steps {
                            sh 'pwd'
                        }
                    }
                }
            }
        }
        stage('GITLEAK-JOB') {
            steps {
                sh 'docker run -v ${path_to_host_folder_to_scan}:/path zricethezav/gitleaks:latest ${run_command_option} --source="/path" ${options}'
            }
        }
        stage('Finished') {
            steps {
                sh 'echo DevSecOps Builder has been finished ${echo_text}'
            }
        }
    }
    post {
        success {
            echo 'Success!'
        }
        failure {
            echo 'Failure!'
        }
    }
}
