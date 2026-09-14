// Pipeline Jenkins pour SunuSanté (chapitre 4).


def runCmd(String commande) {
    if (isUnix()) {
        sh commande
    } else {
        bat commande
    }
}

pipeline {
    agent any

    environment {
        PATH = "C:\\Users\\hp\\AppData\\Local\\Programs\\Python\\Python312;C:\\Users\\hp\\AppData\\Local\\Programs\\Python\\Python312\\Scripts;${env.PATH}"
    }

    stages {
        stage('Récupération du code') {
            steps {
                checkout scm
            }
        }

        stage('Installation des dépendances') {
            steps {
                runCmd 'python -m pip install --upgrade pip'
                runCmd 'pip install -r requirements-dev.txt'
            }
        }

        stage('Build') {
            // Python ne se compile pas comme Java, mais on peut quand
            // même vérifier que le projet est valide avant d'aller plus
            // loin : configuration Django cohérente, fichiers statiques
            // collectables sans erreur.
            steps {
                runCmd 'python manage.py check'
                runCmd 'python manage.py collectstatic --noinput --dry-run'
            }
        }

        stage('Standard de code (lint)') {
            // Prérequis d'une bonne CI, chapitre 4 partie 3 : le style est
            // vérifié par la machine, la revue de code se concentre sur le
            // fond.
            steps {
                runCmd 'flake8 .'
            }
        }

        stage('Tests') {
            // Unitaires, intégration et système (TP1-TP4) sont tous
            // exécutés ici par le même appel : manage.py les découvre
            // automatiquement.
            steps {
                runCmd 'python manage.py test'
            }
        }

        stage('Sécurité - SAST') {
            // cf. chapitre 3 et chapitre 4 partie 2 : "tests de sécurité,
            // cf. SAST/DAST/SCA au chapitre 3".
            steps {
                runCmd 'semgrep --config p/security-audit --config p/django --config p/python --error .'
            }
        }

        stage('Sécurité - SCA') {
            steps {
                runCmd 'pip-audit -r requirements.txt'
            }
        }
    }

    post {
        success {
            echo 'Pipeline vert : build, lint, tests et sécurité tous OK.'
        }
        failure {
            echo 'Pipeline rouge : consultez le premier stage en échec ci-dessus.'
        }
    }
}
