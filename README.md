
# AeroETL: Projet ETL Météo avec Airflow et AWS

## Contexte du Projet

Ce projet implémente un pipeline ETL (Extract, Transform, Load) automatisé pour extraire des données météo provenant de l'API OpenWeatherMap, les transformer et les charger sur AWS pour l'analyse. Ce pipeline est orchestré avec **Apache Airflow**, qui gère l'automatisation et la planification de l'ETL, permettant d'obtenir des données fraîches chaque jour.

Les données météorologiques extraites incluent des informations telles que la température, l'humidité, la pression et des descriptions de conditions météo pour plusieurs villes. Ce projet met également en place des notifications en cas de problèmes dans le pipeline pour assurer une surveillance continue.

## Architecture du Projet

Le pipeline ETL comprend trois étapes principales :

1. **Extraction des Données** : Les données météo sont extraites de l'API OpenWeatherMap pour plusieurs villes. En cas d'erreur, le pipeline gère les exceptions et enregistre les problèmes rencontrés.

2. **Transformation des Données** : Les données brutes sont transformées pour extraire uniquement les informations pertinentes. Les transformations incluent :
   - La conversion des températures de Kelvin à Celsius.
   - La classification des conditions météo (ex: `Rainy`, `Clear`, `Cloudy`).
   - La structuration des données pour une analyse facile.

3. **Chargement des Données** : Les données transformées sont ensuite chargées vers deux destinations :
   - **AWS S3** : Pour un stockage sécurisé et évolutif.
   - **AWS RDS (PostgreSQL)** : Pour un accès facilité aux données et une intégration avec d'autres outils de visualisation.

## Technologies Utilisées

- **Python** : Langage principal pour le développement des scripts ETL.
- **Apache Airflow** : Orchestrateur de workflow pour automatiser le pipeline ETL.
- **AWS S3** : Stockage des données transformées au format JSON.
- **AWS RDS (PostgreSQL)** : Base de données relationnelle pour centraliser les données météo.
- **OpenWeatherMap API** : Source de données météo en temps réel.

## Prérequis

1. **Clé API OpenWeatherMap** : Créez un compte sur [OpenWeatherMap](https://openweathermap.org/) et récupérez une clé API.
2. **AWS** : Un compte AWS avec les permissions nécessaires pour S3 et RDS.
3. **Airflow** : Installez Apache Airflow dans votre environnement local ou sur un serveur.

## Configuration

Dans le dossier `config/`, créez un fichier `config.yaml` pour configurer les informations d'accès nécessaires à l'API OpenWeatherMap et aux services AWS.

Exemple de `config/config.yaml` :

```yaml
api:
  openweathermap_key: "YOUR_API_KEY"

aws:
  s3_bucket_name: "your-s3-bucket-name"
  rds_db_name: "weather_db"
  rds_user: "your_username"
  rds_password: "your_password"
  rds_host: "your_rds_host"
  rds_port: "5432"
```

Les variables d'environnement suivantes doivent également être définies dans Airflow pour l'intégration avec AWS :

- `OPENWEATHERMAP_API_KEY`
- `S3_BUCKET_NAME`
- `RDS_DB_NAME`
- `RDS_USER`
- `RDS_PASSWORD`
- `RDS_HOST`
- `RDS_PORT`

## Structure du Projet

```plaintext
- airflow_dags/
   ├── weather_data_pipeline.py         # Pipeline Airflow orchestrant le processus ETL
- job_scripts/
   ├── data_extraction.py               # Extraction des données depuis OpenWeatherMap
   ├── data_transformation.py           # Transformation des données pour l'analyse
   ├── data_loading.py                  # Chargement des données vers S3 et RDS
- config/
   ├── config.yaml                      # Configuration API et base de données
- README.md                             # Documentation du projet
```

## Instructions

### 1. Extraction des Données (`data_extraction.py`)

Ce script utilise l’API OpenWeatherMap pour récupérer des données météo pour une liste de villes spécifiée. La fonction `fetch_weather_data` se charge de récupérer les données pour chaque ville, en gérant les erreurs pour assurer une extraction robuste.

### 2. Transformation des Données (`data_transformation.py`)

Le script de transformation utilise plusieurs fonctions pour traiter les données extraites :
- **Conversion de Température** : Convertit les températures de Kelvin en Celsius.
- **Classification Météo** : Ajoute une classification basée sur la description des conditions météo.
- **Structuration** : Organise les données dans un format standardisé pour le stockage.

### 3. Chargement des Données (`data_loading.py`)

Les données transformées sont chargées dans :
- **AWS S3** : Les fichiers JSON sont créés pour chaque ville et sauvegardés dans un bucket S3 pour un archivage à long terme.
- **AWS RDS** : Les données sont également insérées dans une base de données PostgreSQL, ce qui permet un accès et une requêtage rapide.

### 4. Orchestration avec Airflow (`weather_data_pipeline.py`)

Le DAG Airflow `weather_data_pipeline.py` orchestre l'ensemble du pipeline ETL :
- **Extraction** → **Transformation** → **Chargement** : Chaque tâche est exécutée séquentiellement, avec des mécanismes de gestion des erreurs et des notifications en cas d’échec.

Exemple de DAG Airflow :

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from job_scripts.data_extraction import fetch_weather_data
from job_scripts.data_transformation import transform_weather_data
from job_scripts.data_loading import load_data_to_s3, load_data_to_rds

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG('weather_data_pipeline', default_args=default_args, schedule_interval='@daily') as dag:
    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=lambda: fetch_weather_data(["Paris", "London", "New York"]),
    )

    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_weather_data,
        provide_context=True
    )

    load_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data_to_s3,
        provide_context=True
    )

    extract_task >> transform_task >> load_task
```

## Exécution du Pipeline

1. **Lancer Airflow** : Si vous utilisez une instance Airflow, assurez-vous qu’elle est configurée avec les bonnes variables d’environnement.
2. **Déclencher le DAG** : Accédez à l'interface Airflow, trouvez le DAG `weather_data_pipeline`, et déclenchez-le manuellement ou laissez-le s’exécuter automatiquement chaque jour.

## Conclusion

Ce pipeline ETL permet une collecte et une structuration automatisée des données météo pour plusieurs villes, facilitant leur analyse et leur stockage sécurisé sur AWS. Grâce à Apache Airflow, ce projet est extensible et facile à maintenir.

---

### Améliorations Futures

- **Support pour d'autres APIs** : Intégration de nouvelles sources de données météorologiques.
- **Analyse Avancée** : Ajout d’analyses statistiques ou de modèles de machine learning pour la prédiction météo.
- **Tableau de Bord** : Création de visualisations en temps réel avec un outil tel que Grafana ou Tableau.

---

Ce modèle de `README.md` documente le projet de manière exhaustive, et le rend facile à comprendre et à utiliser pour tout nouvel utilisateur. Vous pouvez ajuster selon vos préférences et ajouter des images si nécessaire pour illustrer l'architecture.