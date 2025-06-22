# Système de Détection d'Anomalies dans les Logs HDFS

## Description

Ce projet implémente un système intelligent de détection d'anomalies spécialement conçu pour analyser les logs HDFS (Hadoop Distributed File System). Le système utilise des techniques d'apprentissage automatique, notamment l'algorithme Isolation Forest, pour identifier automatiquement les comportements anormaux dans les séquences d'événements sans nécessiter d'exemples d'anomalies préalablement étiquetés.

## Fonctionnalités Principales

- **Détection d'anomalies HDFS** : Analyse spécialisée pour les logs HDFS vectorisés
- **Apprentissage non-supervisé** : Utilise l'algorithme Isolation Forest pour la détection
- **Interface multiple** : Ligne de commande, interface interactive, et scripts dédiés
- **Préprocessing automatique** : Normalisation et réduction de dimensionnalité
- **Rapports détaillés** : Analyse des anomalies avec identification des événements critiques
- **Visualisations avancées** : Heatmaps, histogrammes et graphiques de distribution
- **Architecture modulaire** : Code organisé et extensible

## Structure du Projet

```
gestion_logs/
├── config/                       # Fichiers de configuration
│   ├── data_config.yaml         # Configuration des données
│   ├── logging_config.yaml      # Configuration du système de logs
│   └── model_config.yaml        # Configuration des modèles
├── data/                         # Données du projet
│   ├── raw/                     # Données brutes
│   │   ├── normal_trace.csv     # Logs normaux
│   │   └── failure_trace.csv    # Logs avec anomalies
│   ├── results/                 # Résultats d'analyse
│   │   ├── anomalies_normal_trace.csv
│   │   └── anomalies_failure_trace.csv
│   └── visualizations/          # Visualisations générées
│       └── category_severity_heatmap.png
├── logs/                         # Fichiers de log du système
├── models/                       # Modèles sauvegardés
├── scripts/                      # Scripts d'exécution
│   ├── detect_anomalies.py      # Détection d'anomalies
│   ├── interactive_cli.py       # Interface interactive
│   ├── train_model.py           # Entraînement de modèles
│   └── visualize_anomalies.py   # Génération de visualisations
├── src/                          # Code source principal
│   ├── models/                  # Modèles de détection
│   │   ├── base_detector.py     # Classe de base abstraite
│   │   └── hdfs_detector.py     # Détecteur HDFS spécialisé
│   └── utils/                   # Utilitaires
│       ├── file_utils.py        # Gestion des fichiers
│       └── logger.py            # Système de logging
├── tests/                        # Tests unitaires et d'intégration
├── explication_technique.md      # Documentation technique détaillée
├── guide_utilisateur.md          # Guide utilisateur
├── main.py                       # Point d'entrée principal
├── README.md                     # Documentation générale
└── setup.py                      # Configuration d'installation
```

## Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de packages Python)

### Installation des dépendances

```bash
pip install -r requirements.txt
```

Les dépendances principales incluent :
- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn
- pyyaml

### Installation du package (optionnel)

```bash
pip install -e .
```

## Utilisation

### 1. Interface Interactive (Recommandée)

Lancez l'interface interactive pour une utilisation simple :

```bash
python main.py
```

Cette interface vous guidera à travers les étapes :
1. Création d'un modèle à partir de données normales
2. Détection d'anomalies dans de nouveaux fichiers
3. Visualisation des fichiers disponibles

### 2. Ligne de Commande

#### Créer un modèle

```bash
python main.py create normal_trace.csv
```

#### Détecter des anomalies

```bash
python main.py detect failure_trace.csv
```

#### Lister les fichiers disponibles

```bash
python main.py list
```

### 3. Scripts Dédiés

#### Entraînement avec options avancées

```bash
python scripts/train_model.py --data normal_trace.csv --contamination 0.02
```

#### Détection avec type de modèle spécifique

```bash
python scripts/detect_anomalies.py --data failure_trace.csv --model-type hdfs
```

#### Génération de visualisations

```bash
python scripts/visualize_anomalies.py --input data/results/anomalies_failure_trace.csv
```

## Format des Données

Le système est optimisé pour les logs HDFS vectorisés où :

- **Chaque ligne** représente une séquence d'événements
- **Chaque colonne** représente un type d'événement spécifique
- **Les valeurs** sont des compteurs d'occurrences (0, 1, 2, ...)
- **Première colonne** (optionnelle) : TaskID ou identifiant de séquence

### Exemple de format CSV

```csv
TaskID,getFileInfo+success,blockSeekTo+ioexception,sendBlock+success,...
Task_1,5,0,3,...
Task_2,2,1,4,...
```

## Fonctionnement Technique

### Algorithme de Détection

Le système utilise l'algorithme **Isolation Forest** pour la détection d'anomalies :

1. **Principe** : Les anomalies sont plus faciles à isoler que les points normaux
2. **Avantages** :
   - Ne nécessite pas d'exemples d'anomalies pour l'apprentissage
   - Efficace sur de grands volumes de données
   - Robuste face aux données bruitées

### Pipeline de Traitement

1. **Chargement des données** : Lecture des fichiers CSV
2. **Préprocessing** :
   - Nettoyage et gestion des valeurs manquantes
   - Normalisation via StandardScaler
   - Réduction de dimensionnalité via PCA si nécessaire
3. **Entraînement** : Création d'un modèle Isolation Forest
4. **Détection** : Identification des points anormaux
5. **Post-traitement** : Analyse des résultats et génération de rapports
6. **Visualisation** : Création de graphiques pour l'interprétation

### Paramètres Configurables

- **contamination** : Proportion d'anomalies attendues (défaut: 0.01 = 1%)
- **n_estimators** : Nombre d'arbres dans l'Isolation Forest (défaut: 200)
- **max_samples** : Échantillons utilisés pour chaque arbre (défaut: 'auto')

## Visualisations

Le système génère plusieurs types de visualisations pour faciliter l'analyse :

1. **Heatmap de catégorie/sévérité** : Répartition des anomalies par type et gravité
2. **Histogrammes** : Distribution des scores d'anomalies
3. **Graphiques temporels** : Évolution des anomalies dans le temps (si données temporelles)

### Exemple de Heatmap

La heatmap de catégorie/sévérité permet de visualiser :
- Les catégories d'anomalies (axe Y)
- Les niveaux de gravité (axe X)
- La fréquence de chaque combinaison (couleur)

## Résultats et Interprétation

### Format des Résultats

Le système fournit :

1. **Statistiques globales** : Nombre total d'anomalies et pourcentage
2. **Top anomalies** : Les anomalies les plus sévères avec leurs scores
3. **Événements critiques** : Identification des événements principaux pour chaque anomalie
4. **Fichier de résultats** : Export CSV des anomalies détectées

### Interprétation des Scores

- **Score proche de 0** : comportement très normal
- **Score négatif (ex: -0.1)** : légèrement anormal
- **Score très négatif (ex: -0.5)** : très anormal

### Seuils Recommandés

- **0-2% d'anomalies** : Fonctionnement normal
- **5-15% d'anomalies** : Problème potentiel mineur
- **>20% d'anomalies** : Problème potentiellement sérieux

## Bonnes Pratiques

### Pour l'Entraînement

1. **Qualité des données** : Utilisez des données vraiment normales
2. **Volume suffisant** : Idéalement 10,000+ lignes pour l'entraînement
3. **Diversité** : Les données doivent couvrir différentes situations normales
4. **Réentraînement régulier** : Mettez à jour le modèle périodiquement

### Pour l'Analyse

1. **Vérification des top anomalies** : Examinez toujours les anomalies les plus sévères
2. **Analyse contextuelle** : Interprétez les résultats dans le contexte de votre système
3. **Suivi temporel** : Comparez les résultats dans le temps pour détecter des tendances
4. **Ajustement des seuils** : Adaptez les paramètres selon vos besoins spécifiques

## Extensibilité

Le système est conçu pour être facilement extensible :

1. **Nouveaux détecteurs** : Héritez de `BaseAnomalyDetector` pour créer des détecteurs spécialisés
2. **Nouvelles visualisations** : Ajoutez des scripts dans le dossier `scripts/`
3. **Intégration** : Le système peut être intégré dans des pipelines plus larges

## Limitations

- Optimisé pour les logs HDFS au format vectorisé
- Performance dépendante de la qualité des données d'entraînement
- Détecte les anomalies mais ne les explique pas automatiquement
- Les très gros fichiers peuvent nécessiter un traitement par lots

## Support et Dépannage

### Problèmes Courants

1. **Erreur d'encodage** : Le système essaie automatiquement UTF-8, Latin-1, et CP1252
2. **Mémoire insuffisante** : Échantillonnage automatique à 50,000 lignes
3. **Colonnes manquantes** : Ajout automatique avec valeurs 0

### Logs du Système

Les logs sont sauvegardés dans `logs/gestionlogs.log` pour le débogage.

## Documentation Supplémentaire

- **Documentation Complète** : Un document détaillé (`documentation.md`) contenant les explications techniques approfondies et le guide utilisateur complet
- **Scripts de Visualisation** : Des scripts Python pour générer des visualisations avancées (`scripts/visualize_anomalies.py`)

## Remarques Importantes

- **Fichiers CSV volumineux** : Les fichiers CSV (`normal_trace.csv`, `failure_trace.csv`, etc.) doivent être extraits du fichier zip avant utilisation car ils sont trop volumineux pour être manipulés directement dans l'archive
- **Extraction préalable** : Assurez-vous de dézipper complètement l'archive `gestion_logs.zip` avant d'exécuter les scripts
- **Explication Technique** : Détails sur l'algorithme Isolation Forest et son fonctionnement

## Crédits

- **Dataset** : LogHub – HDFS v3 (https://zenodo.org/record/8196385)
- **Algorithme** : Isolation Forest (scikit-learn)

