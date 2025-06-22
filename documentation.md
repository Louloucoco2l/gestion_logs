# Documentation Complète du Système de Détection d'Anomalies

## Introduction

Ce document fournit une documentation technique complète du système de détection d'anomalies dans les logs HDFS. Il combine les informations essentielles du README, du guide utilisateur et des explications techniques pour offrir une vue d'ensemble exhaustive du projet.

## Table des Matières

1. [Vue d'ensemble du système](#vue-densemble-du-système)
2. [Architecture technique](#architecture-technique)
3. [Algorithme de détection](#algorithme-de-détection)
4. [Installation et configuration](#installation-et-configuration)
5. [Utilisation détaillée](#utilisation-détaillée)
6. [Format des données](#format-des-données)
7. [Visualisations](#visualisations)
8. [Interprétation des résultats](#interprétation-des-résultats)
9. [Bonnes pratiques](#bonnes-pratiques)
10. [Dépannage](#dépannage)
11. [Extensibilité et personnalisation](#extensibilité-et-personnalisation)
12. [Limitations connues](#limitations-connues)
13. [FAQ](#faq)

## Vue d'ensemble du système

Le système de détection d'anomalies est conçu pour analyser automatiquement les logs HDFS (Hadoop Distributed File System) afin d'identifier des comportements anormaux sans nécessiter d'exemples d'anomalies préalablement étiquetés. Il utilise l'apprentissage non-supervisé, spécifiquement l'algorithme Isolation Forest, pour distinguer les comportements normaux des comportements suspects.

### Cas d'utilisation principaux

- **Détection préventive** : Identifier les problèmes potentiels avant qu'ils n'affectent les utilisateurs
- **Analyse post-incident** : Comprendre les causes d'une panne ou d'un dysfonctionnement
- **Surveillance continue** : Maintenir une vigilance constante sur l'état du système
- **Sécurité** : Détecter des comportements potentiellement malveillants

### Fonctionnalités clés

- Détection d'anomalies sans exemples préalables
- Préprocessing automatique des données
- Rapports détaillés avec identification des événements critiques
- Visualisation avancées pour l'interprétation
- Interface multiple (CLI, interactive, scripts)
- Architecture modulaire et extensible

## Architecture technique

### Structure du projet

Le projet suit une architecture modulaire avec séparation claire des responsabilités :

```
gestion_logs/
├── config/                       # Configuration
├── data/                         # Données et résultats
├── logs/                         # Logs du système
├── models/                       # Modèles sauvegardés
├── scripts/                      # Scripts d'exécution
├── src/                          # Code source principal
│   ├── models/                  # Modèles de détection
│   └── utils/                   # Utilitaires
└── tests/                        # Tests
```

### Composants principaux

1. **Détecteurs d'anomalies** (`src/models/`) :
   - `base_detector.py` : Classe abstraite définissant l'interface commune
   - `hdfs_detector.py` : Implémentation spécifique pour les logs HDFS

2. **Utilitaires** (`src/utils/`) :
   - `logger.py` : Système de logging
   - `file_utils.py` : Gestion des fichiers et formats

3. **Scripts** (`scripts/`) :
   - `train_model.py` : Entraînement des modèles
   - `detect_anomalies.py` : Détection des anomalies
   - `interactive_cli.py` : Interface interactive
   - `visualize_anomalies.py` : Génération de visualisations

4. **Point d'entrée** (`main.py`) :
   - Interface unifiée pour toutes les fonctionnalités
   - Parsing des arguments de ligne de commande
   - Routage vers les composants appropriés

### Flux de données

1. **Entrée** : Fichiers CSV contenant des logs vectorisés
2. **Préprocessing** : Nettoyage, normalisation, réduction de dimensionnalité
3. **Traitement** : Entraînement ou détection via Isolation Forest
4. **Sortie** : Rapports, fichiers CSV de résultats, visualisation

## Algorithme de détection

### Isolation Forest : Principes fondamentaux

L'Isolation Forest est un algorithme de détection d'anomalies basé sur une idée simple mais puissante : les anomalies sont plus faciles à isoler que les points normaux.

#### Fonctionnement de base

1. **Construction d'arbres d'isolation** :
   - Sélection aléatoire d'une feature
   - Sélection aléatoire d'une valeur de split entre min et max
   - Division récursive jusqu'à isolation complète

2. **Mesure de l'anomalie** :
   - Calcul du nombre moyen d'étapes nécessaires pour isoler chaque point
   - Les points nécessitant moins d'étapes sont considérés comme anormaux

3. **Scoring** :
   - Normalisation des scores entre -1 et 1
   - Plus le score est négatif, plus le point est anormal

### Avantages de l'Isolation Forest

- **Efficacité computationnelle** : Complexité linéaire O(n)
- **Pas besoin d'exemples d'anomalies** : Apprentissage non-supervisé
- **Robustesse** : Peu sensible aux paramètres et au bruit
- **Scalabilité** : Peut traiter de grands volumes de données

### Paramètres clés

- **contamination** : Proportion attendue d'anomalies (défaut: 0.01)
- **n_estimators** : Nombre d'arbres dans la forêt (défaut: 200)
- **max_samples** : Taille des échantillons pour chaque arbre (défaut: 'auto')
- **random_state** : Graine pour la reproductibilité (défaut: 42)

### Préprocessing des données

1. **Nettoyage** :
   - Gestion des valeurs manquantes
   - Suppression des colonnes constantes
   - Conversion en format numérique

2. **Normalisation** :
   - StandardScaler : (valeur - moyenne) / écart-type
   - Met toutes les features sur une échelle comparable

3. **Réduction de dimensionnalité** (si nécessaire) :
   - PCA (Principal Component Analysis)
   - Appliquée si plus de 100 dimensions
   - Conserve 95% de la variance

## Installation et configuration

### Prérequis système

- Python 3.8 ou supérieur
- 4GB RAM minimum (8GB recommandés pour de gros datasets)
- Espace disque : 500MB minimum pour l'installation

### Dépendances Python

```
pandas>=1.0.0
numpy>=1.18.0
scikit-learn>=0.22.0
matplotlib>=3.1.0
seaborn>=0.10.0
pyyaml>=5.3.0
```

### Procédure d'installation

1. **Cloner le repository** :
   ```bash
   git clone https://github.com/votre-repo/gestion_logs.git
   cd gestion_logs
   ```

2. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

3. **Installation développeur** (optionnel) :
   ```bash
   pip install -e .
   ```

### Configuration

Les fichiers de configuration se trouvent dans le dossier `config/` :

1. **data_config.yaml** : Configuration des chemins et formats de données
2. **logging_config.yaml** : Configuration du système de logging
3. **model_config.yaml** : Paramètres des modèles de détection

Exemple de configuration du modèle :
```yaml
isolation_forest:
  contamination: 0.01
  n_estimators: 200
  max_samples: "auto"
  random_state: 42

preprocessing:
  normalize: true
  pca_threshold: 100
  pca_variance: 0.95
  max_samples: 50000
```

## Utilisation détaillée

### Interface interactive

L'interface interactive est le moyen le plus simple d'utiliser le système :

1. **Lancement** :
   ```bash
   python main.py
   ```

2. **Menu principal** :
   ```
   === SYSTÈME DE DÉTECTION D'ANOMALIES ===
   1. Créer un modèle
   2. Détecter des anomalies
   3. Lister les fichiers disponibles
   4. Quitter
   Votre choix (1-4):
   ```

3. **Création de modèle** :
   - Sélection du fichier d'entraînement
   - Configuration des paramètres (ou utilisation des valeurs par défaut)
   - Entraînement et sauvegarde du modèle

4. **Détection d'anomalies** :
   - Sélection du fichier à analyser
   - Chargement automatique du modèle
   - Analyse et affichage des résultats

### Ligne de commande

Pour une utilisation plus avancée ou dans des scripts :

1. **Création de modèle** :
   ```bash
   python main.py create normal_trace.csv
   ```

2. **Détection avec paramètres personnalisés** :
   ```bash
   python main.py detect failure_trace.csv --contamination 0.05 --model-type hdfs
   ```

3. **Listing des fichiers** :
   ```bash
   python main.py list
   ```

### Scripts spécialisés

Pour des cas d'utilisation avancés :

1. **Entraînement avancé** :
   ```bash
   python scripts/train_model.py --data normal_trace.csv --contamination 0.02 --n-estimators 300
   ```

2. **Détection avec visualisation** :
   ```bash
   python scripts/detect_anomalies.py --data failure_trace.csv --visualize --output-dir reports/
   ```

3. **Génération de visualisation spécifiques** :
   ```bash
   python scripts/visualize_anomalies.py --input data/results/anomalies_failure_trace.csv --output data/visualizations/heatmap.png
   ```

## Format des données

### Format d'entrée

Le système est conçu pour traiter des logs HDFS vectorisés au format CSV :

1. **Structure générale** :
   - Première ligne : en-têtes des colonnes
   - Première colonne (optionnelle) : identifiant de séquence
   - Autres colonnes : types d'événements
   - Valeurs : compteurs d'occurrences

2. **Exemple** :
   ```csv
   TaskID,getFileInfo+success,blockSeekTo+ioexception,sendBlock+success,...
   Task_1,5,0,3,...
   Task_2,2,1,4,...
   ```

3. **Conventions de nommage** :
   - Les noms de colonnes suivent généralement le format `action+résultat`
   - Exemples : `getFileInfo+success`, `blockSeekTo+ioexception`

### Format de sortie

Les résultats sont sauvegardés dans plusieurs formats :

1. **CSV d'anomalies** (`data/results/anomalies_*.csv`) :
   - Contient les lignes identifiées comme anormales
   - Inclut le score d'anomalie et les événements principaux

2. **Rapports textuels** (console) :
   - Statistiques globales
   - Top anomalies avec leurs caractéristiques

3. **Visualisation** (`data/visualizations/`) :
   - Heatmap
   - Format PNG haute résolution

## Visualisations

### Type de visualisation disponibles

**Heatmap de catégorie/sévérité** :
   - Axes : catégories d'anomalies vs niveaux de gravité
   - Couleurs : fréquence des occurrences
   - Utilité : identifier les patterns dominants


```bash
python scripts/visualize_anomalies.py --input data/results/anomalies_failure_trace.csv --output custom_viz.png --log-scale
```

Options disponibles :
- `--log-scale` : Utilise une échelle logarithmique pour les valeurs
- `--figsize` : Taille de la figure (largeur,hauteur)
- `--cmap` : Palette de couleurs (ex: 'viridis', 'plasma', 'YlOrRd')

## Interprétation des résultats

### Comprendre les scores d'anomalie

Les scores d'anomalie de l'Isolation Forest sont normalisés entre -1 et 1 :

- **Score proche de 1** : Très normal
- **Score proche de 0** : À la limite
- **Score négatif** : Anormal
- **Score très négatif (< -0.3)** : Très anormal

### Analyse des événements critiques

Pour chaque anomalie, le système identifie les événements qui contribuent le plus à son caractère anormal :

```
Ligne 5623: Score = -0.211
Événements principaux: {'Erreur_Réseau': 25, 'Timeout': 10}
```

Interprétation : Cette séquence contient un nombre anormalement élevé d'erreurs réseau et de timeouts.

### Seuils d'alerte recommandés

- **< 2% d'anomalies** : Situation normale
- **2-5% d'anomalies** : Vigilance
- **5-15% d'anomalies** : Alerte mineure
- **15-30% d'anomalies** : Alerte majeure
- **> 30% d'anomalies** : Situation critique

### Analyse contextuelle

Les résultats doivent toujours être interprétés dans le contexte spécifique du système :

1. **Comparaison historique** : Comment ces résultats se comparent-ils aux analyses précédentes?
2. **Événements connus** : Y a-t-il eu des changements récents qui pourraient expliquer ces anomalies?
3. **Impact réel** : Ces anomalies ont-elles un impact observable sur le système?

## Bonnes pratiques

### Préparation des données

1. **Qualité des données d'entraînement** :
   - Utilisez uniquement des données normales pour l'entraînement
   - Assurez-vous que les données couvrent toutes les situations normales
   - Minimum 10,000 lignes pour un modèle robuste

2. **Nettoyage préalable** :
   - Vérifiez l'absence de valeurs aberrantes connues
   - Assurez-vous de la cohérence du format

3. **Échantillonnage intelligent** :
   - Pour les très gros fichiers, utilisez un échantillonnage stratifié
   - Assurez-vous que l'échantillon est représentatif

### Cycle de vie du modèle

1. **Création initiale** :
   - Utilisez des données historiques validées comme normales
   - Testez différentes valeurs de contamination (0.01, 0.05, 0.1)
   - Validez sur des données connues (avec anomalies identifiées)

2. **Utilisation régulière** :
   - Analysez de nouveaux logs quotidiennement ou hebdomadairement
   - Conservez les résultats pour analyse de tendances

3. **Réentraînement** :
   - Réentraînez le modèle tous les 1-3 mois
   - Réentraînez immédiatement après des changements majeurs du système

### Analyse des résultats

1. **Priorisation** :
   - Concentrez-vous d'abord sur les anomalies avec les scores les plus négatifs
   - Examinez les patterns récurrents dans les événements principaux

2. **Validation croisée** :
   - Vérifiez si les anomalies détectées correspondent à des problèmes réels
   - Ajustez le seuil de contamination en fonction des résultats

3. **Documentation** :
   - Documentez les anomalies significatives et leurs causes
   - Créez une base de connaissances des patterns anormaux

## Dépannage

### Problèmes courants et solutions

1. **"Fichier non trouvé"** :
   - Vérifiez que le fichier est dans le bon dossier
   - Utilisez `python main.py list` pour voir les fichiers disponibles
   - Vérifiez les permissions du fichier

2. **"Erreur d'encodage"** :
   - Le système essaie automatiquement UTF-8, Latin-1, et CP1252
   - Si l'erreur persiste, convertissez manuellement le fichier en UTF-8

3. **"Mémoire insuffisante"** :
   - Réduisez la taille de l'échantillon avec `--max-samples`
   - Augmentez la mémoire disponible
   - Traitez le fichier par morceaux

4. **"Modèle non trouvé"** :
   - Assurez-vous d'avoir créé un modèle avant la détection
   - Vérifiez le dossier `models/` pour les modèles existants

5. **Trop/pas assez d'anomalies détectées** :
   - Ajustez le paramètre `contamination`
   - Vérifiez la qualité des données d'entraînement
   - Assurez-vous que les données de test sont comparables aux données d'entraînement

### Logs du système

Les logs du système sont sauvegardés dans `logs/gestionlogs.log` :

```
2023-06-22 14:30:15 INFO [hdfs_detector.py:125] Chargement du fichier normal_trace.csv
2023-06-22 14:30:18 INFO [hdfs_detector.py:142] Préprocessing des données: 29817 lignes, 46 colonnes
2023-06-22 14:30:25 INFO [hdfs_detector.py:165] Entraînement du modèle avec contamination=0.01
2023-06-22 14:30:32 INFO [hdfs_detector.py:180] Modèle sauvegardé dans models/isolation_forest_20230622.pkl
```

Utilisez ces logs pour diagnostiquer les problèmes :
- Vérifiez les erreurs et avertissements
- Suivez le flux d'exécution
- Identifiez les étapes qui prennent le plus de temps

## Extensibilité et personnalisation

### Ajouter un nouveau type de détecteur

1. **Créer une nouvelle classe** dans `src/models/` :
   ```python
   from .base_detector import BaseAnomalyDetector

   class MonNouveauDetector(BaseAnomalyDetector):
       def load_data(self, file_path):
           # Implémentation spécifique
           pass

       def preprocess_data(self, data):
           # Préprocessing spécialisé
           pass
   ```

2. **Enregistrer le détecteur** dans `main.py` :
   ```python
   # Ajouter l'import
   from models.mon_nouveau_detector import MonNouveauDetector

   # Ajouter dans le traitement des arguments
   if args.model_type == "mon_type":
       detector = MonNouveauDetector(contamination=args.contamination)
   ```

### Personnaliser les visualisations

1. **Créer un nouveau script** dans `scripts/` :
   ```python
   # ma_visualisation.py
   import matplotlib.pyplot as plt
   import pandas as pd

   def create_custom_viz(data_file, output_file):
       # Charger les données
       df = pd.read_csv(data_file)

       # Créer la visualisation
       plt.figure(figsize=(12, 8))
       # ... code de visualisation ...
       plt.savefig(output_file)
   ```

2. **Ajouter l'option** dans `main.py` ou créer un point d'entrée dédié.

### Intégration avec d'autres systèmes

Le système peut être intégré dans des pipelines plus larges :

1. **API Python** :
   ```python
   from src.models.hdfs_detector import HDFSDetector

   detector = HDFSDetector(contamination=0.01)
   detector.create_model_from_file("normal_data.csv")
   results = detector.detect_anomalies_in_file("test_data.csv")
   ```

2. **Automatisation** :
   - Créez des scripts cron pour l'exécution régulière
   - Intégrez dans des pipelines CI/CD
   - Connectez à des systèmes d'alerte

## Limitations connues

1. **Spécificité du format** :
   - Optimisé pour les logs HDFS vectorisés
   - Adaptation nécessaire pour d'autres formats

2. **Détection sans explication** :
   - Identifie QU'il y a une anomalie mais pas POURQUOI
   - L'analyse des événements principaux aide mais reste limitée

3. **Sensibilité aux données d'entraînement** :
   - La qualité de détection dépend entièrement de la qualité des données d'entraînement
   - Des données d'entraînement contenant des anomalies non détectées fausseront le modèle

4. **Évolution temporelle** :
   - Les systèmes évoluent, ce qui était normal hier peut ne plus l'être aujourd'hui
   - Nécessité de réentraîner régulièrement le modèle

5. **Performance sur très gros volumes** :
   - Échantillonnage nécessaire au-delà de plusieurs millions de lignes
   - Compromis entre exhaustivité et performance

## FAQ

### Questions générales

**Q: Quelle est la différence entre ce système et un simple seuil d'alerte?**  
R: Les seuils d'alerte traditionnels sont statiques et définis manuellement pour chaque métrique. Notre système apprend automatiquement ce qui est "normal" à partir des données et peut détecter des anomalies complexes impliquant plusieurs métriques simultanément.

**Q: Le système peut-il détecter des attaques ou intrusions?**  
R: Oui, si ces attaques génèrent des patterns anormaux dans les logs. Cependant, le système n'est pas spécifiquement conçu pour la sécurité et devrait compléter, non remplacer, les solutions de sécurité dédiées.

**Q: À quelle fréquence dois-je analyser mes logs?**  
R: Cela dépend de votre cas d'utilisation. Pour une surveillance proactive, une analyse quotidienne ou même horaire peut être appropriée. Pour une analyse post-mortem, une analyse ponctuelle suffit.

### Questions techniques

**Q: Pourquoi utiliser l'Isolation Forest plutôt qu'un autre algorithme?**  
R: L'Isolation Forest offre plusieurs avantages: il est efficace sur de grands volumes de données, ne nécessite pas d'exemples d'anomalies pour l'apprentissage, et est relativement insensible aux paramètres. D'autres algorithmes comme One-Class SVM ou LOF pourraient être implémentés dans de futures versions.

**Q: Comment choisir la valeur de contamination optimale?**  
R: Commencez avec la valeur par défaut (0.01 = 1%). Si vous obtenez trop peu d'anomalies, augmentez progressivement (0.05, 0.1). Si vous obtenez trop d'anomalies, diminuez (0.005, 0.001). L'idéal est de calibrer sur des données où vous connaissez déjà quelques anomalies.

**Q: Le système peut-il traiter des données en temps réel?**  
R: La version actuelle est conçue pour l'analyse par lots. Pour une analyse en temps réel, vous devriez adapter le système pour traiter des flux de données et implémenter une logique de mise à jour incrémentale du modèle.

### Questions d'utilisation

**Q: Comment interpréter un taux d'anomalies très élevé (>50%)?**  
R: Un taux aussi élevé indique généralement l'un de ces problèmes:
1. Le modèle a été entraîné sur des données non représentatives
2. Le système analysé a radicalement changé depuis l'entraînement
3. La valeur de contamination est trop élevée
4. Il y a effectivement un problème majeur dans le système

**Q: Dois-je investiguer toutes les anomalies détectées?**  
R: Non, concentrez-vous sur:
1. Les anomalies avec les scores les plus négatifs
2. Les clusters d'anomalies (plusieurs anomalies similaires)
3. Les anomalies impliquant des événements critiques pour votre système

**Q: Comment savoir si mon modèle fonctionne correctement?**  
R: Validez votre modèle en:
1. Vérifiant qu'il détecte des anomalies connues
2. Confirmant que le taux d'anomalies est raisonnable (généralement 0.5-5%)
3. Examinant si les événements principaux identifiés sont effectivement anormaux
