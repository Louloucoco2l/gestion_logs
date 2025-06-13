# Système de Détection d'Anomalies dans les Logs HDFS

## Description

Ce projet implémente un système intelligent de détection d'anomalies spécialement conçu pour analyser les logs HDFS (Hadoop Distributed File System) sous format vectorisé. Le système utilise des techniques d'apprentissage automatique pour identifier automatiquement les comportements anormaux dans les séquences d'événements.

## Fonctionnalités Principales

- **Détection d'anomalies HDFS** : Analyse spécialisée pour les logs HDFS vectorisés
- **Apprentissage automatique** : Utilise l'algorithme Isolation Forest pour la détection
- **Interface multiple** : Ligne de commande, interface interactive, et scripts dédiés
- **Préprocessing automatique** : Normalisation et réduction de dimensionnalité
- **Rapports détaillés** : Analyse des anomalies avec identification des événements critiques
- **Architecture modulaire** : Code organisé et extensible

## Structure du Projet

```
gestionlogs/
├── src/                          # Code source principal
│   ├── models/                   # Modèles de détection
│   │   ├── base_detector.py      # Classe de base abstraite
│   │   └── hdfs_detector.py      # Détecteur HDFS spécialisé
│   └── utils/                    # Utilitaires
│       ├── file_utils.py         # Gestion des fichiers
│       └── logger.py             # Système de logging
├── scripts/                      # Scripts d'exécution
│   ├── train_model.py            # Entraînement de modèles
│   ├── detect_anomalies.py       # Détection d'anomalies
│   └── interactive_cli.py        # Interface interactive
├── data/                         # Données du projet
│   ├── raw/                      # Données brutes
│   └── results/                  # Résultats d'analyse
├── models/                       # Modèles sauvegardés
├── logs/                         # Fichiers de log
└── main.py                       # Point d'entrée principal
```

## Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de packages Python)

### Installation des dépendances

```bash
pip install -r requirements.txt
```

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

## Configuration

### Paramètres du Modèle

- **contamination** : Proportion d'anomalies attendues (défaut: 0.01 = 1%)
- **n_estimators** : Nombre d'arbres dans l'Isolation Forest (défaut: 200)
- **max_samples** : Échantillons utilisés pour chaque arbre (défaut: 'auto')

### Préprocessing

- **Normalisation** : StandardScaler pour normaliser les features
- **Réduction de dimensionnalité** : PCA si plus de 100 dimensions
- **Échantillonnage** : Limitation à 50,000 échantillons pour l'entraînement

## Résultats

### Sortie de Détection

Le système fournit :

1. **Statistiques globales** : Nombre total d'anomalies et pourcentage
2. **Top anomalies** : Les 5 anomalies les plus sévères avec leurs scores
3. **Événements critiques** : Identification des événements principaux pour chaque anomalie
4. **Fichier de résultats** : Export CSV des anomalies détectées

### Exemple de Sortie

```
RÉSULTATS DE L'ANALYSE:
  - Total analysé: 29817 séquences HDFS
  - Anomalies trouvées: 22440
  - Pourcentage d'anomalies: 75.26%

TOP 5 ANOMALIES LES PLUS SÉVÈRES:
  1. Ligne 22623: Score = -0.211
     Événements principaux: {'bestNode+success': 16.0, 'chooseDataNode+success': 16.0}
```

## Architecture Technique

### Modèle de Détection

- **Algorithme** : Isolation Forest
- **Principe** : Isolation des points anormaux par partitionnement récursif
- **Avantages** : Efficace sur de gros volumes, pas besoin de données labellisées

### Pipeline de Traitement

1. **Chargement** : Lecture CSV avec gestion d'encodage multiple
2. **Validation** : Vérification de la structure des données
3. **Préprocessing** : Nettoyage et normalisation
4. **Entraînement/Prédiction** : Application du modèle
5. **Post-traitement** : Analyse et sauvegarde des résultats

## Extensibilité

### Ajouter un Nouveau Type de Détecteur

1. Hériter de `BaseAnomalyDetector`
2. Implémenter les méthodes abstraites
3. Ajouter le nouveau type dans les scripts

```python
from src.models.base_detector import BaseAnomalyDetector

class MonNouveauDetector(BaseAnomalyDetector):
    def load_data(self, file_path):
        # Implémentation spécifique
        pass

    def preprocess_data(self, data):
        # Préprocessing spécialisé
        pass
```

## Dépannage

### Problèmes Courants

1. **Erreur d'encodage** : Le système essaie automatiquement UTF-8, Latin-1, et CP1252
2. **Mémoire insuffisante** : Échantillonnage automatique à 50,000 lignes
3. **Colonnes manquantes** : Ajout automatique avec valeurs 0

### Logs

Les logs sont sauvegardés dans `logs/gestionlogs.log` pour le débogage.

## Performance

### Recommandations

- **Données d'entraînement** : 10,000 à 100,000 échantillons optimaux
- **Mémoire** : 4GB RAM recommandés pour de gros datasets
- **Temps d'exécution** : ~1-5 minutes selon la taille des données

## Contribution

### Structure de Développement

1. **Tests** : Ajouter des tests dans le dossier `tests/`
2. **Documentation** : Maintenir les docstrings en français
3. **Style** : Suivre PEP 8 pour le code Python

### Workflow de Développement

1. Fork du projet
2. Création d'une branche feature
3. Développement avec tests
4. Pull request avec description détaillée

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## Support

Pour toute question ou problème :

1. Vérifiez la documentation
2. Consultez les logs d'erreur
3. Ouvrez une issue sur le repository

## Changelog

### Version 2.0.0
- Refactorisation complète de l'architecture
- Séparation en modules spécialisés
- Interface en ligne de commande améliorée
- Documentation complète en français
- Suppression des émojis du code
- Amélioration du système de logging

### Version 1.0.0
- Implémentation initiale du détecteur HDFS
- Interface interactive de base
- Détection d'anomalies avec Isolation Forest
